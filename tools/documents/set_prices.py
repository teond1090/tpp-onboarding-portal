#!/usr/bin/env python3
"""Change the monthly fees in an addendum's rate table.

Every replacement is decided from the paragraph's *original* text and applied
in one pass, so a chain like $9 -> $12 -> $15 cannot run away: the cell that
held $9.00 becomes $12.00 and the one that already held $12.00 becomes $15.00,
rather than both ending up at $15.00.

The rate table appears twice in these documents — once as the table and once
as a text box holding the same values run together — so the replacement works
on substrings as well as whole cells.

    python3 tools/documents/set_prices.py doc.docx --map '$9.00=$12.00' '$12.00=$15.00'
"""
import argparse, re, shutil, zipfile
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
ET.register_namespace("w", W[1:-1])


def own_texts(p):
    """The <w:t> elements this paragraph owns directly.

    A text box lives inside a run, and its own paragraphs hang below that, so
    a plain p.iter() walk reaches the text box's text from the outer paragraph
    *and* again from the nested paragraph — applying every replacement twice.
    Descending stops at a nested <w:p> so each piece of text is visited once.
    """
    out = []
    def walk(node):
        for ch in node:
            if ch.tag == W + "p":
                continue
            if ch.tag == W + "t":
                out.append(ch)
            else:
                walk(ch)
    walk(p)
    return out


def rewrite_paragraph(p, mapping, pattern):
    ts = own_texts(p)
    if not ts:
        return 0
    texts = [t.text or "" for t in ts]
    joined = "".join(texts)
    if not pattern.search(joined):
        return 0
    spans = [(m.start(), m.end(), mapping[m.group(0)]) for m in pattern.finditer(joined)]
    starts = {s: rep for s, _, rep in spans}
    covered = {x for s, e, _ in spans for x in range(s, e)}
    pos = 0
    for t, txt in zip(ts, texts):
        buf = []
        for j in range(len(txt)):
            idx = pos + j
            if idx in starts:
                buf.append(starts[idx])
            elif idx not in covered:
                buf.append(joined[idx])
        t.text = "".join(buf)
        pos += len(txt)
    return len(spans)


def process(path, mapping, dry_run=False):
    pattern = re.compile("|".join(re.escape(k) for k in sorted(mapping, key=len, reverse=True)))
    zin = zipfile.ZipFile(path)
    parts, hits = {}, 0
    for name in zin.namelist():
        data = zin.read(name)
        if re.match(r"word/(document|header\d*|footer\d*)\.xml$", name):
            root = ET.fromstring(data)
            n = sum(rewrite_paragraph(p, mapping, pattern) for p in root.iter(W + "p"))
            if n:
                hits += n
                data = ET.tostring(root, encoding="UTF-8", xml_declaration=True)
        parts[name] = data
    zin.close()
    if hits and not dry_run:
        shutil.copy2(path, path + ".bak")
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zout:
            for name, data in parts.items():
                zout.writestr(name, data)
    return hits


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--map", nargs="+", required=True, metavar="OLD=NEW")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    mapping = dict(m.split("=", 1) for m in a.map)
    print(f"{process(a.file, mapping, a.dry_run)} replacement(s) in {a.file}")
