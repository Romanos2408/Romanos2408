---
name: dental-tech-design
description: Art direction, copy voice and build rules for dental-tech.gr, the website of Γιώργος Πατεράκης (Υποστήριξη Οδοντιατρείου), a friendly, funny, 24/7 dental-equipment technician in Heraklion. Use this skill for ANY design, redesign, layout, copy, photo or styling work on dental-tech.gr or the dental-tech/ folder, even small tweaks ("change the hero", "add a section", "make it less AI-looking", "add his photos", "new colors"). It exists to stop the site drifting back into generic AI-template looks.
---

# dental-tech.gr design skill

The client is one person, not a company. Dentists in Heraklion call Giorgos when a chair, handpiece, autoclave or X-ray stops working, any hour of any day. He is a physicist who also keeps the telescope at Skinakas Observatory running. He is warm, funny and always on the road with a car full of parts. The site should feel like meeting him, not like reading a brochure.

The user has rejected three previous versions for looking "like all the websites you make" and "AI-ish". Read `references/anti-patterns.md` before designing: it lists exactly what those versions did, so you can avoid it.

## The concept: Ο πάγκος (the workbench)

The page is his workbench, laid on a white marble countertop (marble is what dental clinics are made of). Everything on it is a real object from a technician's day:

| Object | Used for | Why it works |
|---|---|---|
| **Dymo label tape** (embossed white capitals on red/black/blue plastic tape) | Section headings, the call button | Every technician labels parts with a Dymo. Instantly "workshop", impossible to mistake for a template. |
| **Δελτίο Εργασίας** (carbon-copy work order, ruled lines, blue ballpoint ticks) | The services list | Dentists sign one of these after every visit. Ticked boxes plus a few handwritten words carry the services with almost no text. |
| **Polaroids held by masking tape** | His photos, with handwritten captions | Personal and funny ("Το γραφείο μου" under a photo of his car). |
| **Yellow sticky note** | The phone number | It's what a dentist would stick on the reception screen. |
| **Hang tag on a string** | The KAVO price offer | A price tag, literally. |
| **Business card** | Contact section | The thing he hands out. |

Objects sit at slight, varied angles (between -3° and 3°, never all the same), with soft realistic shadows, as if dropped on the counter. The marble stays calm and white; the objects bring the colour.

Details, measurements and CSS for each object are in `references/kit.md`. Read it before writing CSS.

## Palette

Pull every colour from the objects, nothing invented:

- Marble white `#f5f4f0`, veins `rgba(90,92,98,.16)`; the texture is `assets/marble.svg` used as a mask
- Ink black `#1d1e20` for text
- Dymo red `#d22b2b`, Dymo black `#1b1b1d`, Dymo blue `#1f4fa3`, with label text `#fbfbf8`
- Ballpoint blue `#2a3f9d` for all handwriting
- Post-it yellow `#ffe66d`
- Masking tape `rgba(232,220,190,.85)`
- Carbon-paper blue lines `#c9d3ea` on the work order

Dark mode is the same bench at night under a desk lamp: counter `#18191b`, objects keep their colours, ink becomes `#ecebe6`. Never invert the Dymo tape or the Post-it.

## Type (all three must have Greek; they do)

- **Dymo labels:** Sofia Sans Extra Condensed, 700-800, uppercase, letter-spacing .12em, with an embossed text-shadow
- **Handwriting:** Mynerve. Use it only for things he would write by hand: ticks, captions, the sticky note, notes in the margin. Never for paragraphs.
- **Everything else:** Fira Mono for the printed parts of forms and tags (labels like "ΗΜΕΡΟΜΗΝΙΑ", "ΥΠΟΓΡΑΦΗ") and a plain sans (Manrope) for the few sentences of body text

Self-host the fonts. Get them with `npm pack @fontsource/<name>` (npm is reachable; Google Fonts is a GDPR risk in the EU) and keep only the greek and latin woff2 subsets.

