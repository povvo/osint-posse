# Iconography System

Output path: `foundations/iconography-system.md`

## Icon Set Identity

- **Icon set family:** solemn, low-detail utility pictograms on a consistent 24px grid. Begin with one established, accessibility-reviewed set and extend it only when a product concept has no adequate symbol.
- **Outline/filled/duotone rule:** outline is the default functional state; filled marks indicate selected, active, or strongly categorical states. A duotone warm/cool edge is allowed only for expressive icons at 48px or larger and never as the sole state distinction.
- **Stroke weight:** `2px` at 24px, `1.5px` at 16px, and proportional scaling above 32px with optical review. Critical or low-vision variants may increase to `2.5px`.
- **Corner radius:** restrained, approximately `1–2px` at 24px. Use roundness to protect legibility, not to make the set playful.
- **End-cap and join style:** mostly round caps and round joins for small-size durability; use square caps only when direction or measurement requires an exact endpoint.
- **Filled silhouette boundary:** category and scene glyphs may use a solid dark mass with one contour cutout. Functional icons do not receive grain, bloom, blur, or chromatic aberration.

## Optical Correction

- **Overshoot:** circles and pointed forms may exceed the nominal alignment box by `0.5–1px` at 24px. Keep the tappable box unchanged.
- **Optical centering:** shift visually heavy forms `0.5–1px` away from their dense side. Play triangles, chevrons, and asymmetric tools almost never appear centered by geometric bounds alone.
- **Visual weight balancing:** reduce enclosed black area or open a counter when a filled icon appears heavier than its outline peers. Compare at actual rendered size, not only enlarged.
- **Stroke-to-container compensation:** icons inside filled buttons may need `0.25–0.5px` lower nominal stroke or `1px` smaller visible size because the container increases perceived weight.
- **Baseline correction:** align the visual base of the glyph, not its mathematical bounds, with the text cap-height or control center.

## Metaphor Rules

- **Literal metaphors:** use familiar objects only when the action genuinely concerns that object—folder for stored files, magnifier for search, speaker for audio, map pin for location.
- **Abstract metaphors:** prefer text plus a simple state or directional mark. Do not invent picturesque objects for concepts such as trust, intelligence, automation, privacy, resilience, or quality.
- **Culturally risky metaphors:** weapons, badges, stars, brimmed hats, feathers, conical shelters, skulls, bison, cacti, ropes, and campfires are narrative imagery, not universal symbols. Use only in a context where their literal meaning has been reviewed.
- **Metaphors requiring labels:** unfamiliar domain actions, AI behavior, sync state, data provenance, permissions, irreversible actions, accessibility functions, and any icon that users cannot name quickly.
- **Status rule:** error, success, warning, offline, locked, and selected states use icon plus text or shape. Colour is supplemental.

## Icon And Text Relationship

- **Icon-only eligibility:** reserve for platform-standard actions with unambiguous context, such as close, back, forward, search, play/pause, overflow, and expand/collapse. Even these require an accessible name.
- **Label pairing:** place labels beside icons for primary actions and beneath them only in stable navigation. Sentence case is preferred.
- **Tooltip or accessible name:** tooltips supplement but do not replace visible labels for unfamiliar actions. Every interactive icon exposes an accessible name and state; decorative icons are hidden from assistive technology.
- **Dense UI behavior:** retain the same set, reduce secondary icons before removing labels, and use grouping or progressive disclosure instead of shrinking below the small-size rules.
- **Text alignment:** use a `6–8px` gap between 20–24px icons and labels. Multi-line labels align to the icon’s visual top or first-line center according to platform convention.

## Sizing And Alignment

- **Grid:** design at `24×24`; support simplified `16×16`, standard `20×20`/`24×24`, and expressive `32×32`/`48×48` masters.
- **Safe area:** keep ordinary strokes within a `2px` inset at 24px; allow optical overshoot without touching the container edge.
- **Touch target:** use at least `44×44 CSS px` or the stricter native-platform floor. The visible glyph may remain 20–24px.
- **Baseline alignment:** align with text using optical cap-height and platform metrics; avoid per-screen manual nudges.
- **Small-size simplification:** remove interior texture, secondary strokes, double contours, and shallow notches. Preserve the action-defining angle, opening, or mass.
- **Responsive rule:** the icon’s target may grow with input modality while the visible mark stays stable; never infer touch target from glyph size.

## Brand And Emotional Signal

- **Personality:** spare, watchful, durable, and direct.
- **Polish level:** highly controlled geometry with slight optical humanization; no faux-handmade wobble.
- **Trust signal:** familiar metaphor, visible label where needed, consistent state changes, and no ornamental ambiguity.
- **Expressive limit:** one filled silhouette or one local warm/cool accent at larger sizes. The utility set remains crisp and monochrome on functional surfaces.

## State Translation Rules

- Default: outline mark with current text colour.
- Hover: surface or label changes before the icon; no glow-only state.
- Focus: focus ring belongs to the control container, not a luminous icon halo.
- Pressed: minor value change or `1px` container compression; glyph geometry stays stable.
- Selected: filled counterpart plus marker or label/state change.
- Disabled: retain recognizability and readable label; reduce prominence without dropping below required contrast for essential information.
- Error/warning/success: use distinct symbol, explicit copy, and tested contrast. Do not merely recolour the same circle.
- High contrast: use solid strokes and system colours; disable duotone and atmospheric effects.

## Asset And Engineering Rules

- Use SVG or native vector paths for functional icons; preserve a `viewBox="0 0 24 24"` for web assets.
- Prefer `currentColor` for single-colour icons. Expose separate semantic paths only when a validated duotone state is required.
- Set `fill="none"` or filled geometry intentionally; do not inherit accidental defaults.
- Prevent stroke scaling when icons resize if the platform supports it, or ship size-specific masters.
- Test at 100%, 200% zoom, 1× and 2× pixel density, forced colours, dark/light modes, and with common font fallbacks beside the icon.

## Anti-Patterns

- Custom frontier-themed icon packs, decorative spurs, rope borders, distressed glyphs, or weapon metaphors for ordinary actions.
- Mixing rounded, sharp, filled, outline, and duotone families without state logic.
- Grain, glow, blur, texture, thin chromatic rims, or colour separation on small functional icons.
- Unlabelled abstract icons, tooltip-only meaning, hover-only state, or inaccessible SVG titles.
- Shrinking visible icons and targets to preserve sparse layouts.
- Using colour alone for status, selection, ownership, direction, or severity.
