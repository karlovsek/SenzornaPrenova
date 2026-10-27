"""Izdela PDF učbenika Senzorna prenova (izdaja 2) s številkami strani v kazalu.

Pass 1: tisk z nevidnimi označevalci @@id@@ v naslovih in nadomestkom 000 v kazalu.
Iz PDF preberemo stran vsakega označevalca, jih vpišemo kot data-page in natisnemo
znova. Kontrolni tisk (z označevalci) preveri, da se številke ujemajo; nato končni tisk.
Uporaba: python tools/build_pdf.py  (odvisnosti: pip install --target tools/pylib -r tools/requirements.txt)
"""
import json, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "pylib"))
from pypdf import PdfReader  # noqa: E402

PROJ = HERE.parent
SRC = PROJ / "Senzorna prenova – zgornji del trupa.html"
OUT = PROJ / "Senzorna prenova – zgornji del trupa.pdf"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
WORK = HERE / "build"
WORK.mkdir(exist_ok=True)

MARKER_JS = """<script>
document.querySelectorAll("[data-toc]").forEach(function(el){
  var h=el.querySelector("h2")||el, m=document.createElement("span");
  m.textContent="@@"+el.id+"@@";
  m.style.cssText="position:absolute;font-size:1px;line-height:1px;color:#fff;white-space:nowrap";
  h.insertBefore(m,h.firstChild);
});
</script>
</body>"""


FONT_LINK = re.compile(r'<link rel="stylesheet" href="(https://fonts\.googleapis\.com/[^"]+)">')
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0 Safari/537.36"


def inline_fonts(url):
    """Google Fonts (latin, latin-ext) kot base64, da jih Chrome brez okna zagotovo uporabi."""
    cache = WORK / "fonts.css"
    if cache.exists():
        return cache.read_text(encoding="utf-8")
    import base64, urllib.request

    def get(u):
        return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=30).read()

    css = get(url.replace("&amp;", "&")).decode("utf-8")
    out = []
    for subset, block in re.findall(r"/\* ([\w-]+) \*/\s*(@font-face \{.*?\})", css, re.S):
        if subset not in ("latin", "latin-ext"):
            continue
        furl = re.search(r"url\((https://[^)]+)\)", block).group(1)
        data = base64.b64encode(get(furl)).decode("ascii")
        block = block.replace(furl, "data:font/woff2;base64," + data).replace("font-display: swap", "font-display: block")
        out.append(block)
    cache.write_text("\n".join(out), encoding="utf-8")
    return cache.read_text(encoding="utf-8")


def make_html(pages, markers):
    html = SRC.read_text(encoding="utf-8")
    m = FONT_LINK.search(html)
    if m:
        html = html.replace(m.group(0), "<style>" + inline_fonts(m.group(1)) + "</style>", 1)

    def add_page(m):
        pid = m.group(1)
        return f'id="{pid}" data-page="{pages.get(pid, "000")}" data-toc='

    html = re.sub(r'id="([^"]+)" data-toc=', add_page, html)
    if markers:
        html = html.replace("</body>", MARKER_JS, 1)
    return html


def render(html, pdf):
    tmp = WORK / "page.html"
    tmp.write_text(html, encoding="utf-8")
    if pdf.exists():
        pdf.unlink()
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=15000", f"--print-to-pdf={pdf}",
                    tmp.as_uri()], check=True, capture_output=True, timeout=180)
    if not pdf.exists():
        raise SystemExit("Chrome ni ustvaril PDF")


def marker_pages(pdf):
    found = {}
    for i, page in enumerate(PdfReader(str(pdf)).pages, start=1):
        text = re.sub(r"\s+", "", page.extract_text() or "")
        for pid in re.findall(r"@@([A-Za-z0-9_-]+)@@", text):
            found.setdefault(pid, i)
    return found


ids = re.findall(r'id="([^"]+)" data-toc=', SRC.read_text(encoding="utf-8"))
render(make_html({}, True), WORK / "pass1.pdf")
pages = {k: str(v) for k, v in marker_pages(WORK / "pass1.pdf").items()}
missing = [i for i in ids if i not in pages]
if missing:
    raise SystemExit(f"Ni označevalcev za: {missing}")

for attempt in range(3):
    render(make_html(pages, True), WORK / "check.pdf")
    got = {k: str(v) for k, v in marker_pages(WORK / "check.pdf").items()}
    if got == pages:
        break
    print("Premik strani, ponavljam:", {k: (pages[k], got.get(k)) for k in ids if pages[k] != got.get(k)})
    pages = got
else:
    raise SystemExit("Številke strani se ne ustalijo")

render(make_html(pages, False), WORK / "final.pdf")
try:
    OUT.write_bytes((WORK / "final.pdf").read_bytes())
except PermissionError:
    raise SystemExit(f"{OUT.name} je odprt v drugem programu. Zaprite ga in poženite znova "
                     f"(PDF je že v {WORK / 'final.pdf'}).")
n = len(PdfReader(str(OUT)).pages)
(WORK / "pages.json").write_text(json.dumps(pages, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"OK: {OUT.name}, {n} strani")
print(" ".join(f"{k}={pages[k]}" for k in ids))
