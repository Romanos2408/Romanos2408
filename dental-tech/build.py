#!/usr/bin/env python3
"""Builds the static site for dental-tech.gr.

Each file in src/pages/ starts with a header comment:

    <!--
    title: Page <title>
    description: Meta description
    nav: slug of the menu item to highlight
    h1: Page heading (inner pages only)
    lead: Sentence under the heading (inner pages only)
    -->

The rest of the file is the page body. Run `python3 build.py`; the finished
site lands in site/ and can be uploaded as-is to any web host.
"""
import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "site"

DOMAIN = "https://www.dental-tech.gr"
PHONE = "6944 648 748"
PHONE_TEL = "+306944648748"
EMAIL = "tech@dental-tech.gr"
VIBER = "viber://chat?number=%2B306944648748"
GOOGLE_VERIFICATION = "9U862btudvMgP9ZRfHiI7--urNMIV4rYU9bUqNHhfRM"

NAV = [
    ("episkeves", "Επισκευές & service"),
    ("xeirolaves", "Χειρολαβές"),
    ("autokaustoi", "Αυτόκαυστοι"),
    ("aktinografia", "Ψηφιακή ακτινογραφία"),
    ("eksoplismos", "Εξοπλισμός"),
    ("meletes", "Μελέτη & μεταφορά"),
    ("ypologistes", "Υπολογιστές"),
    ("aggelies", "Αγγελίες"),
    ("about", "Ποιοι είμαστε"),
    ("contact", "Επικοινωνία"),
]
SERVICES = NAV[:7]
# Shorter labels for the top menu so it fits on one line.
SHORT = {"episkeves": "Επισκευές", "aktinografia": "Ακτινογραφία", "meletes": "Μελέτες"}

ICON_PHONE = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>'
ICON_VIDEO = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="14" height="12" rx="2"/><path d="m16 10 6-3v10l-6-3z"/></svg>'


def href(slug):
    return "index.html" if slug == "index" else f"{slug}.html"


def canonical(slug):
    return f"{DOMAIN}/" if slug == "index" else f"{DOMAIN}/{slug}.html"


def parse(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"\s*<!--(.*?)-->\s*", text, re.S)
    meta = {}
    for line in m.group(1).strip().splitlines():
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    return meta, text[m.end():]


def call_button(extra=""):
    return (f'<a class="btn btn-call{extra}" href="tel:{PHONE_TEL}">{ICON_PHONE}'
            f'<span>Κλήση <span class="num">{PHONE}</span></span></a>')


def header(current):
    items = "\n".join(
        f'<li><a href="{href(s)}"{" aria-current=\"page\"" if s == current else ""}>{SHORT.get(s, label)}</a></li>'
        for s, label in NAV
    )
    return f"""<a class="skip" href="#main">Μετάβαση στο περιεχόμενο</a>
<header class="site-header">
  <div class="wrap">
    <div class="header-row">
      <a class="brand" href="index.html" aria-label="Υποστήριξη Οδοντιατρείου, αρχική σελίδα">
        <span class="brand-name">Υποστήριξη Οδοντιατρείου<b>.</b></span>
        <span class="brand-sub">dental-tech.gr · Ηράκλειο Κρήτης</span>
      </a>
      <div class="header-actions">
        {call_button()}
        <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="main-nav">Μενού</button>
      </div>
    </div>
    <nav class="main-nav" id="main-nav" aria-label="Κύριο μενού">
      <ul>
{items}
      </ul>
    </nav>
  </div>
</header>"""


