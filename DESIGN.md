---
name: Meníčko Litomyšl
description: Today's Litomyšl lunch menus, printed like a hand-coloured woodcut.
colors:
  ground: "oklch(74.5% 0.135 77)"
  paper: "oklch(97.6% 0.012 85)"
  ink: "oklch(19% 0.01 70)"
  muted: "oklch(43% 0.03 70)"
  line: "oklch(19% 0.01 70)"
  on-line: "oklch(97.6% 0.012 85)"
  red: "oklch(51% 0.17 29)"
  on-red: "oklch(98% 0.01 85)"
  soup: "oklch(86% 0.055 40)"
  dessert: "oklch(86% 0.045 155)"
  ground-dark: "oklch(16.5% 0.01 65)"
  paper-dark: "oklch(25% 0.045 72)"
  ink-dark: "oklch(94% 0.015 85)"
  muted-dark: "oklch(78% 0.06 78)"
  line-dark: "oklch(74% 0.13 77)"
  on-line-dark: "oklch(17% 0.012 65)"
  red-dark: "oklch(63% 0.17 29)"
  on-red-dark: "oklch(15% 0.01 30)"
  soup-dark: "oklch(34% 0.065 38)"
  dessert-dark: "oklch(33% 0.045 155)"
typography:
  display:
    fontFamily: "Grenze, Georgia, serif"
    fontSize: "2.125rem"
    fontWeight: 800
    lineHeight: 1.05
    letterSpacing: "0.005em"
  headline:
    fontFamily: "Grenze, Georgia, serif"
    fontSize: "1.5rem"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "0.01em"
  title:
    fontFamily: "Grenze, Georgia, serif"
    fontSize: "1.1875rem"
    fontWeight: 700
    lineHeight: 1.2
  dish-label:
    fontFamily: "Grenze, Georgia, serif"
    fontSize: "1.125rem"
    fontWeight: 700
    lineHeight: 1
  stamp:
    fontFamily: "Grenze, Georgia, serif"
    fontSize: "1rem"
    fontWeight: 800
    lineHeight: 1.3
    letterSpacing: "0.09em"
  body:
    fontFamily: "system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.45
  control:
    fontFamily: "system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "0.9375rem"
    fontWeight: 600
    lineHeight: 1.3
  meta:
    fontFamily: "system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "0.8125rem"
    fontWeight: 400
    lineHeight: 1.45
rounded:
  pill: "2px 4px 3px 2px"
  field: "3px"
  frame: "3px 6px 4px 5px"
spacing:
  page-gutter: "16px"
  inside-closed: "10px"
  between-menus: "22px"
  before-closed: "36px"
  column-min: "340px"
components:
  day-pill:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    typography: "{typography.control}"
    rounded: "{rounded.pill}"
    padding: "6px 13px"
  day-pill-selected:
    backgroundColor: "{colors.red}"
    textColor: "{colors.on-red}"
    typography: "{typography.control}"
    rounded: "{rounded.pill}"
    padding: "6px 13px"
  search-field:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.field}"
    padding: "10px 12px"
  menu-card:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.frame}"
    padding: "4px"
  name-block:
    backgroundColor: "{colors.line}"
    textColor: "{colors.on-line}"
    typography: "{typography.headline}"
    padding: "8px 8px 7px 12px"
  band:
    backgroundColor: "{colors.line}"
    textColor: "{colors.on-line}"
    typography: "{typography.display}"
---

# Design System: Meníčko Litomyšl

## Overview

**Creative North Star: "The Portmoneum Woodcut"**

The page is a print after Josef Váchal, whose Portmoneum house stands in Litomyšl: a heavy black cut line, with colour washed by hand only inside it. An ochre wall is the ground; each restaurant's menu is a paper block in an uneven black frame, its name cut white out of a black block. Everything that has to be read at length (dishes, prices, allergens, controls) stays in the plain system face, so the woodcut is carried by line, frame and the cut letter, never by making the menu harder to scan.

