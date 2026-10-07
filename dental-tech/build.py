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
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/manrope-greek-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
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


# The colour the real site ships with. Options: green, blue, navy, charcoal, teal, violet.
PALETTE = "green"
PALETTES = [("green", "Πράσινο", "#0d6b56"), ("blue", "Μπλε", "#1f5fd1"), ("navy", "Navy", "#1b2f5e"),
            ("charcoal", "Ανθρακί", "#2b2e33"), ("teal", "Πετρόλ", "#0b6b7a"), ("violet", "Μωβ", "#5a3fb3")]

SWITCHER_HTML = """
<div class="swatches" role="group" aria-label="Δοκιμή χρώματος">
  <span class="name" id="pal-name">Χρώμα</span>
  {buttons}
</div>
<script>
(function () {{
  var root = document.documentElement, name = document.getElementById("pal-name");
  var btns = document.querySelectorAll(".swatches button");
  function apply(p) {{
    if (p === "green") root.removeAttribute("data-palette"); else root.setAttribute("data-palette", p);
    btns.forEach(function (b) {{ var on = b.dataset.p === p; b.setAttribute("aria-pressed", on); if (on) name.textContent = b.title; }});
    try {{ localStorage.setItem("palette", p); }} catch (e) {{}}
  }}
  btns.forEach(function (b) {{ b.addEventListener("click", function () {{ apply(b.dataset.p); }}); }});
  var start = "green", h = location.hash.slice(1);
  try {{ start = localStorage.getItem("palette") || start; }} catch (e) {{}}
  btns.forEach(function (b) {{ if (b.dataset.p === h) start = h; }});
  apply(start);
}})();
</script>"""


def switcher():
    buttons = "".join(f'<button type="button" data-p="{k}" title="{label}" aria-label="{label}" style="--c:{c}"></button>'
                      for k, label, c in PALETTES)
    return SWITCHER_HTML.format(buttons=buttons)


def build(out, preview=False, pages=False):
    """preview: artifact copy (no document wrapper). pages: shareable GitHub Pages copy.
    Both get the colour switcher and are hidden from search engines."""
    global OUT
    OUT = out
    _cache.clear()
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(SRC / "assets", out / "assets")
    trial = preview or pages

    body = expand((SRC / "index.html").read_text(encoding="utf-8"))
    extra = (f'\n<meta name="google-site-verification" content="{GOOGLE_VERIFICATION}">'
             f'\n<script type="application/ld+json">{json.dumps(business_ld(), ensure_ascii=False)}</script>')
    if find_photo("hero"):
        extra += f'\n<meta property="og:image" content="{DOMAIN}/assets/photos/{_cache["hero"][-1][0]}">'
    if trial:
        extra = '\n<meta name="robots" content="noindex">'
    elif PALETTE != "green":
        extra += f'\n<script>document.documentElement.setAttribute("data-palette", "{PALETTE}")</script>'
    page = f'{head(TITLE, DESCRIPTION, DOMAIN + "/", extra)}\n{body}\n<script src="assets/site.js" defer></script>'
    if trial:
        page += switcher()
    (out / "index.html").write_text(document(page, wrap=not preview), encoding="utf-8")

    notfound = f"""{head("Η σελίδα δεν βρέθηκε · Υποστήριξη Οδοντιατρείου", "Η σελίδα δεν υπάρχει.", DOMAIN + "/404.html")}
<main style="min-height:100vh;display:grid;place-items:center;text-align:center;padding:2rem">
  <div style="display:grid;gap:1.2rem;justify-items:center">
    <span class="kicker">404</span>
    <h1>Αυτή η σελίδα δεν υπάρχει.</h1>
    <a class="btn btn-brand" href="index.html">Στην αρχική</a>
  </div>
</main>"""
    (out / "404.html").write_text(document(notfound, wrap=True), encoding="utf-8")

    if pages:
        (out / ".nojekyll").write_text("", encoding="utf-8")
        (out / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    if not trial:
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
    elif len(sys.argv) > 2 and sys.argv[1] == "--pages":
        build(Path(sys.argv[2]), pages=True)
    else:
        build(ROOT / "site")
        print(f"Built into {ROOT / 'site'}")