def footer():
    services = "\n".join(f'<li><a href="{href(s)}">{label}</a></li>' for s, label in SERVICES)
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="stack">
        <h2>Υποστήριξη Οδοντιατρείου</h2>
        <p>Τεχνική υποστήριξη για οδοντιάτρους στο Ηράκλειο και σε όλη την Κρήτη: επισκευές, service, εξοπλισμός, ψηφιακή ακτινογραφία και υπολογιστές.</p>
        <p><a href="tel:{PHONE_TEL}" class="mono">{PHONE}</a><br><a href="mailto:{EMAIL}" class="mono">{EMAIL}</a></p>
      </div>
      <div>
        <h2>Υπηρεσίες</h2>
        <ul>
{services}
        </ul>
      </div>
      <div>
        <h2>Ακόμα</h2>
        <ul>
          <li><a href="aggelies.html">Αγγελίες μεταχειρισμένων</a></li>
          <li><a href="about.html">Ποιοι είμαστε</a></li>
          <li><a href="contact.html#video">Βοήθεια με βιντεοκλήση</a></li>
          <li><a href="contact.html">Επικοινωνία</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-legal">
      <span>© <span id="year">2026</span> Υποστήριξη Οδοντιατρείου · Γιώργος Πατεράκης</span>
      <span>Οι τιμές δεν περιλαμβάνουν ΦΠΑ, εκτός αν αναφέρεται διαφορετικά.</span>
    </div>
  </div>
</footer>
<div class="callbar">
  {call_button()}
  <a class="btn btn-ghost" href="{VIBER}" aria-label="Βιντεοκλήση Viber">{ICON_VIDEO}<span>Viber</span></a>
</div>"""


def aside(current):
    links = "\n".join(
        f'<li><a href="{href(s)}"{" aria-current=\"page\"" if s == current else ""}>{label}</a></li>'
        for s, label in SERVICES
    )
    return f"""<aside class="aside" aria-label="Επικοινωνία και υπηρεσίες">
  <div class="aside-card">
    <span class="eyebrow">Χρειάζεστε βοήθεια τώρα;</span>
    <span class="phone">{PHONE}</span>
    <p>Το τηλέφωνο είναι ο πιο γρήγορος τρόπος. Καλέστε οποτεδήποτε, δεν ενοχλείτε.</p>
    {call_button()}
    <a class="btn btn-ghost" href="contact.html#video">{ICON_VIDEO}<span>Βοήθεια με βιντεοκλήση</span></a>
  </div>
  <div>
    <span class="eyebrow">Υπηρεσίες</span>
    <ul class="aside-nav">
{links}
    </ul>
  </div>
</aside>"""


def json_ld():
    data = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": "Υποστήριξη Οδοντιατρείου",
        "alternateName": "dental-tech.gr",
        "description": "Επισκευή και service οδοντιατρικών μηχανημάτων, χειρολαβών, αυτόκαυστων κλιβάνων και ψηφιακής ακτινογραφίας στο Ηράκλειο Κρήτης.",
        "url": f"{DOMAIN}/",
        "telephone": PHONE_TEL,
        "email": EMAIL,
        "founder": {"@type": "Person", "name": "Γιώργος Πατεράκης"},
        "areaServed": [{"@type": "City", "name": "Ηράκλειο"}, {"@type": "AdministrativeArea", "name": "Κρήτη"}],
        "address": {"@type": "PostalAddress", "addressLocality": "Ηράκλειο", "addressRegion": "Κρήτη", "addressCountry": "GR"},
        "knowsLanguage": "el",
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def head(meta, slug):
    title = html.escape(meta["title"])
    desc = html.escape(meta["description"])
    extra = ""
    if slug == "index":
        extra = f'\n<meta name="google-site-verification" content="{GOOGLE_VERIFICATION}">\n{json_ld()}'
    return f"""<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical(slug)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="el_GR">
<meta property="og:site_name" content="Υποστήριξη Οδοντιατρείου">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical(slug)}">
<meta name="theme-color" content="#12222b">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/commissioner-greek-full-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/style.css">{extra}"""


