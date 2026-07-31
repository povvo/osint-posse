# Semantic Tokens

Output path: `tokens/semantic-tokens.md`

Semantic tokens name user-facing intent. Values below define the dark identity mode; `mode-tokens.md` supplies light, high-contrast, and reduced-motion overrides. Component tokens may reference only `semantic.*` tokens or other component tokens within the same contract.

## Semantic Intent Map

### Surface, Text, Border, And Icon

| Token | Intent | Default value | State | Mode | Required contrast/behavior |
| --- | --- | --- | --- | --- | --- |
| `semantic.surface.canvas` | Primary application field | `{alias.palette.field.deep}` | Default | Dark default | Absorptive base; no text-dependent texture |
| `semantic.surface.canvas.alternate` | Second dark plane | `{alias.palette.field.alternate}` | Default | Dark default | Visible by value or boundary; not elevation alone |
| `semantic.surface.raised` | Functional raised content | `{alias.palette.field.lifted}` | Default | Dark default | Pair with primary text; elevation remains restrained |
| `semantic.surface.overlay` | Menu/dialog support | `{alias.palette.field.deep}` | Open | Dark default | `92–100%` opacity behind text |
| `semantic.surface.critical` | High-stakes information plate | `{alias.palette.field.deep}` | Critical | Any | Zero grain/bloom; crisp validated boundaries |
| `semantic.surface.disabled` | Unavailable control surface | `{alias.palette.field.alternate}` | Disabled | Dark default | Label remains readable; state also conveyed in semantics |
| `semantic.surface.scrim` | Blocks background interaction | `rgb(13 14 14 / 0.72)` | Overlay | Dark default | Background becomes inert; not a text surface |
| `semantic.text.primary` | Primary readable text | `{alias.palette.convergence.cool}` | Default | Dark default | WCAG 2.2 target for actual size/weight; no glow |
| `semantic.text.secondary` | Supporting copy | `{alias.palette.thermal.cool.primary}` | Default | Dark default | Do not use below validated size/weight |
| `semantic.text.muted` | Metadata and low emphasis | `{alias.palette.mediator.mid}` | Default | Dark default | Must still meet required text contrast |
| `semantic.text.inverse` | Text on pale surfaces | `{alias.palette.field.deep}` | Default | Dark default | Validate against actual pale field |
| `semantic.text.on-accent` | Text on primary warm action | `{alias.palette.field.deep}` | Default | Dark default | Minimum 4.5:1 for normal text |
| `semantic.text.disabled` | Unavailable label | `{alias.palette.mediator.mid}` | Disabled | Dark default | Do not lower opacity below legibility floor |
| `semantic.text.link` | Inline link | `{alias.palette.thermal.cool.primary}` | Default | Dark default | Underline in body text; colour is supplemental |
| `semantic.border.subtle` | Nonessential separation | `{alias.palette.field.lifted}` | Default | Dark default | Not for focus or essential graphics |
| `semantic.border.standard` | Essential component boundary | `{alias.palette.thermal.cool.mid}` | Default | Dark default | Target 3:1 for essential non-text boundaries |
| `semantic.border.strong` | Emphasis/selected boundary | `{alias.palette.thermal.cool.primary}` | Emphasis | Dark default | Shape or marker accompanies selection |
| `semantic.border.focus` | Keyboard focus | `{alias.palette.convergence.cool}` | Focus | Dark default | Solid 2px minimum with offset; 3:1 against adjacent colours |
| `semantic.icon.primary` | Ordinary functional icon | `{alias.palette.convergence.cool}` | Default | Dark default | Accessible name where interactive |
| `semantic.icon.secondary` | Supporting icon | `{alias.palette.thermal.cool.primary}` | Default | Dark default | Never the only carrier of meaning |
| `semantic.icon.selected` | Persistent selected mark | `{alias.palette.field.deep}` | Selected | Dark default | Used on pale selected/accent surface with label/state |
| `semantic.icon.disabled` | Unavailable icon | `{alias.palette.mediator.mid}` | Disabled | Dark default | Target remains noninteractive and state is announced |

