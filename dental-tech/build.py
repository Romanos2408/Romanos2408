#!/usr/bin/env python3
"""Builds dental-tech.gr from src/ into site/.

Pages live in src/pages/<slug>.html. Each starts with a header comment:

    <!--
    title: The <title> (what Google shows as the link)
    description: The grey text under the link on Google
    -->

Tokens you can use in a page:
  {{photo:name|alt|class|fallback}}  src/photos/name.(jpg|png|webp); if it's
      missing and a fallback is given, a soft placeholder is shown instead.
  {{icon:name}}   an inline line icon from ICONS below.
  {{contact}}     the dark "call me" panel.

Run `python3 build.py`, then upload the contents of site/.
`python3 build.py --pages DIR` builds the shareable preview (colour switcher,
hidden from Google). `pip install pillow` lets the build resize photos.
"""
import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
PHOTOS = SRC / "photos"
OUT = ROOT / "site"

DOMAIN = "https://www.dental-tech.gr"
GOOGLE_VERIFICATION = "9U862btudvMgP9ZRfHiI7--urNMIV4rYU9bUqNHhfRM"
PHONE, TEL, EMAIL = "6944 648 748", "+306944648748", "tech@dental-tech.gr"
VIBER = "viber://chat?number=%2B306944648748"

# The colour the real site ships with: "navy", "charcoal" or "teal".
PALETTE = "navy"
PALETTES = [("navy", "Navy", "#1b2f5e"), ("charcoal", "Ανθρακί", "#2b2e33"), ("teal", "Πετρόλ", "#0b6b7a")]

NAV = [("index", "Αρχική"), ("ypiresies", "Υπηρεσίες"), ("giorgos", "Ποιος είμαι"), ("epikoinonia", "Επικοινωνία")]

ICONS = {
    "phone": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>',
    "video": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="14" height="12" rx="2"/><path d="m16 10 6-3v10l-6-3z"/></svg>',
    "logo": '<svg viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="12" style="fill:var(--logo,#0d6b56)"/><path d="M20 10.5c-2.1 0-3 .9-4.6.9s-2.6-1-4.3.2c-1.9 1.4-1.9 4.6-1 7.4.8 2.6 1.4 7.6 3.2 8.6 1.6.9 1.9-3.6 3-5.2.7-1 1.5-1.4 3.7-1.4s3 .4 3.7 1.4c1.1 1.6 1.4 6.1 3 5.2 1.8-1 2.4-6 3.2-8.6.9-2.8.9-6-1-7.4-1.7-1.2-2.7-.2-4.3-.2s-2.5-.9-4.6-.9z" fill="none" stroke="#fff" stroke-width="2" stroke-linejoin="round"/><circle cx="31" cy="9" r="3.2" style="fill:var(--logo-dot,#7fe0bf)"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "search": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.2-4.2"/><path d="M8.5 11h5M11 8.5v5"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3 5 6v5c0 4.5 3 8 7 10 4-2 7-5.5 7-10V6z"/><path d="m9 12 2 2 4-4"/></svg>',
    "swap": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 8h13l-3-3M20 16H7l3 3"/></svg>',
    "handpiece": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21 15 9"/><path d="m13 7 4 4"/><path d="M16 8l3-3 1 1-3 3"/><path d="M19 5l1.5-1.5"/></svg>',
    "autoclave": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="10" cy="12" r="4"/><path d="M17 9h1M17 12h1M17 15h1"/></svg>',
    "xray": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M12 7.5c-1.2 0-1.7.5-2.6.5S8 7.3 7.3 8c-.8.8-.6 2.6 0 4 .5 1.3.8 3.8 1.7 4 .8.2 1-2 1.6-2.7.4-.4.8-.5 1.4-.5s1 .1 1.4.5c.6.7.8 2.9 1.6 2.7.9-.2 1.2-2.7 1.7-4 .6-1.4.8-3.2 0-4-.7-.7-1.2 0-2.1 0s-1.4-.5-2.6-.5z"/></svg>',
    "clinic": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18M5 21V8l7-4 7 4v13"/><path d="M12 9v5M9.5 11.5h5"/></svg>',
    "laptop": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="5" width="16" height="11" rx="1.5"/><path d="M2 19h20"/></svg>',
    "spark": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v4M12 17v4M3 12h4M17 12h4M5.6 5.6l2.8 2.8M15.6 15.6l2.8 2.8M5.6 18.4l2.8-2.8M15.6 8.4l2.8-2.8"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 7 8.5-7"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
    "star": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7.5l1.3 3 3.2.3-2.4 2.1.7 3.1-2.8-1.6-2.8 1.6.7-3.1-2.4-2.1 3.2-.3z"/></svg>',
    "cap": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c2 2 10 2 12 0v-5"/></svg>',
    "heart": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/></svg>',
}