def render(meta, body, slug, wrap_document=True):
    if slug == "index" or meta.get("layout") == "bare":
        main = body
    else:
        crumbs = (f'<nav class="crumbs" aria-label="Διαδρομή"><a href="index.html">Αρχική</a> / '
                  f'{html.escape(meta["h1"])}</nav>')
        lead = f'<p class="lead">{meta["lead"]}</p>' if meta.get("lead") else ""
        main = f"""<div class="page-hero">
  <div class="wrap">
    {crumbs}
    <h1>{meta["h1"]}</h1>
    {lead}
  </div>
</div>
<div class="wrap page-body">
  <article class="prose">
{body}
  </article>
  {aside(slug)}
</div>"""
    inner = f"""{head(meta, slug)}
{header(meta.get("nav", slug))}
<main id="main">
{main}
</main>
{footer()}
<script src="assets/site.js" defer></script>"""
    if not wrap_document:
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


# Old URL -> new URL, so Google rankings and old bookmarks carry over.
REDIRECTS = {
    "/Pages/index.html": "/",
    "/Pages/about.html": "/about.html",
    "/Pages/contact.html": "/contact.html",
    "/Pages/remoterepair.html": "/contact.html#video",
    "/Pages/parts-equipment-repair.html": "/episkeves.html",
    "/Pages/anakataskeyes.html": "/episkeves.html#anakataskeues",
    "/Pages/handpiece-repair.html": "/xeirolaves.html",
    "/Pages/sterilizer-repair.html": "/autokaustoi.html",
    "/Pages/DigiRadiography.html": "/aktinografia.html",
    "/Pages/dental-equipment.html": "/eksoplismos.html",
    "/Pages/dental-chairs.html": "/eksoplismos.html#mixanimata",
    "/Pages/lasers.html": "/eksoplismos.html#laser",
    "/Pages/arch_studies.html": "/meletes.html",
    "/Pages/meletes.html": "/meletes.html",
    "/Pages/DentalOfficeMove.html": "/meletes.html#metafora",
    "/Pages/Computerfix.html": "/ypologistes.html",
    "/Pages/Computerteach.html": "/ypologistes.html#ekmathisi",
    "/Pages/software.html": "/ypologistes.html#logismiko",
    "/Pages/aggelies.html": "/aggelies.html",
}


def write_redirects():
    lines = ["# Apache: 301 redirects from the old site's URLs", "RewriteEngine On"]
    for old, new in REDIRECTS.items():
        target, _, frag = new.partition("#")
        lines.append(f"RewriteRule ^{re.escape(old.lstrip('/'))}$ {target}{'#' + frag if frag else ''} [R=301,L,NE]")
    lines += ["", "ErrorDocument 404 /404.html", "",
              "<IfModule mod_expires.c>", "  ExpiresActive On",
              '  ExpiresByType font/woff2 "access plus 1 year"',
              '  ExpiresByType text/css "access plus 1 month"',
              '  ExpiresByType application/javascript "access plus 1 month"',
              "</IfModule>", ""]
    (OUT / ".htaccess").write_text("\n".join(lines), encoding="utf-8")
    # Netlify / Cloudflare Pages format
    (OUT / "_redirects").write_text(
        "\n".join(f"{old} {new} 301" for old, new in REDIRECTS.items()) + "\n", encoding="utf-8")


def write_sitemap(slugs):
    urls = "\n".join(f"  <url><loc>{canonical(s)}</loc></url>" for s in slugs if s != "404")
    (OUT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n',
        encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n", encoding="utf-8")


def build(out=OUT, preview=False):
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(SRC / "assets", out / "assets")
    slugs = []
    for path in sorted((SRC / "pages").glob("*.html")):
        slug = path.stem
        meta, body = parse(path)
        # In preview mode the homepage is published without its document
        # wrapper, because the preview host adds one.
        doc = render(meta, body, slug, wrap_document=not (preview and slug == "index"))
        (out / f"{slug}.html").write_text(doc, encoding="utf-8")
        slugs.append(slug)
    return slugs


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2 and sys.argv[1] == "--preview":
        build(Path(sys.argv[2]), preview=True)
    else:
        slugs = build()
        write_redirects()
        write_sitemap(slugs)
        print(f"Built {len(slugs)} pages into {OUT}")
