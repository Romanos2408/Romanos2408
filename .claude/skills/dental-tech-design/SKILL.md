---
name: dental-tech-design
description: Art direction, copy voice and build rules for dental-tech.gr, the website of Γιώργος Πατεράκης (Υποστήριξη Οδοντιατρείου), a friendly, 24/7 dental-equipment technician in Heraklion. Use this skill for ANY design, redesign, layout, copy, photo or styling work on dental-tech.gr or the dental-tech/ folder, even small tweaks ("change the hero", "add a section", "new colors", "add his photos", "make it look better"). It records what the user chose and everything they already rejected, so the site doesn't drift.
---

# dental-tech.gr design skill

The client is one person: Giorgos, who repairs dental equipment for dentists in Heraklion, any hour of any day. He's a physicist who also runs the telescope at Skinakas Observatory. He is friendly and always helping.

## The direction the user chose: a clean, modern dental brand

Think of the websites of the big dental companies (Straumann, Dentsply Sirona, W&H): bright white, soft colour, rounded shapes, big friendly photos of people, and very little text. The site should look as trustworthy as the equipment he repairs. The personal warmth comes from **his photos and a few sentences in his voice**, not from decoration or jokes in the layout.

The user rejected nine directions before choosing this one. Read `references/anti-patterns.md` before changing the look, so none of them come back.

## Palette (light only)

There is no dark mode; the user chose a light-only site. Three colour options remain, and Giorgos picks one:
- **Navy** (the default): brand `#1b2f5e`, deep panel `#0e1a36`, surfaces `#f3f4f8` and `#e1e5f0`, ink `#10162a`
- **Charcoal (Ανθρακί):** brand `#2b2e33`, deep panel `#17191c`
- **Teal (Πετρόλ):** brand `#0b6b7a`, deep panel `#083d46`

The values live in `src/assets/style.css` (`:root` for navy, `[data-palette]` blocks for the others). The production colour is `PALETTE` in `build.py`. Preview builds (`--preview`, `--pages`) show a three-dot colour switcher; `#charcoal` or `#teal` in the URL pre-selects one. Green, blue and violet were dropped. Status green `#22a06b` is used only for the "Διαθέσιμος τώρα" dot. Everything new must use the tokens (`--brand`, `--brand-deep`, `--soft`, `--mint`, `--logo`) so all three palettes keep working. Don't add a second accent.

## Type

Manrope only (it has Greek), self-hosted from `@fontsource-variable/manrope`. Headings are 750 weight with tight letter-spacing (-0.025em); body text is 400 at about 17px.

## Pages

Four short pages plus a 404, all in `src/pages/`:
- **index (Αρχική):** hero, three promises, a services bento linking to the services page, an about teaser, the KAVO offer and the contact panel
- **ypiresies (Υπηρεσίες):** jump links, then one row per service (photo, icon, title, one sentence, three ticks), alternating sides. Anchors: `#edres #xeirolaves #autokaustoi #aktinografia #iatreio #ypologistes #eksoplismos`
- **giorgos (Ποιος είμαι):** portrait, his story in three short paragraphs, fact cards (training, partners, the 2013 Social Dental Clinic) and a three-photo gallery
- **epikoinonia (Επικοινωνία):** three ways to reach him (phone highlighted), the three video-help steps (`#video`), and "what to have ready" / "where I work" panels

Header and footer are generated in `build.py`. `{{contact}}` inserts the dark call panel.

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

Greek, polite plural (εσείς/σας) to dentists, but first person and warm: «Απαντάω εγώ, ο Γιώργος», «Πάρτε με τηλέφωνο, όποια ώρα κι αν είναι. Δεν ενοχλείτε.» Short sentences. No marketing phrases («λύσεις», «υψηλής ποιότητας», «η εταιρεία μας», «Γιατί να μας επιλέξετε»). Keep each page short: about 150 words of body text, and services in one sentence plus three ticks.

Use only the facts in `references/facts.md`. Never invent years in business, client numbers, reviews or awards.

## Photos (the most important missing piece)

The design depends on real, bright, friendly photos of Giorgos at work: smiling, in clinics, with equipment. Never use a stock person as him. Equipment-only shots may be free stock (Unsplash, Pexels; not "Unsplash+"). Until a photo exists, the build shows a soft mint placeholder with a camera icon. `dental-tech/PHOTOS.md` lists every file name.

## Motion

Subtle and modern: content rises in on load, sections fade up as they scroll in, a slight parallax on the hero photo, cards lift 4px on hover, and the status dot pulses. Everything is off under `prefers-reduced-motion`.

## Build

Pages are in `dental-tech/src/pages/`; `{{photo:name|alt|class|fallback}}`, `{{icon:name}}` and `{{contact}}` are tokens. `python3 build.py` builds `site/`, including redirects from the old site, the sitemap and the Search Console tag. Check with Playwright (Chromium at `/opt/pw-browsers/chromium`) at 1360px and 390px for overflow and Greek fonts.

## Before handing over

1. Does it look like a serious dental-equipment brand at first glance?
2. Is Giorgos (photo and voice) the warm part, rather than decoration?
3. Is the phone number reachable in one tap on a phone?
4. Did anything from `references/anti-patterns.md` come back?
