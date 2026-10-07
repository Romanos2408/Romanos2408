# The workbench kit

The working implementation of every object is in `dental-tech/src/assets/style.css`, with the page in `dental-tech/src/index.html`. Reuse those classes rather than re-inventing them. This file records the measurements and the reasons, so changes stay true to the objects.

## Dymo label: `.dymo` (+ `.red`, `.blue`; black by default)
- Embossed look: off-white letters, `text-shadow: 0 -1px 0 rgba(0,0,0,.45), 0 1px 0 rgba(255,255,255,.28)`, plus a vertical sheen gradient over the tape colour.
- Slightly uneven cut ends: `clip-path: polygon(0 4%, 100% 0, 99.2% 100%, .6% 97%)`.
- Font: Sofia Sans Extra Condensed 760, uppercase, letter-spacing .13em.
- Every label gets its own tilt through `--r` (between -2.5° and 2°). Neighbouring labels never share the same angle.
- Use labels for headings, the call buttons and the brand stickers. Use at most about 10 on the page, or they stop being special.
- Never round the corners and never add a gradient border. Real tape is flat plastic.

## Handwriting: `.hand`
- Mynerve in ballpoint blue `#2a3f9d`. Use it for ticks, captions, the Post-it, margin notes and the signature.
- Keep each note to 2-8 words, the way someone actually writes on a form.
- For a highlighter mark use `<u>` inside `.scribble` (a yellow band behind the text). For a circled value use `.circled` (a red hand-drawn ellipse).

## Δελτίο εργασίας: `.sheet`
- A white form slightly rotated (-0.6°) with a perforated top edge (radial-gradient dots) and carbon-blue ruled lines `#c9d3ea`.
- Printed parts use Fira Mono uppercase in grey; filled-in parts use `.hand`.
- Each service is a `.box` (printed square) with a handwritten ✓, a printed name (`.job`) and a handwritten note.
- The footer fields are ΕΚΤΙΜΗΣΗ ΒΛΑΒΗΣ (0 €, circled), ΕΓΓΥΗΣΗ and ΤΕΧΝΙΚΟΣ (signature).
- Brand stickers are small Dymo labels stuck on the right edge (`.stickers`). On mobile they wrap under the form.

## Polaroid: `.polaroid.taped`
- White frame with a 12px border and a deeper bottom for the caption. The photo area `.ph` is square.
- Masking tape on top (`.taped::before`) with zig-zag torn edges. Tape angle is set by `--tr`.
- On hover the photo lifts: rotation goes to 0, it scales to 1.02 and the shadow deepens.
- A missing photo shows striped grey with «φωτό σύντομα 📷», produced by the build's photo fallback.

## Post-it: `.postit`
- Yellow `#ffe66d`, 12.5rem square, rotated -4° to -6°, with the bottom-right corner curling (the corner grows on hover).
- Holds the phone number in big handwriting. The whole note is a `tel:` link.

## Hang tag: `.tag-wrap > .tag`
- Manila `#ead8ab`, with a chamfered left end via clip-path and a punched hole via radial-gradient. A red string is drawn by `.tag-wrap::before`.
- Holds the KAVO prices in mono, with a handwritten note beside it (`.tag-note`, arrow pointing at the tag).

## Business card: `.bcard`
- 1.75:1 white card rotated -1.5°, with the name in Manrope 800 and the contact lines in mono with red letters (Τ, V, E).
- A red Dymo "24/7" stuck in the corner and a handwritten «Δεν ενοχλείς!».
- Beneath it sit two Dymo buttons: Κλήση (red) and Viber (blue).

## Shadows
One shared shadow, `--drop`, layered tight, mid and far, so every object looks lit by the same ceiling light. Don't invent a shadow per component.

## Motion hooks
- `.drop-in` with `--d` delay: objects land on the bench.
- `.typing`: the Dymo letters print one by one.
- `.reveal`: objects below the first screen settle in as you scroll.
- `[data-speed]` on a wrapper (never on the animated element itself): depth parallax.
