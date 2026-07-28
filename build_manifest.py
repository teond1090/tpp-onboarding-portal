"""Scan the documents folders and write documents/manifest.json for the portal.

Run this via PUBLISH.bat - you should not need to touch it directly.

How matching works: each document card in the portal has a short key
(e.g. 'addendum'). A PDF is matched to that card if the key appears anywhere in
the filename, ignoring case, spaces, underscores and hyphens. Anything that
doesn't match a card still appears on the site, under the same program, rather
than being silently dropped.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, 'documents')

# folder name -> the keys used by that program's cards, longest first so that
# a specific key wins over a shorter one contained inside it
PROGRAMS = {
    'portable-container': ['prelaunch-letter', 'addendum', 'terms', 'reporting'],
    'tpp-secure':         ['announcement-letter', 'addendum', 'terms', 'birdseye', 'reporting'],
    'rv-park-n-protect':  ['announcement-letter', 'addendum', 'terms', 'reporting'],
}

ALLOWED = {'.pdf', '.docx', '.doc', '.xlsx', '.png', '.jpg', '.jpeg'}

def norm(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

def pretty(fname):
    stem = os.path.splitext(fname)[0]
    stem = re.sub(r'[_-]+', ' ', stem).strip()
    return re.sub(r'\s+', ' ', stem)

manifest = {'programs': {}}
total = matched_total = 0
problems = []

for pid, keys in PROGRAMS.items():
    folder = os.path.join(DOCS, pid)
    os.makedirs(folder, exist_ok=True)
    matched, extra, used = {}, [], set()

    files = sorted(f for f in os.listdir(folder)
                   if os.path.isfile(os.path.join(folder, f)) and not f.startswith('.')
                   and f.lower() != 'readme.txt')

    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext not in ALLOWED:
            problems.append(f'{pid}/{f}  (skipped - {ext or "no extension"} is not a document type)')
            continue
        total += 1
        n = norm(f)
        hit = next((k for k in sorted(keys, key=len, reverse=True)
                    if norm(k) in n and k not in used), None)
        rel = f'documents/{pid}/{f}'.replace('\\', '/')
        if hit:
            matched[hit] = rel
            used.add(hit)
            matched_total += 1
            print(f'  [card ] {pid}/{f}  ->  "{hit}"')
        else:
            extra.append({'name': pretty(f), 'path': rel})
            print(f'  [extra] {pid}/{f}  ->  shown as its own card')

    manifest['programs'][pid] = {'matched': matched, 'extra': extra}

os.makedirs(DOCS, exist_ok=True)
with open(os.path.join(DOCS, 'manifest.json'), 'w', encoding='utf-8') as fh:
    json.dump(manifest, fh, indent=1)

print()
print(f'{total} document(s) found - {matched_total} matched to a card, {total - matched_total} extra.')
if problems:
    print('\nSkipped:')
    for p in problems:
        print('  ' + p)
print('\nmanifest.json written.')
