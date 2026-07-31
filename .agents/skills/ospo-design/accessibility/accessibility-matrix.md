# Accessibility Matrix

Output path: `accessibility/accessibility-matrix.md`

Web outputs target WCAG 2.2 AA as the default compliance frame unless the product commits to a stricter level or another platform/legal standard applies. Numeric values below distinguish formal Criterion thresholds from deliberately stronger design targets.

## Accessibility Requirements Matrix

| Area | Criterion | Threshold | Design rule | Token/component implication |
| --- | --- | --- | --- | --- |
| Normal text contrast | WCAG 1.4.3 | At least `4.5:1` | Validate final rendered pair after opacity, texture, compositing, and state | `semantic.text.*`; use opaque support plate over variable imagery |
| Large text contrast | WCAG 1.4.3 | At least `3:1` for qualifying large text | Do not promote text to “large” merely to pass; keep functional copy readable | Type semantic roles plus contrast tests |
| Essential non-text contrast | WCAG 1.4.11 | At least `3:1` against adjacent colours where required | Essential boundaries, icons, charts, and states remain visible | `semantic.border.standard/strong`, status/icon tokens |
| Colour vision deficiency | Redundant meaning | No hue-only status/selection/data encoding | Pair colour with text, icon, shape, pattern, sign, or position; test protan/deutan/tritan and greyscale | Status, selection, chart, imagery contracts |
| Text over imagery | Stable contrast | Required ratio throughout every responsive crop/state | Move text or add `92–100%` opaque carbon support; never solve with glow | `component.scene-support.*` |
| High contrast/forced colours | Platform/WCAG support | All essential content and state survives | Use system colours, solid boundaries, zero functional grain/bloom, visible current/focus state | High-contrast mode tokens |
| Keyboard | WCAG 2.1.1/2.1.2 | All functionality operable; no keyboard trap | Use native semantics and current composite-widget key patterns | Actions/forms/navigation contracts |
| Focus visible | WCAG 2.4.7 and design target | Always visible; target solid `2px` perimeter and `3:1` separation | Focus is independent of hover, selection, error, and imagery; never glow-only | `semantic.focus.ring`, component focus tokens |
| Focus not obscured | WCAG 2.4.11 | Focused component not entirely hidden by author content | Add scroll padding, avoid sticky obstruction, preserve overlay focus return | Layout/navigation/dialog contracts |
| Focus order | WCAG 2.4.3 | Meaningful task/reading sequence | DOM/accessibility order follows meaning, not visual z-plane | Components and responsive layouts |
| Target size | WCAG 2.5.8 AA plus stronger design target | Formal web minimum `24×24 CSS px` with exceptions; design target `44×44 CSS px/pt`, Android `48×48dp`, or stricter current platform rule | Grow target independently from visible icon and density | `global.target.touch`, platform transform |
| Pointer gestures | WCAG 2.5.1/2.5.7 | Multipoint/path/drag has simple alternative where required | Upload, reorder, sliders, maps, and carousels provide keyboard/button alternatives | Drag/drop behavioral contract |
| Motion preference | User/platform preference | Reduced-motion branch available from first render | Replace travel, parallax, ambient drift, animated grain, and long fades with cut/short fade plus state cue | Reduced-motion mode tokens |
| Pause/stop/hide | WCAG 2.2.2 | Moving/auto-updating content lasting over `5s` is controllable where required | No persistent identity motion by default; provide pause for permitted media | Motion and media controls |
| Flashes | WCAG 2.3.1 | No more than `3` flashes in any one-second period within threshold | Prohibit flashing convergence light, rapid thermal alternation, and high-frequency animated grain | Motion/media anti-patterns |
| Text resize | WCAG 1.4.4 | Text resizes to `200%` without loss | Use relative/native semantic type, flexible containers, and no baked-in essential text | Type/platform transforms |
| Reflow | WCAG 1.4.10 | Reflow at `320 CSS px` equivalent without two-dimensional scroll except exemptions | Preserve labels, state, focus, and actions; data uses purposeful responsive alternative | Spatial/component responsive contracts |
| Text spacing | WCAG 1.4.12 | User overrides for line/paragraph/letter/word spacing do not break content | Avoid fixed-height text containers and clipping; body target line-height `1.5–1.7` | Typography and layout tokens |
| Body readability | Design target | `1rem` web-equivalent floor, weight `400+`, about `55–68` characters/line | Choose open apertures and robust counters; allow user scaling | `semantic.type.body.*` |
| Labels and names | WCAG 3.3.2/2.5.3/4.1.2 | Visible label and programmatic name/state | Label Fields and unfamiliar icons; visible words appear in accessible name | Forms/actions/icon contracts |
| Error identification | WCAG 3.3.1/3.3.3 | Error identified in text; correction suggested when known | Preserve input, associate error, name scope and Recovery | `component.field.error.*`, feedback |
| Status messages | WCAG 4.1.3 | Status exposed without unnecessary focus change | Use polite/assertive live semantics by urgency; throttle progress announcements | Feedback/Progress API |
| Images | WCAG 1.1.1 | Purpose-appropriate text alternative or decorative exclusion | Describe subject/action/function; style only when meaningful; no essential raster text | Imagery metadata and component APIs |
| Audio/video | WCAG 1.2 series | Captions, transcript, description, and controls as applicable | Sound/haptic is never the sole signal; no atmospheric autoplay in task flows | Media and feedback contracts |
| Timing | WCAG 2.2.1 | Adjustable/extendable timing except valid exceptions | Warn, explain expiry, allow extension/pause where required, preserve work | Timer/sequence contract |
| Authentication | WCAG 3.3.8 | Avoid cognitive-function tests without alternative | Support password managers, paste, passkeys/native methods, and accessible challenge alternatives | Forms/authentication domain extension |
| Cognitive load | Design target | One primary task/event; progressive disclosure; stable placement | Atmosphere may withhold story, never instructions, consequence, or Recovery | Interaction register and voice |
| Localization | Product requirement | At least `35%` text expansion design allowance plus script/RTL review | Flexible height, complete strings, locale units/formats, no essential truncation | Typography/content/component APIs |
| Cultural and trauma safety | Inclusive design review | Review before release for sensitive modules | Do not infer identity or use colonial, Indigenous-coded, firearm, land, migration, or animal imagery as generic decoration | Imagery/brand review gate |

