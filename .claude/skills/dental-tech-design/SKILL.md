---
name: dental-tech-design
description: Art direction, copy voice and build rules for dental-tech.gr, the website of Γιώργος Πατεράκης (Υποστήριξη Οδοντιατρείου), a friendly, 24/7 dental-equipment technician in Heraklion. Use this skill for ANY design, redesign, layout, copy, photo or styling work on dental-tech.gr or the dental-tech/ folder, even small tweaks ("change the hero", "add a section", "new colors", "add his photos", "make it look better"). It records what the user chose and everything they already rejected, so the site doesn't drift.
---

# dental-tech.gr design skill

The client is one person: Giorgos, who repairs dental equipment for dentists in Heraklion, any hour of any day. He's a physicist who also runs the telescope at Skinakas Observatory. He is friendly and always helping.

## The direction the user chose: a clean, modern dental brand

Think of the websites of the big dental companies (Straumann, Dentsply Sirona, W&H): bright white, soft colour, rounded shapes, big friendly photos of people, and very little text. The site should look as trustworthy as the equipment he repairs. The personal warmth comes from **his photos and a few sentences in his voice**, not from decoration or jokes in the layout.

The user rejected nine directions before choosing this one. Read `references/anti-patterns.md` before changing the look, so none of them come back.

## Palette

The live values are in `dental-tech/src/assets/style.css`:
- White `#ffffff` page, soft sage surfaces `#f2f6f4`, mint tint `#dcefe6`
- Ink `#0f201b`, muted text `#56655f`, lines `#e1e8e5`
- One brand colour, a deep clinical green `#0d6b56`, plus a darker panel colour `#0a3d32`
- Status green `#22a06b`, used only for the "Διαθέσιμος τώρα" dot
- Dark mode is the same layout on deep green-black `#0d1513`, with a lighter brand green `#4fc6a3`

Don't add a second accent colour. Calm comes from restraint.

**The colour isn't final.** Giorgos chooses it. Six palettes exist as `[data-palette]` blocks in `style.css`: green (the default), blue, navy, charcoal, teal and violet, each with a dark-mode version. Preview builds (`--preview`, `--pages`) show a colour switcher at the bottom left, and `#blue`, `#navy` and so on in the URL pre-select one. The production colour is `PALETTE` in `build.py`. When he picks, set it there and drop the other palettes if you like. Anything new must use the tokens (`--brand`, `--brand-deep`, `--logo`, `--mint`…) so every palette keeps working.

## Type

Manrope only (it has Greek), self-hosted from `@fontsource-variable/manrope`. Headings are 750 weight with tight letter-spacing (-0.025em); body text is 400 at about 17px.

## Shape and components

- Rounded corners: 28px for big tiles and photos, 20px for small cards, pill-shaped buttons.
- **Hero:** the "Διαθέσιμος τώρα · 24/7" status pill, a headline, a single sentence, a call button and a Viber button. On the right, a big rounded photo of Giorgos with one floating white card ("Δανεικός εξοπλισμός").
- **Three promises:** soft sage cards with a line icon: 24/7, free assessment, warranty up to 12 months.
- **Services:** a bento grid. One big photo tile (dental chairs) plus small icon tiles. One line of text each.
- **About:** a rounded portrait beside "Γεια σας, είμαι ο Γιώργος." Two short paragraphs and brand chips.
- **KAVO offer:** a mint panel with two white price cards (€280 labour, €120 parts, maximum, without VAT).
- **Contact:** a deep green panel with a big white phone number and buttons.
- **Phones:** a call bar at the bottom.
- Icons are simple 1.8px line icons drawn inline in `build.py` (`ICONS`). Keep new ones in the same style.

## Voice

Greek, polite plural (εσείς/σας) to dentists, but first person and warm: «Απαντάω εγώ, ο Γιώργος», «Πάρτε με τηλέφωνο, όποια ώρα κι αν είναι. Δεν ενοχλείτε.» Short sentences. No marketing phrases («λύσεις», «υψηλής ποιότητας», «η εταιρεία μας», «Γιατί να μας επιλέξετε»). Keep the whole page to about 150 words of body text.

Use only the facts in `references/facts.md`. Never invent years in business, client numbers, reviews or awards.

## Photos (the most important missing piece)

The design depends on real, bright, friendly photos of Giorgos at work: smiling, in clinics, with equipment. Never use a stock person as him. Equipment-only shots may be free stock (Unsplash, Pexels; not "Unsplash+"). Until a photo exists, the build shows a soft mint placeholder with a camera icon. `dental-tech/PHOTOS.md` lists the file names: `hero`, `giorgos`, `s-mixanimata`.

## Motion

Subtle and modern: content rises in on load, sections fade up as they scroll in, a slight parallax on the hero photo, cards lift 4px on hover, and the status dot pulses. Everything is off under `prefers-reduced-motion`.

## Build

`dental-tech/src/index.html` holds the page; `{{photo:name|alt|class|fallback}}` and `{{icon:name}}` are tokens. `python3 build.py` builds `site/`, including redirects from the old site, the sitemap and the Search Console tag. Check with Playwright (Chromium at `/opt/pw-browsers/chromium`) at 1360px and 390px, light and dark, for overflow and Greek fonts.

## Before handing over

1. Does it look like a serious dental-equipment brand at first glance?
2. Is Giorgos (photo and voice) the warm part, rather than decoration?
3. Is the phone number reachable in one tap on a phone?
4. Did anything from `references/anti-patterns.md` come back?