Density is high and deliberate: menus pack into as many columns as fit, top-down, so a short menu never leaves a hole next to a long one. Colour is rationed: one solid red for state (selected day, favourite ring, stamps), two pale washes for dish types, and the rest is ink, paper and wall. Dark mode inverts the print: the ground becomes ink, the cut becomes ochre, the paper turns dark ochre-brown, and the washes stay.

Motion has one grammar: switching day is pulling a fresh print. The red day label travels to the new day and the new menus press down onto the page; nothing else fades.

**Key Characteristics:**
- Ochre wall ground, paper blocks, heavy black cut frames roughened by one SVG displacement filter.
- Restaurant names cut out of a black block in Grenze; all reading text in the system face.
- Colour only inside the line: soup and dessert washes, red for state only.
- States are stamps: a red, rotated, uppercase Grenze word pressed onto the paper.
- Full-bleed black band for the title and search; day row on the wall below it.

## Colors

A three-material print (wall, paper, ink) with a single red and two pale washes; every value is OKLCH and has a dark-mode twin.

### Primary
- **Váchal Red** (red / red-dark): the only solid colour. Selected day pill, the favourite ring and filled heart, stamp borders and words, focus outline, selection tint, caret. Never a background for content and never decoration.

### Secondary
- **Madder Wash** (soup / soup-dark): full-width background of soup rows inside a menu; text on it stays ink.
- **Verdigris Wash** (dessert / dessert-dark): full-width background of dessert rows; text stays ink.

### Neutral
- **Portmoneum Ochre** (ground): the page wall in light mode; in dark mode the same hue becomes the cut line (line-dark), so the frames glow ochre on ink.
- **Print Paper** (paper / paper-dark): menu blocks, day pills, search field. Dark mode is a dark ochre-brown paper, not grey.
- **Cut Ink** (ink, line): body text and the cut line share one value in light mode; they are separate tokens because dark mode splits them (ink goes light, line goes ochre).
- **Reverse** (on-line): text cut out of the black band and name blocks.
- **Faded Ink** (muted / muted-dark): allergens, placeholder, secondary notes.

### Named Rules
**The Inside-The-Line Rule.** Colour lives only inside a cut frame or a cut row: washes fill rows between black rules, red fills the pill inside its black border. No coloured element floats free on the wall.

**The One Red Rule.** Red means state (chosen, favourite, failed). If it is not one of those, it is not red.

## Typography

**Display Font:** Grenze 700–800 (self-hosted, latin and latin-ext subsets in site/fonts, with Georgia fallback)
**Body Font:** system-ui (with -apple-system, Segoe UI, sans-serif)

**Character:** Grenze is the cut letter, blackletter-tinged and blunt, used only where a woodcutter would carve: the title, restaurant names, the closed-group heading, dish labels and stamp words. The system face carries everything read at length so scanning stays fast.

### Hierarchy
- **Display** (800, 34px, 1.05): the title in the black band, once.
- **Headline** (700, 24px, 1.1, balanced): restaurant names in their name blocks.
- **Title** (700, 19px, 1.2): the closed-restaurants heading and names on closed labels.
- **Dish label** (700, 18px, 1): the inline label before a dish (A, 1, Pizza I).
- **Stamp** (800, 16px, 0.09em, uppercase): stamp words only.
- **Body** (400, 16px, 1.45; dark mode 1.5 with 0.01em tracking): dish names, notes. Prices 650 weight, tabular figures, right-aligned.
- **Control** (600, 15px, 1.3): day pills, empty-state buttons, notes.
- **Meta** (400, 13px): update time, allergens, footer.

### Named Rules
**The Cut Letter Rule.** Grenze is for names and labels that are carved, never for sentences, dishes or prices.

## Layout

One centred column, max 1280px, 16px side gutter. Bands (the black title band, the day row) run full-bleed inside it via a 100vmax box-shadow plus clip-path trick. Menus flow into CSS columns of at least 340px with a 22px gap: one column on phones, two on tablets, three on desktop, packed top-down and never split. Spacing rhythm: 22px between menus (margin on top, so each column ends flush), 36px before the closed-restaurant block, 10px between its labels; the closed block spans all columns as an auto-fill grid on the same 340px column lines.