# Every page of the old site now lands on the matching new page.
REDIRECTS = {
    "/index.html": "/",
    "/Pages/index.html": "/",
    "/Pages/about.html": "/giorgos.html",
    "/Pages/contact.html": "/epikoinonia.html",
    "/Pages/remoterepair.html": "/epikoinonia.html#video",
    "/Pages/parts-equipment-repair.html": "/ypiresies.html#edres",
    "/Pages/anakataskeyes.html": "/ypiresies.html#edres",
    "/Pages/dental-chairs.html": "/ypiresies.html#edres",
    "/Pages/handpiece-repair.html": "/ypiresies.html#xeirolaves",
    "/Pages/sterilizer-repair.html": "/ypiresies.html#autokaustoi",
    "/Pages/DigiRadiography.html": "/ypiresies.html#aktinografia",
    "/Pages/dental-equipment.html": "/ypiresies.html#eksoplismos",
    "/Pages/lasers.html": "/ypiresies.html#eksoplismos",
    "/Pages/arch_studies.html": "/ypiresies.html#iatreio",
    "/Pages/meletes.html": "/ypiresies.html#iatreio",
    "/Pages/DentalOfficeMove.html": "/ypiresies.html#iatreio",
    "/Pages/Computerfix.html": "/ypiresies.html#ypologistes",
    "/Pages/Computerteach.html": "/ypiresies.html#ypologistes",
    "/Pages/software.html": "/ypiresies.html#ypologistes",
    "/Pages/aggelies.html": "/",
}

_cache = {}


def find_photo(name):
    for ext in (".webp", ".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"):
        if (PHOTOS / f"{name}{ext}").exists():
            return PHOTOS / f"{name}{ext}"
    return None


def photo(name, alt, cls="", fallback=""):
    src = find_photo(name)
    if not src:
        return f'<div class="{cls} empty" aria-hidden="true"><span>{fallback}</span></div>' if fallback else ""
    if name not in _cache:
        out = OUT / "assets" / "photos"
        out.mkdir(parents=True, exist_ok=True)
        try:
            from PIL import Image, ImageOps
            im = ImageOps.exif_transpose(Image.open(src))
            keep_alpha = im.mode in ("RGBA", "LA", "P") and src.suffix.lower() == ".png"
            im = im.convert("RGBA" if keep_alpha else "RGB")
            variants = []
            for w in (800, 1600):
                ww = min(w, im.width)
                if variants and ww == variants[-1][1]:
                    break
                hh = round(im.height * ww / im.width)
                fn = f"{name}-{ww}.webp"
                im.resize((ww, hh), Image.LANCZOS).save(out / fn, "WEBP", quality=82, method=6)
                variants.append((fn, ww, hh))
        except ImportError:
            shutil.copy(src, out / src.name)
            variants = [(src.name, None, None)]
        _cache[name] = variants
    v = _cache[name]
    fn, w, h = v[-1]
    attrs = f'src="assets/photos/{fn}" alt="{html.escape(alt)}"'
    if w:
        attrs += f' srcset="{", ".join(f"assets/photos/{f} {vw}w" for f, vw, _ in v)}" sizes="(max-width: 900px) 100vw, 50vw" width="{w}" height="{h}"'
    attrs += ' loading="eager" fetchpriority="high"' if name == "hero" else ' loading="lazy" decoding="async"'
    img = f"<img {attrs}>"
    return f'<div class="{cls}">{img}</div>' if cls else img


def href(slug):
    return "index.html" if slug == "index" else f"{slug}.html"


def canonical(slug):
    return f"{DOMAIN}/" if slug == "index" else f"{DOMAIN}/{slug}.html"