### Action, Focus, Selection, And Feedback

| Token | Intent | Default value | State | Mode | Required contrast/behavior |
| --- | --- | --- | --- | --- | --- |
| `semantic.action.primary.surface` | Primary action | `{alias.palette.thermal.hot.primary}` | Default | Dark default | At most one primary action per local decision group |
| `semantic.action.primary.foreground` | Primary action label/icon | `{alias.palette.field.deep}` | Default | Dark default | Validate normal-text contrast |
| `semantic.action.primary.hover` | Pointer hover on primary | `{alias.palette.thermal.hot.highlight}` | Hover | Dark default | Also change boundary/value; no layout shift |
| `semantic.action.primary.pressed` | Committed press | `{alias.palette.thermal.hot.shadow}` | Pressed | Dark default | Brief response under 140ms |
| `semantic.action.secondary.surface` | Secondary action | `{alias.palette.field.lifted}` | Default | Dark default | Clear boundary against canvas |
| `semantic.action.secondary.foreground` | Secondary action label/icon | `{alias.palette.convergence.cool}` | Default | Dark default | Same legibility obligation as primary |
| `semantic.action.destructive.surface` | Consequential destructive action | `{alias.palette.thermal.hot.dark}` | Default | All modes | Never relies on colour; copy names consequence |
| `semantic.action.destructive.foreground` | Destructive label/icon | `{alias.palette.convergence.cool}` | Default | All modes | Validate 4.5:1 at actual render |
| `semantic.action.disabled.surface` | Disabled action surface | `{semantic.surface.disabled}` | Disabled | Any | No hover/press behavior |
| `semantic.action.disabled.foreground` | Disabled label/icon | `{semantic.text.disabled}` | Disabled | Any | Readable and programmatically disabled |
| `semantic.selection.surface` | Persistent selection region | `{alias.palette.thermal.cool.primary}` | Selected | Dark default | Add check/marker and accessible state |
| `semantic.selection.foreground` | Selected content foreground | `{alias.palette.field.deep}` | Selected | Dark default | Preserve text/icon contrast |
| `semantic.focus.ring` | Focus indicator colour | `{semantic.border.focus}` | Focus | Dark default | Never rendered as blur or glow |
| `semantic.focus.offset` | Separation around focus ring | `{alias.space.optical}` | Focus | Any | 4px target offset where geometry allows |
| `semantic.status.info.accent` | Informational state | `{alias.palette.thermal.cool.primary}` | Info | Dark default | Pair with info icon and label |
| `semantic.status.success.accent` | Completed state | `{alias.palette.mediator.warm}` | Success | Dark default | Pair with check and completion copy; not colour-only |
| `semantic.status.warning.accent` | Consequential caution | `{alias.palette.thermal.hot.highlight}` | Warning | Dark default | Pair with warning icon and consequence |
| `semantic.status.error.accent` | Failure or invalid state | `{alias.palette.thermal.hot.dark}` | Error | Any | Pair with error icon, message, and recovery |
| `semantic.status.foreground` | Text on status plate | `{alias.palette.convergence.cool}` | Any status | Dark default | Validate per status surface; allow dark foreground on pale accents |
| `semantic.progress.track` | Progress background | `{alias.palette.field.lifted}` | Loading | Dark default | Stable nonanimated track |
| `semantic.progress.value` | Determinate progress | `{alias.palette.thermal.cool.primary}` | Loading | Dark default | Provide numeric/text progress when useful |

The brand palette is not a universal status taxonomy. Domain or platform implementation may substitute conventional, research-tested status hues at the mode/platform layer, but must preserve token intent, contrast, icon, label, and recovery behavior.

### Typography And Layout

