# dental-tech.gr — new site

A rebuild of www.dental-tech.gr (Υποστήριξη Οδοντιατρείου, Γιώργος Πατεράκης, Heraklion).
Plain static HTML: no WordPress, no database, nothing to update or patch.

## Folders

- `src/pages/` holds the text of each page. Edit these.
- `src/assets/` holds the stylesheet, script, favicon and self-hosted fonts.
- `site/` is the finished website. Upload its contents to the web host.

## Changing text

1. Edit the page in `src/pages/`. The header comment at the top sets the page title, the Google description and the heading.
2. Run `python3 build.py` (Python 3, no packages needed).
3. Upload the contents of `site/`.

## Going live

- **Same host as now (Apache):** upload everything in `site/`, including `.htaccess`. It redirects every old `/Pages/*.html` address to its new page, so Google rankings and old bookmarks keep working. Then delete the old `/Pages`, `/images` and `/Documents_etc` folders.
- **Netlify or Cloudflare Pages (free):** deploy the `site/` folder. `_redirects` handles the old addresses.
- In Google Search Console, submit `https://www.dental-tech.gr/sitemap.xml`. The verification tag is already in the homepage.

## Still to do (search for `TODO` in `src/pages/`)

- Confirm prices and whether they include VAT. The KAVO 68LH/68LDN head is listed at €110 for a replacement and €180 for a new head in the classifieds.
- Confirm which classifieds are still available.
- Name of the dental software he recommends.
- Copy `Documents_etc/CDR Talking About Resolution.pdf` from the old site to `site/docs/cdr-talking-about-resolution.pdf`.
- Real photos of his work and his logo, if he wants them on the site.