CONTACT = f"""<div class="contact reveal">
  <span class="ring" aria-hidden="true"></span>
  <div>
    <h2>Χάλασε κάτι; Πάρτε με τηλέφωνο.</h2>
    <p>Ή στείλτε μου βίντεο της βλάβης στο Viber. Συχνά τη λύνουμε μαζί, δωρεάν.</p>
  </div>
  <div>
    <a class="phone" href="tel:{TEL}">{PHONE}</a>
    <a class="mail" href="mailto:{EMAIL}">{EMAIL}</a>
    <div class="actions" data-hide-callbar>
      <a class="btn btn-light" href="tel:{TEL}">{{{{icon:phone}}}}Κλήση</a>
      <a class="btn btn-outline-light" href="{VIBER}">{{{{icon:video}}}}Viber</a>
    </div>
  </div>
</div>"""


def expand(body):
    body = body.replace("{{contact}}", CONTACT)

    def ph(m):
        p = m.group(1).split("|") + ["", "", ""]
        return photo(p[0], p[1], p[2], p[3])
    body = re.sub(r"\{\{photo:([^}]*)\}\}", ph, body)
    return re.sub(r"\{\{icon:(\w+)\}\}", lambda m: ICONS[m.group(1)], body)


def header(current):
    links = "\n".join(f'      <a href="{href(s)}"{" aria-current=\"page\"" if s == current else ""}>{label}</a>' for s, label in NAV)
    return f"""<a class="skip" href="#main">Μετάβαση στο περιεχόμενο</a>
<header class="site-header">
  <div class="wrap header-row">
    <a class="logo" href="index.html" aria-label="Υποστήριξη Οδοντιατρείου, αρχική">{ICONS["logo"]}<span>Υποστήριξη Οδοντιατρείου<small>dental-tech.gr · Ηράκλειο</small></span></a>
    <nav class="nav" id="nav" aria-label="Κύριο μενού">
{links}
    </nav>
    <div class="header-end">
      <a class="btn btn-brand" href="tel:{TEL}">{ICONS["phone"]}<span class="txt">{PHONE}</span></a>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="Μενού">{ICONS["menu"]}</button>
    </div>
  </div>
</header>"""


def footer():
    links = "".join(f'<a href="{href(s)}">{label}</a>' for s, label in NAV)
    return f"""<footer class="site-footer">
  <div class="wrap foot-grid">
    <span>© <span id="year">2026</span> Υποστήριξη Οδοντιατρείου · Γιώργος Πατεράκης · Ηράκλειο Κρήτης · Τιμές χωρίς ΦΠΑ</span>
    <nav class="foot-nav" aria-label="Σελίδες">{links}</nav>
  </div>
</footer>
<div class="callbar">
  <a class="btn btn-brand" href="tel:{TEL}">{ICONS["phone"]}Κλήση {PHONE}</a>
  <a class="btn btn-ghost" href="{VIBER}" aria-label="Viber">{ICONS["video"]}</a>
</div>"""


SWITCHER = """
<div class="swatches" role="group" aria-label="Δοκιμή χρώματος">
  <span class="name" id="pal-name">Χρώμα</span>
  {buttons}
</div>
<script>
(function () {{
  var root = document.documentElement, name = document.getElementById("pal-name");
  var btns = document.querySelectorAll(".swatches button");
  function apply(p) {{
    if (p === "navy") root.removeAttribute("data-palette"); else root.setAttribute("data-palette", p);
    btns.forEach(function (b) {{ var on = b.dataset.p === p; b.setAttribute("aria-pressed", on); if (on) name.textContent = b.title; }});
    try {{ localStorage.setItem("palette", p); }} catch (e) {{}}
  }}
  btns.forEach(function (b) {{ b.addEventListener("click", function () {{ apply(b.dataset.p); }}); }});
  var start = "navy", h = location.hash.slice(1), ok = {{}};
  btns.forEach(function (b) {{ ok[b.dataset.p] = 1; }});
  try {{ var saved = localStorage.getItem("palette"); if (ok[saved]) start = saved; }} catch (e) {{}}
  if (ok[h]) start = h;
  apply(start);
}})();
</script>"""


def switcher():
    buttons = "".join(f'<button type="button" data-p="{k}" title="{label}" aria-label="{label}" style="--c:{c}"></button>' for k, label, c in PALETTES)
    return SWITCHER.format(buttons=buttons)


