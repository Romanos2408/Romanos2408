#!/usr/bin/env python3
"""Builds dental-tech.gr: one page, src/index.html, into site/.

In src/index.html:
  {{photo:name|alt|class|fallback}}  inserts src/photos/name.(jpg|png|webp).
      If the photo is missing and a fallback is given, a marble block
      showing the fallback text is used instead.
  {{icon:phone}} / {{icon:video}}  inline icons.

Run `python3 build.py`, then upload the contents of site/.
`pip install pillow` lets the build resize photos to fast WebP files.
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

DOMAIN = "https://www.dental-tech.gr"
TITLE = "Υποστήριξη Οδοντιατρείου · Επισκευές οδοντιατρικών μηχανημάτων Ηράκλειο, 24/7"
DESCRIPTION = ("Επισκευές και service σε όλα τα οδοντιατρικά μηχανήματα στο Ηράκλειο, 24/7. "
               "Δωρεάν εκτίμηση, δανεικός εξοπλισμός, εγγύηση. Γιώργος Πατεράκης, 6944 648 748.")
GOOGLE_VERIFICATION = "9U862btudvMgP9ZRfHiI7--urNMIV4rYU9bUqNHhfRM"

ICONS = {
    "phone": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>',
    "video": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="14" height="12" rx="2"/><path d="m16 10 6-3v10l-6-3z"/></svg>',
}

# Every page of the old site now lands on the matching part of the new one.
REDIRECTS = {
    "/index.html": "/",
    "/Pages/index.html": "/",
    "/Pages/about.html": "/#giorgos",
    "/Pages/contact.html": "/#epikoinonia",
    "/Pages/remoterepair.html": "/#epikoinonia",
    "/Pages/parts-equipment-repair.html": "/#ypiresies",
    "/Pages/anakataskeyes.html": "/#ypiresies",
    "/Pages/handpiece-repair.html": "/#ypiresies",
    "/Pages/sterilizer-repair.html": "/#ypiresies",
    "/Pages/DigiRadiography.html": "/#ypiresies",
    "/Pages/dental-equipment.html": "/#ypiresies",
    "/Pages/dental-chairs.html": "/#ypiresies",
    "/Pages/lasers.html": "/#ypiresies",
    "/Pages/arch_studies.html": "/#ypiresies",
    "/Pages/meletes.html": "/#ypiresies",
    "/Pages/DentalOfficeMove.html": "/#ypiresies",
    "/Pages/Computerfix.html": "/#ypiresies",
    "/Pages/Computerteach.html": "/#ypiresies",
    "/Pages/software.html": "/#ypiresies",
    "/Pages/aggelies.html": "/",
}

OUT = ROOT / "site"
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


def expand(body):
    def ph(m):
        p = m.group(1).split("|") + ["", "", ""]
        return photo(p[0], p[1], p[2], p[3])
    body = re.sub(r"\{\{photo:([^}]*)\}\}", ph, body)
    return re.sub(r"\{\{icon:(\w+)\}\}", lambda m: ICONS[m.group(1)], body)


def head(title, description, canonical, extra=""):
    return f"""<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:locale" content="el_GR">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{canonical}">
<meta name="theme-color" content="#f6f5f1">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/noto-serif-display-greek-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/style.css">{extra}"""


def document(inner, wrap):
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


def business_ld():
    return {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": "Υποστήριξη Οδοντιατρείου",
        "alternateName": "dental-tech.gr",
        "description": DESCRIPTION,
        "url": f"{DOMAIN}/",
        "telephone": "+306944648748",
        "email": "tech@dental-tech.gr",
        "founder": {"@type": "Person", "name": "Γιώργος Πατεράκης"},
        "areaServed": [{"@type": "City", "name": "Ηράκλειο"}, {"@type": "AdministrativeArea", "name": "Κρήτη"}],
        "address": {"@type": "PostalAddress", "addressLocality": "Ηράκλειο", "addressRegion": "Κρήτη", "addressCountry": "GR"},
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "00:00", "closes": "23:59",
        },
    }


def build(out, preview=False):
    global OUT
    OUT = out
    _cache.clear()
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(SRC / "assets", out / "assets")

    body = expand((SRC / "index.html").read_text(encoding="utf-8"))
    extra = (f'\n<meta name="google-site-verification" content="{GOOGLE_VERIFICATION}">'
             f'\n<script type="application/ld+json">{json.dumps(business_ld(), ensure_ascii=False)}</script>')
    if find_photo("hero"):
        extra += f'\n<meta property="og:image" content="{DOMAIN}/assets/photos/{_cache["hero"][-1][0]}">'
    page = f'{head(TITLE, DESCRIPTION, DOMAIN + "/", extra)}\n{body}\n<script src="assets/site.js" defer></script>'
    (out / "index.html").write_text(document(page, wrap=not preview), encoding="utf-8")

    notfound = f"""{head("Η σελίδα δεν βρέθηκε · Υποστήριξη Οδοντιατρείου", "Η σελίδα δεν υπάρχει.", DOMAIN + "/404.html")}
<main class="marble" style="min-height:100vh;display:grid;place-items:center;text-align:center;padding:2rem">
  <div style="display:grid;gap:1.2rem;justify-items:center">
    <span class="label">404</span>
    <h1>Αυτή η σελίδα <em>δεν υπάρχει.</em></h1>
    <a class="btn btn-dark" href="index.html">Στην αρχική</a>
  </div>
</main>"""
    (out / "404.html").write_text(document(notfound, wrap=True), encoding="utf-8")

    if not preview:
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
        (out / "sitemap.xml").write_text(
            f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>{DOMAIN}/</loc></url>\n</urlset>\n',
            encoding="utf-8")
        (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n", encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--preview":
        build(Path(sys.argv[2]), preview=True)
    else:
        build(ROOT / "site")
        print(f"Built into {ROOT / 'site'}")