## Voice

He talks; the site doesn't "present". Write in Greek and in the first person singular ("φτιάχνω", "πάρε με"), and use the informal εσύ with dentists. Use short sentences, and add one joke per section at most.

Good:
- «Χάλασε; Πάρε με. 24/7. Σοβαρά.»
- «Δεν ενοχλείς. Ούτε Κυριακή.»
- «Το πρωί τηλεσκόπια, το απόγευμα έδρες. Οι έδρες είναι πιο εύκολες.»
- «Μέχρι να φτιαχτεί, δουλεύεις με το δικό μου.»

Never use: «Η εταιρεία μας», «παρέχουμε», «λύσεις», «υψηλής ποιότητας», «Γιατί να μας επιλέξετε», «Η ικανοποίησή σας», or any line that would fit any other business. If a line could appear on a plumber's site unchanged, cut it or make it about dental gear.

Budget: about **120 words of body text on the whole page**, not counting labels and handwritten ticks. If you go over, cut.

Facts you may use are in `references/facts.md`. Don't invent years of experience, client counts, reviews or awards. Leave a visible TODO for the user instead.

## Page structure (one page)

1. **Bench top (hero):** a Dymo headline, one handwritten line, his big Polaroid, and the Post-it with the phone. One call button, which is itself a Dymo label.
2. **Δελτίο Εργασίας:** the six services as ticked lines on a work-order sheet, each with 2-5 handwritten words. A "signature" at the bottom reading «Γ. Πατεράκης».
3. **Hang tag:** the KAVO annual service, up to €280 for labour and up to €120 for parts.
4. **Polaroids:** 3-5 photos of him with funny handwritten captions, plus 2 sentences in his voice.
5. **Business card:** phone, Viber, email, «24/7».

Five blocks, no more. No tabs, no FAQ, no stats strip, no logo carousel. Brands may appear as tiny Dymo labels stuck on the work order, not as a marquee.

## Photos

Giorgos is the brand. His real photos go in the Polaroids and the hero; never a stock person standing in for him. Equipment shots may be free stock (Unsplash, Pexels or Kaboompics, never "Unsplash+"). Missing photos render as an empty Polaroid with a handwritten «φωτό σύντομα 📷», which looks deliberate and stays on-concept. `dental-tech/PHOTOS.md` lists the file names.

PNG cut-outs with transparent backgrounds (a handpiece, a Dymo printer, a coffee cup) can sit directly on the marble as props. They are the best way to add depth. The build keeps the transparency.

## Motion

Physical, small and rare:
- On load, the objects "drop" onto the bench with a slight overshoot, staggered.
- The Dymo headline types out letter by letter, like the label maker clicking.
- On hover, a Polaroid lifts (bigger shadow, rotation towards 0°) and the Post-it corner peels.
- Parallax by depth: the marble moves slowest, paper objects at medium speed, props fastest.
- Everything is off under `prefers-reduced-motion`, and the first frame is complete without JS.

## Build

The site lives in `dental-tech/`: `src/index.html` holds the page, `src/assets/` the CSS, JS, fonts and marble, `src/photos/` the photos, and `build.py` turns them into `site/`. Keep that pipeline: `{{photo:name|alt|class|fallback}}` and `{{icon:...}}` tokens, redirects, sitemap and the Search Console tag. Run `python3 build.py`, then check the page with Playwright (Chromium at `/opt/pw-browsers/chromium`) at 1360px and 390px, in light and dark, for horizontal overflow and Greek font loading.

## Before you hand it over

Ask yourself honestly:
1. Cover the logo. Could this page belong to anyone else? If yes, it's not done.
2. Is every object one Giorgos would actually have on his bench?
3. Is the body text under about 120 words, and does it sound like him talking?
4. Did anything from `references/anti-patterns.md` sneak back in?
5. Does a dentist with a broken chair find the phone number in under 2 seconds on a phone?