def business_ld():
    return {
        "@context": "https://schema.org", "@type": "ProfessionalService",
        "name": "Υποστήριξη Οδοντιατρείου", "alternateName": "dental-tech.gr",
        "description": "Επισκευές και service σε όλα τα οδοντιατρικά μηχανήματα στο Ηράκλειο, 24/7.",
        "url": f"{DOMAIN}/", "telephone": TEL, "email": EMAIL,
        "founder": {"@type": "Person", "name": "Γιώργος Πατεράκης"},
        "areaServed": [{"@type": "City", "name": "Ηράκλειο"}, {"@type": "AdministrativeArea", "name": "Κρήτη"}],
        "address": {"@type": "PostalAddress", "addressLocality": "Ηράκλειο", "addressRegion": "Κρήτη", "addressCountry": "GR"},
        "openingHoursSpecification": {"@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "00:00", "closes": "23:59"},
    }


def parse(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"\s*<!--(.*?)-->\s*", text, re.S)
    meta = {}
    for line in m.group(1).strip().splitlines():
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip()
    return meta, text[m.end():]


def render(slug, meta, body, trial, wrap):
    title, desc = html.escape(meta["title"]), html.escape(meta["description"])
    extra = ""
    if trial:
        extra += '\n<meta name="robots" content="noindex">'
    else:
        if slug == "index":
            extra += f'\n<meta name="google-site-verification" content="{GOOGLE_VERIFICATION}">'
            extra += f'\n<script type="application/ld+json">{json.dumps(business_ld(), ensure_ascii=False)}</script>'
        if PALETTE != "navy":
            extra += f'\n<script>document.documentElement.setAttribute("data-palette", "{PALETTE}")</script>'
    if find_photo("hero") and "hero" in _cache:
        extra += f'\n<meta property="og:image" content="{DOMAIN}/assets/photos/{_cache["hero"][-1][0]}">'
    inner = f"""<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical(slug)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="el_GR">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical(slug)}">
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/manrope-greek-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/style.css">{extra}
{header(meta.get("nav", slug))}
<main id="main">
{body}
</main>
{footer()}
<script src="assets/site.js" defer></script>{switcher() if trial else ""}"""
    if not wrap:
        return inner + "\n"
    return f"""<!doctype html>
<html lang="el">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
</head>
<body>
{inner}
</body>
</html>
"""


def build(out, preview=False, pages=False):
    """preview: copy for the Claude preview (homepage without document wrapper).
    pages: shareable GitHub Pages copy. Both get the colour switcher and noindex."""
    global OUT
    OUT = out
    _cache.clear()
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(SRC / "assets", out / "assets")
    trial = preview or pages
    slugs = []
    for path in sorted((SRC / "pages").glob("*.html")):
        slug = path.stem
        meta, body = parse(path)
        doc = render(slug, meta, expand(body), trial, wrap=not (preview and slug == "index"))
        (out / f"{slug}.html").write_text(doc, encoding="utf-8")
        slugs.append(slug)

    if trial:
        (out / ".nojekyll").write_text("", encoding="utf-8")
        (out / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
        return slugs
    lines = ["# 301 redirects from the old site's pages", "RewriteEngine On"]
    for old, new in REDIRECTS.items():
        target, _, frag = new.partition("#")
        lines.append(f"RewriteRule ^{re.escape(old.lstrip('/'))}$ {target}{'#' + frag if frag else ''} [R=301,L,NE]")
    lines += ["", "ErrorDocument 404 /404.html", "",
              "<IfModule mod_expires.c>", "  ExpiresActive On",
              '  ExpiresByType font/woff2 "access plus 1 year"',
              '  ExpiresByType image/webp "access plus 1 year"',
              '  ExpiresByType text/css "access plus 1 month"',
              "</IfModule>", ""]
    (out / ".htaccess").write_text("\n".join(lines), encoding="utf-8")
    (out / "_redirects").write_text("\n".join(f"{o} {n} 301" for o, n in REDIRECTS.items()) + "\n", encoding="utf-8")
    urls = "\n".join(f"  <url><loc>{canonical(s)}</loc></url>" for s in slugs if s != "404")
    (out / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n', encoding="utf-8")
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n", encoding="utf-8")
    return slugs


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--preview":
        build(Path(sys.argv[2]), preview=True)
    elif len(sys.argv) > 2 and sys.argv[1] == "--pages":
        build(Path(sys.argv[2]), pages=True)
    else:
        slugs = build(ROOT / "site")
        print(f"Built {len(slugs)} pages into {ROOT / 'site'}")