The header is sticky. Below 1000px the title block (fixed 62px height) scrolls away and only search and day row stay pinned; at 1000px and up the title, update time and search share one row (search capped at 380px) and the whole header stays pinned. The day row scrolls horizontally when it overflows.

## Elevation & Depth

Flat. Depth is the print's: a black frame on paper on a wall. There are no drop shadows. The only box-shadows are structural: the full-bleed band extension, and a 2px inset paper ring that separates the red selected pill from its black border. Favourites lift by a 3px red outline at 4px offset, not by shadow.

### Named Rules
**The Flat Print Rule.** Nothing casts a shadow. Separation comes from cut lines, paper against wall, and red rings.

## Shapes

Corners are near-square and deliberately uneven, as if cut by hand: frames 3px 6px 4px 5px, pills 2px 4px 3px 2px, the search field 3px. Lines are heavy: 4px menu frames, 2px pill borders and dish rules, 2px frames on closed labels, 3px stamp borders.

### Named Rules
**The Roughen-The-Edge-Only Rule.** The #cut filter (fractal-noise turbulence, base frequency 0.045, 3 octaves, displacement scale 5) is applied only to pseudo-elements that draw a frame or a black block. Text is never filtered.

## Components

### Day Pills
Small paper tickets in a black cut border.
- **Shape:** uneven near-square (2px 4px 3px 2px), 2px line border.
- **Default:** paper background, ink text, control type, 6px 13px padding.
- **Hover:** paper mixed 20% toward red. **Active:** 1px downward press (80ms).
- **Selected:** solid red, on-red text, black border kept, 2px inset paper ring.
- **No match (search active):** 45% opacity unless selected.

### Search Field
- **Style:** paper field in the black band, no border, 3px radius, 10px 12px padding, red caret.
- **Focus:** 3px solid red outline, no offset.

### Menu Card
The signature: a paper block in a cut frame, headed by the restaurant name cut out of black.
- **Frame:** 4px line border on a pseudo-element through #cut, uneven radius, above the content.
- **Name block:** line-colour block running under the frame on three sides so frame and block read as one cut; Grenze headline in on-line, link underlines 2px on hover.
- **Dish rows:** 2px line rule between rows; price right, tabular; allergens on their own line in meta. Soup and dessert rows take their wash edge to edge, with allergens at 70% ink.
- **Favourite:** 3px red outline at 4px offset around the card.
- **Closed label:** no dishes means no paper: transparent, 2px frame straight on the wall, title-size name in ink, note inline.

### Favourite Heart
36px hit area in the name block; an inline SVG heart, 2.2 stroke, outline by default. Hover shifts toward red; pressed fills red with an on-line stroke (red stroke on closed labels); press scales the heart to 0.85 (100ms).

### Stamp
State made visible: a short uppercase Grenze word in red inside a 3px red border, rotated -3deg, pressed above the plain-ink sentence that explains it (for example "Nenačteno"). The stamp word is hidden from screen readers because the sentence repeats it.

### Day Switch Motion
The selected pill is a shared view-transition element moving over 260ms on cubic-bezier(.16, 1, .3, 1). The old menus vanish at once; the new ones press in over 220ms from 10px above at 0.6 opacity. The root does not cross-fade. Reduced motion removes both.

## Do's and Don'ts

### Do:
- **Do** keep every colour inside a black line: washes in ruled rows, red inside a bordered pill or stamp.
- **Do** cut new headings and names out of a line-colour block in Grenze, and keep reading text in the system face.
- **Do** draw new frames and black blocks on pseudo-elements through the #cut filter, so the text stays sharp.
- **Do** show failure or staleness as a red rotated stamp with a plain sentence and a link, never by hiding the restaurant.
- **Do** define every new colour as an OKLCH token with a dark-mode value.

### Don't:
- **Don't** add drop shadows, gradients or soft white cards on a pale page; the depth is the print.
- **Don't** use red for anything but state (selected, favourite, failed).
- **Don't** apply the #cut filter to an element that contains text.
- **Don't** set dishes, prices or sentences in Grenze.
- **Don't** add fades or entrance animations beyond the day-switch press.
