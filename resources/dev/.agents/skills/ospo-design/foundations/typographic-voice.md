# Typographic Voice

Output path: `foundations/typographic-voice.md`

## Voice Weight

- **Weight personality:** quiet infrastructure with occasional monumental titles. Typography should feel steady, open, and materially present, never distressed or theatrically “Western.”
- **Authority, warmth, precision, fragility, institutional tone, or display energy:** body copy is precise and humane; display copy is grave and cinematic. Authority comes from placement, scale, and restraint rather than condensed capitals or ornamental styling.
- **Weight shifts by hierarchy, state, or emotional moment:** body remains 400–500, labels and controls 550–650, headings 600–700, and rare display moments 650–750. Do not use weights below 400 for functional text. Reserve the heaviest weight for short, high-level statements.

## Voice Classification

| Type category | Role in the language | Why it fits |
| --- | --- | --- |
| Open-aperture humanist sans | Primary UI, body, labels, metadata, and accessibility-critical text | Holds clarity against dark fields, survives small sizes, and feels less clinical than a rigid geometric sans |
| Sturdy oldstyle or transitional serif | Optional display, editorial title, pull quote, and scene chapter | Adds gravity and human irregularity without resorting to novelty frontier lettering |
| Tabular mono, sparingly | Coordinates, time, technical values, or machine-readable provenance | Separates factual data from narrative voice; use only where the content is genuinely structured |

## Type Pairing Logic

- **Primary face:** one open-aperture humanist sans with high x-height, distinct `I/l/1` and `O/0`, generous counters, and reliable variable or static weights.
- **Secondary face:** one moderate-contrast serif with sturdy serifs, robust lowercase, and an optical text cut where available.
- **Pairing contrast:** contrast texture and cadence, not historical costume. The sans carries function; the serif carries rare atmosphere.
- **Pairing boundary:** two families maximum. Never alternate families within one control, label set, paragraph, or compact component. If only one family is available, use the sans throughout and create hierarchy with size, weight, and space.

## Text As Spatial Element

- **Typography as annotation, object, architecture, label, texture, or absence:** default to annotation and architecture. A title may become one large quiet block; labels remain crisp infrastructure. Text is never used as grain or decorative texture.
- **Placement behavior:** anchor text to a calm edge or negative-space region. Maintain a consistent left edge and allow generous breathing room above and beside a display block.
- **Relationship to image, surface, and grid:** do not place body text over active particulate bloom or a subject contour. Use an opaque carbon support plate when crop-dependent contrast cannot be guaranteed. Align text to the compositional axis without copying the irregularity of the image.

## Dialogue Density

- **Text-to-visual ratio:** low in identity-bearing scenes; moderate in functional views. A hero should normally carry one short title, one supporting sentence, and one action cluster at most.
- **Verbosity tolerance:** terse but not cryptic. Prefer concrete verbs and short clauses; move explanation into progressive disclosure.
- **Label density:** sparse, stable, and explicit. Use labels for unfamiliar icons and never force atmosphere through vague one-word controls.
- **Information scent rule:** every interactive label states what will happen. Mystery belongs to the image, not to navigation, consent, payment, recovery, or safety copy.

## Silence As Whitespace

- **Meaning of absent text:** silence creates watchfulness and lets the primary event remain unresolved. It should feel intentional, not unfinished.
- **Whitespace pressure:** preserve at least one display line-height between a title and supporting copy, and two between copy and unrelated controls. In dense views, retain ordinary product spacing rather than imitating cinematic emptiness at the cost of scanning.
- **Where text must not appear:** across faces or recognition contours; inside bright convergence zones; over high-frequency grain; along a luminous edge; or in the lower foreground when that region carries the directional route.

## Scale Relationship

Use a hand-tuned responsive scale. Values are CSS-pixel-equivalent targets and must be validated in the actual platform font.

| Role | Size/range | Weight | Line height | Behavior |
| --- | --- | --- | --- | --- |
| Display | `clamp(2.5rem, 6vw, 4.5rem)` | 650–750 | 0.96–1.06 | Maximum 8–12 words; sentence or title case; optical tracking from `-0.03em` to `0` |
| Heading 1 | `clamp(2rem, 4vw, 3rem)` | 650–700 | 1.05–1.15 | Short line length; no faux small caps or textured fill |
| Heading 2 | `clamp(1.5rem, 2.5vw, 2rem)` | 600–700 | 1.10–1.22 | Establishes sections without competing with the scene |
| Body lead | `1.125rem`–`1.25rem` | 400–500 | 1.50–1.65 | Maximum 55–68 characters per line |
| Body | `1rem`–`1.125rem` | 400–500 | 1.50–1.70 | Minimum `1rem` equivalent; honour user text scaling |
| Caption | `0.8125rem`–`0.9375rem` | 400–500 | 1.40–1.60 | Factual and complete; never encode essential information only here |
| Label/control | `0.875rem`–`1rem` | 550–650 | 1.25–1.45 | Sentence case; `0` to `0.02em` tracking; preserve a minimum usable control target |
| Data/mono | `0.8125rem`–`0.9375rem` | 450–550 | 1.40–1.60 | Tabular numbers where alignment matters; provide spoken labels |

## Optical And Platform Considerations

- **Optical sizing:** enable an optical-size axis for serif display and text cuts when the font supports it; otherwise choose separate text/display masters. Do not simulate optical size with blur or stroke.
- **Small text aperture and legibility:** require open apertures, clear punctuation, distinguishable numerals, and durable counters. Avoid compressed widths and thin strokes below 16px.
- **Dark-mode weight compensation:** dark backgrounds can make pale type appear heavier or haloed. Prefer a warm or mineral off-white, test 400 and 450/500 weights, and avoid text glow.
- **iOS, Android, web, and responsive differences:** validate rendered x-height, wrapping, synthetic bold prevention, variable-font support, fallback metrics, zoom, dynamic type, and 200% text reflow on each target. Preserve role relationships rather than forcing identical pixel sizes.
- **Localization:** allow at least 35% expansion for translated labels, avoid fixed-height text boxes, and select fallbacks that support required scripts without changing the quiet, open-aperture character.

## Accessibility Boundary

Typography is a functional translation layer. If a display choice conflicts with legibility, user scaling, language coverage, or contrast, the functional requirement wins. Do not bake type into generated imagery when the text must be translated, selected, searched, announced, or resized.

## Anti-Patterns

- “Wanted poster,” circus slab, rope, woodcut, distressed, stencil, spur, or decorative frontier fonts.
- Condensed all-caps body copy, excessive tracked capitals, faux small caps, or ornamental drop caps.
- Glowing, blurred, chromatically split, grain-filled, or low-opacity text.
- Ultra-light body weights, narrow line-height, long centered paragraphs, or text justified into rivers.
- More than two type families, arbitrary font changes by scene, or using a mono face merely to appear technical.
- Withholding labels, recovery guidance, or consent language to preserve mood.
