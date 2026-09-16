#!/usr/bin/env python3
"""Replace the old Protego branding in the program documents with TPP's.

These are the customer-facing lease addendum and terms, where "Protego" is the
plan's *name*, not just a link — so this rewrites the wording as well as the
URLs, in the Word originals, and leaves the formatting alone.

    python3 tools/documents/rebrand.py documents/tpp/*.docx          # apply
    python3 tools/documents/rebrand.py --dry-run documents/tpp/*.docx

The replacement URLs are TPP's own, the same ones the portal already cites:
tppclaims.com for claims and tpptermsandconditions.com for the terms.

Word splits a paragraph into runs wherever formatting changes, so a phrase can
straddle several of them. Each paragraph is therefore rebuilt from its runs:
the replaced text goes into the first run that held any of the match and the
rest are emptied, which keeps the paragraph's formatting except across a
boundary that a replacement spans.
"""
import argparse, re, shutil, sys, zipfile
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
ET.register_namespace("w", W[1:-1])

# Longest first: a specific phrase must win over a shorter one inside it.
RULES = [
    (r"www\.ProtegoClaims\.com",            "tppclaims.com"),
    (r"https?://www\.ProtegoClaims\.com",   "https://tppclaims.com"),
    (r"https?://protegotermsconditions\.com", "https://tpptermsandconditions.com"),
    (r"www\.protegotermsconditions\.com",   "tpptermsandconditions.com"),
    (r"protegotermsconditions\.com",        "tpptermsandconditions.com"),
    (r"Protegoclaims\.com",                 "tppclaims.com"),
    (r"ProtegoClaims\.com",                 "tppclaims.com"),
    (r"Protego\s*CUSTOMER PROTECTION PLAN", "TPP SECURE CUSTOMER PROTECTION PLAN"),
    (r"ProtegoSECURE",                      "TPP SECURE"),
    (r"Protego Protection Plan",            "TPP Secure Protection Plan"),
    (r"Protego Secure Addendum",            "TPP Secure Addendum"),
    (r"Protego Claims",                     "TPP Claims"),
    (r"Protego Plan",                       "TPP Secure Plan"),
    # Anything left standing alone is the company itself.
    (r"Protego",                            "Tenant Property Protection"),
]
PATTERNS = [(re.compile(p), r) for p, r in RULES]
HIT = re.compile(r"[Pp]rotego")


def rewrite(text):
    for pat, rep in PATTERNS:
        text = pat.sub(rep, text)
    return text


def rewrite_paragraph(p):
    """Rewrite one <w:p>, returning how many replacements it made.

    Word splits a paragraph into runs wherever formatting changes, so a phrase
    can straddle several of them — "Protego Protection Plan" is three runs. The
    match therefore has to be found in the paragraph's joined text, or the bare
    word matches first and the phrase rule never fires. Each replacement is then
    emitted into the run where its match *started* and the matched characters
    are dropped from wherever else they sat, so formatting outside the matched
    spans is untouched.
    """
    ts = [t for r in p.iter(W + "r") for t in r.iter(W + "t")]
    if not ts:
        return 0
    texts = [t.text or "" for t in ts]
    joined = "".join(texts)
    if not HIT.search(joined):
        return 0

    # Longest match wins at each position, so rule order cannot mis-rank them.
    spans, i = [], 0
    while i < len(joined):
        best = None
        for pat, rep in PATTERNS:
            m = pat.match(joined, i)
            if m and m.end() > m.start() and (best is None or m.end() > best[0].end()):
                best = (m, rep)
        if best:
            m, rep = best
            spans.append((m.start(), m.end(), rep))
            i = m.end()
        else:
            i += 1
    if not spans:
        return 0

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


def process(path, dry_run=False):
    zin = zipfile.ZipFile(path)
    parts, hits = {}, 0
    for name in zin.namelist():
        data = zin.read(name)
        if name.endswith(".rels") or name == "[Content_Types].xml":
            text = data.decode("utf8")
            if HIT.search(text):
                hits += len(HIT.findall(text))
                data = rewrite(text).encode("utf8")
        elif re.match(r"word/(document|header\d*|footer\d*|footnotes|endnotes|comments)\.xml$", name):
            root = ET.fromstring(data)
            n = sum(rewrite_paragraph(p) for p in root.iter(W + "p"))
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
    ap.add_argument("files", nargs="+")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    total = 0
    for f in a.files:
        n = process(f, a.dry_run)
        total += n
        print(f"{'would change' if a.dry_run else 'changed':>13} {n:>3}  {f}")
    print(f"\n{total} replacement(s){' (dry run, nothing written)' if a.dry_run else ''}")
