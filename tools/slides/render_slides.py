import asyncio, json, sys, pathlib
from playwright.async_api import async_playwright
html_dir, out_dir = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
names = json.load(open(html_dir.parent/'slide_names.json')) if (html_dir.parent/'slide_names.json').exists() else [p.stem for p in sorted(html_dir.glob('*.html'))]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        pg = await b.new_page(viewport={"width":1920,"height":1080}, device_scale_factor=1)
        for n in names:
            await pg.goto((html_dir/f"{n}.html").resolve().as_uri()); await pg.wait_for_timeout(150)
            # anything past the 1280px text edge that is not the brand/photo is a layout fault — report it
            over = await pg.evaluate("""() => [...document.querySelectorAll('.slide *')]
              .filter(e => !e.closest('.photo') && !e.classList.contains('photo') && !e.classList.contains('brand'))
              .map(e => [e, e.getBoundingClientRect()]).filter(([e,r]) => r.width>0 && r.right>1282 && e.children.length===0)
              .map(([e,r]) => e.tagName+':'+Math.round(r.right)+':'+(e.textContent||'').trim().slice(0,30))""")
            await pg.screenshot(path=str(out_dir/f"{n}.png"))
            print(n, ("OVER " + "; ".join(over)) if over else "ok")
        await b.close()
asyncio.run(main())
