# dental-tech.gr

A one-page site for Υποστήριξη Οδοντιατρείου (Γιώργος Πατεράκης, Heraklion).
It's plain static HTML, so there's nothing to update or patch.

- `src/index.html` holds the page text. Edit it here.
- `src/photos/` holds the photos. See `PHOTOS.md` for names and format.
- `src/assets/` holds the styles, the marble texture, the script and self-hosted fonts.
- `site/` is the finished website. Upload its contents.

## Change something

1. Edit `src/index.html` or add photos.
2. Run `python3 build.py`. `pip install pillow` once lets the build resize photos to fast WebP files.
3. Upload the contents of `site/`.

## Going live

- **Current host (Apache):** upload everything in `site/`, including `.htaccess`. It sends every old `/Pages/*.html` address to the right part of the new page, so Google rankings carry over. Then delete the old `Pages`, `images` and `Documents_etc` folders.
- **Netlify or Cloudflare Pages (free):** deploy the `site/` folder. `_redirects` handles the old addresses.
- In Google Search Console, submit `https://www.dental-tech.gr/sitemap.xml`. The verification tag is already in the page.

## Check with Giorgos

- The "About" text is written in his voice, including the joke about telescopes and dental chairs. Make sure he's happy with it.
- The 12-month warranty and the KAVO prices (€280 labour, €120 parts, without VAT) are still current.