| Token | Intent | Default value | State | Mode | Required contrast/behavior |
| --- | --- | --- | --- | --- | --- |
| `semantic.type.display.family` | Rare editorial display | `{alias.type.family.editorial}` | Default | Any | May fall back to interface family |
| `semantic.type.display.size` | Hero title scale | `clamp(2.5rem, 6vw, {alias.type.size.display})` | Default | Responsive | Maximum 8–12 words |
| `semantic.type.display.weight` | Hero title weight | `{alias.type.weight.display}` | Default | Any | No textured or outline fill |
| `semantic.type.display.line` | Hero title rhythm | `{alias.type.line.compact}` | Default | Any | Short lines only |
| `semantic.type.heading.family` | Section heading voice | `{alias.type.family.interface}` | Default | Any | Stable across modes |
| `semantic.type.heading.size` | Section heading scale | `{alias.type.size.heading.large}` | Default | Responsive | May step down on compact screens |
| `semantic.type.heading.weight` | Section heading weight | `{alias.type.weight.display}` | Default | Any | Avoid unnecessary all caps |
| `semantic.type.heading.line` | Heading rhythm | `{alias.type.line.heading}` | Default | Any | Supports wrapping/localization |
| `semantic.type.body.family` | Primary reading voice | `{alias.type.family.interface}` | Default | Any | Open apertures and script coverage |
| `semantic.type.body.size` | Primary body scale | `{alias.type.size.body}` | Default | Any | Honour user scaling; 1rem floor |
| `semantic.type.body.weight` | Primary body weight | `{alias.type.weight.body}` | Default | Any | 400 minimum target |
| `semantic.type.body.line` | Primary body rhythm | `{alias.type.line.reading}` | Default | Any | 1.5–1.7 acceptable override |
| `semantic.type.label.size` | Control label scale | `{alias.type.size.label}` | Default | Any | Increase when platform requires |
| `semantic.type.label.weight` | Control label weight | `{alias.type.weight.control}` | Default | Any | Sentence case |
| `semantic.type.caption.size` | Metadata scale | `{alias.type.size.caption}` | Default | Any | Not for essential instructions alone |
| `semantic.layout.inline-gap` | Icon-label gap | `{alias.space.inline}` | Default | Any | 6–8px target |
| `semantic.layout.control-padding` | Compact control inset | `{alias.space.control}` | Default | Any | Touch target remains independent |
| `semantic.layout.content-inset` | Ordinary content inset | `{alias.space.panel}` | Default | Any | May reduce to group spacing on compact |
| `semantic.layout.section-gap` | Section separation | `{alias.space.section}` | Default | Any | Preserve grouping at zoom/reflow |
| `semantic.layout.scene-gap` | Expressive scene breathing room | `{alias.space.scene}` | Default | Editorial | May use proportional expansion on wide screens |
| `semantic.layout.void-gap` | Maximum deliberate negative space | `{alias.space.void}` | Default | Editorial | Never creates unreachable controls |

### Surface Treatment And Motion