## Component Completion Gate

An interactive component is incomplete until it has:

- default, hover where relevant, Focus, pressed, Selected/current where relevant, disabled, Loading, error, success/Completion, and reduced-motion/high-contrast behavior;
- semantic role, name, value/state, keyboard contract, logical focus order, and programmatic status;
- a platform-appropriate target, readable text, tested contrast, and redundant state encoding;
- localization/reflow behavior and a Recovery path for failure or interruption.

## Media And Atmosphere Boundary

- Texture, bloom, chromatic edge effects, and unresolved silhouettes are permitted only in expressive media.
- Text, icons, focus, forms, data, dialogs, consent, alerts, timers, and Recovery remain crisp and low texture.
- Identity art never supplies the only explanation of subject, status, progress, direction, or action.
- Anonymous silhouette treatment is not used for real-person identity, testimony, authorship, or contexts requiring representation.

## Test Matrix

Test at minimum:

- light, dark, high contrast/forced colours, and reduced motion;
- keyboard-only, screen reader, touch, pointer, speech/switch where supported;
- 200% text size, 400% browser zoom/reflow scenario, narrow/wide viewports, portrait/landscape;
- protan, deutan, tritan, greyscale, bright environment, low brightness;
- one long translation, RTL, complex-script fallback, locale numbers/dates/units;
- loading, offline, stale, error, retry, undo, resume, destructive confirmation, and Completion;
- final compressed identity media at 1×/2× density with support-text contrast.

## Anti-Patterns

- Treating WCAG as a final checklist rather than a component/state design input.
- Claiming compliance from palette hexes without testing rendered pairs and modes.
- Grain, glow, blur, opacity, or imagery beneath essential information.
- Tiny targets justified by visual minimalism, focus inferred from hover, or state encoded by warm/cool colour alone.
- Reduced motion implemented by deleting feedback, or high contrast implemented by increasing saturation.
- Accessibility exceptions recorded without scope, owner, rationale, alternate access, and expiry/review.