| Token | Intent | Default value | State | Mode | Required contrast/behavior |
| --- | --- | --- | --- | --- | --- |
| `semantic.imagery.field` | Identity-bearing dark field | `{alias.palette.field.deep}` | Default | Identity media | Holds the structural void |
| `semantic.imagery.subject.core` | Recognizable dark subject mass | `{alias.palette.field.deep}` | Default | Identity media | Remains opaque enough for thumbnail recognition |
| `semantic.imagery.light.hot` | Dominant or secondary warm territory | `{alias.palette.thermal.hot.primary}` | Default | Identity media | Relational, not status-bearing |
| `semantic.imagery.light.hot.highlight` | Warm luminous step | `{alias.palette.thermal.hot.highlight}` | Default | Identity media | Localized to edge, ground, or focal pool |
| `semantic.imagery.light.cool` | Dominant or secondary cool territory | `{alias.palette.thermal.cool.primary}` | Default | Identity media | Relational, not status-bearing |
| `semantic.imagery.light.cool.mid` | Cool atmospheric step | `{alias.palette.thermal.cool.mid}` | Default | Identity media | Haze and depth only; not small text |
| `semantic.imagery.light.convergence` | Scarce pale intersection | `{alias.palette.convergence.cool}` | Focal | Identity media | Attached to the primary event |
| `semantic.imagery.mediator` | Dust-like warm/cool bridge | `{alias.palette.mediator.warm}` | Default | Identity media | Avoid smooth neutral blending |
| `semantic.imagery.ratio.master` | Portrait-first identity plate | `{alias.media.ratio.identity}` | Default | Identity media | Derived crops protect recognition core |
| `semantic.imagery.dark.min` | Minimum dark structural occupancy | `{alias.media.dark.min}` | Default | Identity media | Review below 50% |
| `semantic.imagery.dark.max` | Ordinary dark structural target | `{alias.media.dark.max}` | Default | Identity media | May exceed for intentionally sparse variants |
| `semantic.imagery.peak.max` | Pale convergence ceiling | `{alias.media.peak.max}` | Focal | Identity media | Review above 5% |
| `semantic.texture.functional` | Text/control clarity | `{alias.media.texture.none}` | Any | Any | Zero grain, bloom, and channel shift |
| `semantic.texture.shell` | Matte dark field | `{alias.media.texture.matte}` | Default | Dark | Maximum 1.5% luminance texture |
| `semantic.texture.identity.min` | Identity grain floor | `{alias.media.texture.identity.low}` | Default | Identity media | 3% start at master scale |
| `semantic.texture.identity.max` | Identity grain ceiling | `{alias.media.texture.identity.high}` | Default | Identity media | Review before exceeding 6% |
| `semantic.motion.feedback.duration` | Immediate feedback | `{alias.motion.feedback}` | Interaction | Default motion | Must begin within 100ms |
| `semantic.motion.reveal.duration` | Ordinary disclosure | `{alias.motion.reveal}` | Expanded | Default motion | Under 300ms |
| `semantic.motion.axis.duration` | Spatial transition | `{alias.motion.axis}` | Navigation | Default motion | Under 500ms for routine product use |
| `semantic.motion.editorial.duration` | Optional atmospheric reveal | `{alias.motion.editorial}` | Editorial | Default motion | Nonessential and user-controllable |
| `semantic.motion.response.easing` | Direct response curve | `{alias.motion.ease.response}` | Interaction | Default motion | No spring |
| `semantic.motion.reveal.easing` | Disclosure curve | `{alias.motion.ease.reveal}` | Expanded | Default motion | Decelerating |
| `semantic.motion.axis.easing` | Directional transition curve | `{alias.motion.ease.axis}` | Navigation | Default motion | Preserve governing axis |
| `semantic.motion.exit.easing` | Dismissal curve | `{alias.motion.ease.exit}` | Exit | Default motion | Faster than entry |

## Intent-Family Rules

- Text, surface, border, icon, action, feedback, status, focus, selection, data, and overlay tokens name intent rather than appearance.
- No semantic token may include `orange`, `cyan`, `cowboy`, page name, or component name.
- Status tokens always specify the required non-colour encoding and copy behavior.
- Semantic motion tokens describe purpose; reduced-motion mode may replace their values without changing component contracts.
- If a semantic token cannot be described without naming a component, it belongs in the component layer.

## Anti-Patterns

- Binding a button, card, dialog, or scene directly to an alias/global/primitive token.
- Using `semantic.status.error.accent` as a decorative brand red or `semantic.action.primary.surface` as a generic orange.
- Creating separate semantic names for visually identical states without a behavioral difference.
- Encoding selection, status, ownership, or direction only through colour.
- Overriding semantic values in local CSS, generated prompts, or platform code without a mode or transform record.
