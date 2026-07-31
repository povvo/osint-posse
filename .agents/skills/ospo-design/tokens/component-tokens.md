# Component Tokens

Output path: `tokens/component-tokens.md`

Each component property binds to a semantic token. Component implementations may expose the `component.*` token as a customization point, but its default must remain a semantic reference. Mode changes occur upstream; a component must not branch on raw colours or primitives.

## Component Token Contract

### Action Controls

| Component | Part | Property | Component token | Semantic token | State or variant | Override rule |
| --- | --- | --- | --- | --- | --- | --- |
| Button | Container | Background | `component.button.primary.background` | `{semantic.action.primary.surface}` | Primary/default | Override only through an approved semantic action role |
| Button | Label/icon | Colour | `component.button.primary.foreground` | `{semantic.action.primary.foreground}` | Primary/default | Keep text and icon synchronized |
| Button | Container | Background | `component.button.primary.hover.background` | `{semantic.action.primary.hover}` | Primary/hover | Pointer only; focus remains independent |
| Button | Container | Background | `component.button.primary.pressed.background` | `{semantic.action.primary.pressed}` | Primary/pressed | Return within feedback duration |
| Button | Container | Background | `component.button.secondary.background` | `{semantic.action.secondary.surface}` | Secondary/default | Never promoted by local colour override |
| Button | Label/icon | Colour | `component.button.secondary.foreground` | `{semantic.action.secondary.foreground}` | Secondary/default | Same contrast obligation as primary |
| Button | Container | Background | `component.button.destructive.background` | `{semantic.action.destructive.surface}` | Destructive/default | Requires explicit consequence copy |
| Button | Label/icon | Colour | `component.button.destructive.foreground` | `{semantic.action.destructive.foreground}` | Destructive/default | Do not use for non-destructive emphasis |
| Button | Container | Background | `component.button.disabled.background` | `{semantic.action.disabled.surface}` | Disabled | No hover/press token |
| Button | Label/icon | Colour | `component.button.disabled.foreground` | `{semantic.action.disabled.foreground}` | Disabled | Remains readable |
| Button | Focus indicator | Colour | `component.button.focus.ring` | `{semantic.focus.ring}` | Focus-visible | Solid ring, never glow |
| Button | Content | Gap | `component.button.content.gap` | `{semantic.layout.inline-gap}` | All | Preserve through localization |
| Button | Container | Inline/block padding | `component.button.padding` | `{semantic.layout.control-padding}` | All | May scale by density; target floor remains |
| Button | Feedback | Duration | `component.button.feedback.duration` | `{semantic.motion.feedback.duration}` | Press | Reduced-motion mode may shorten |

### Form Controls

| Component | Part | Property | Component token | Semantic token | State or variant | Override rule |
| --- | --- | --- | --- | --- | --- | --- |
| Text field | Container | Background | `component.field.background` | `{semantic.surface.canvas.alternate}` | Default | Opaque behind text |
| Text field | Input text | Colour | `component.field.value` | `{semantic.text.primary}` | Default | Never rendered with opacity |
| Text field | Label | Colour | `component.field.label` | `{semantic.text.secondary}` | Default | Visible label preferred |
| Text field | Help text | Colour | `component.field.help` | `{semantic.text.muted}` | Default | Programmatically associated |
| Text field | Boundary | Colour | `component.field.border` | `{semantic.border.standard}` | Default | Essential boundary targets 3:1 |
| Text field | Boundary | Colour | `component.field.focus.border` | `{semantic.border.focus}` | Focus-visible | Focus ring is additional, not colour-only |
| Text field | Focus indicator | Colour | `component.field.focus.ring` | `{semantic.focus.ring}` | Focus-visible | Crisp 2px minimum |
| Text field | Boundary | Colour | `component.field.error.border` | `{semantic.status.error.accent}` | Error | Pair with icon and message |
| Text field | Error icon | Colour | `component.field.error.icon` | `{semantic.status.error.accent}` | Error | Decorative duplicate hidden if message covers semantics |
| Text field | Error message | Colour | `component.field.error.text` | `{semantic.text.primary}` | Error | Never colour-only |
| Text field | Disabled surface | Background | `component.field.disabled.background` | `{semantic.surface.disabled}` | Disabled | Retain content visibility |

### Navigation And Selection

| Component | Part | Property | Component token | Semantic token | State or variant | Override rule |
| --- | --- | --- | --- | --- | --- | --- |
| Navigation item | Label | Colour | `component.nav.label` | `{semantic.text.secondary}` | Default | Visible label required for unfamiliar destination |
| Navigation item | Label | Colour | `component.nav.label.selected` | `{semantic.text.inverse}` | Selected | Used with selected surface and state |
| Navigation item | Container | Background | `component.nav.surface.selected` | `{semantic.selection.surface}` | Selected | Pair with marker or current-page semantics |
| Navigation item | Icon | Colour | `component.nav.icon` | `{semantic.icon.secondary}` | Default | Does not replace label |
| Navigation item | Focus indicator | Colour | `component.nav.focus.ring` | `{semantic.focus.ring}` | Focus-visible | Independent of selected state |
| Choice | Container | Background | `component.choice.selected.background` | `{semantic.selection.surface}` | Selected | Pair with check and accessible state |
| Choice | Mark | Colour | `component.choice.selected.mark` | `{semantic.icon.selected}` | Selected | Remains visible without colour perception |
| Choice | Label | Colour | `component.choice.label` | `{semantic.text.primary}` | All | Label toggles the control |

### Feedback, Progress, And Overlay

| Component | Part | Property | Component token | Semantic token | State or variant | Override rule |
| --- | --- | --- | --- | --- | --- | --- |
| Status message | Container | Background | `component.status.background` | `{semantic.surface.raised}` | All statuses | Status type is not background colour alone |
| Status message | Icon/border | Colour | `component.status.info.accent` | `{semantic.status.info.accent}` | Info | Pair with info label/icon |
| Status message | Icon/border | Colour | `component.status.success.accent` | `{semantic.status.success.accent}` | Success | Pair with check and completion copy |
| Status message | Icon/border | Colour | `component.status.warning.accent` | `{semantic.status.warning.accent}` | Warning | Pair with consequence |
| Status message | Icon/border | Colour | `component.status.error.accent` | `{semantic.status.error.accent}` | Error | Pair with problem and recovery |
| Status message | Copy | Colour | `component.status.text` | `{semantic.text.primary}` | All statuses | Announce according to urgency |
| Progress | Track | Background | `component.progress.track` | `{semantic.progress.track}` | Loading | Stable, nonpulsing track |
| Progress | Value | Background | `component.progress.value` | `{semantic.progress.value}` | Determinate | Add numeric or text progress when useful |
| Progress | Label | Colour | `component.progress.label` | `{semantic.text.secondary}` | All | Names the task |
| Panel | Container | Background | `component.panel.background` | `{semantic.surface.raised}` | Default | Functional content remains clean |
| Panel | Boundary | Colour | `component.panel.border` | `{semantic.border.subtle}` | Default | Omit if value separation suffices |
| Panel | Content | Padding | `component.panel.padding` | `{semantic.layout.content-inset}` | Default | May reduce at compact breakpoint |
| Dialog | Container | Background | `component.dialog.background` | `{semantic.surface.overlay}` | Open | Opaque enough for stable contrast |
| Dialog | Scrim | Background | `component.dialog.scrim` | `{semantic.surface.scrim}` | Open | Background becomes inert |
| Dialog | Heading | Colour | `component.dialog.heading` | `{semantic.text.primary}` | Open | Focus starts at meaningful content/control |
| Dialog | Focus indicator | Colour | `component.dialog.focus.ring` | `{semantic.focus.ring}` | Focus-visible | Trap focus only while modal |

### Expressive Scene Modules

| Component | Part | Property | Component token | Semantic token | State or variant | Override rule |
| --- | --- | --- | --- | --- | --- | --- |
| Scene plate | Field | Background | `component.scene.field` | `{semantic.imagery.field}` | All | Dark structural majority remains |
| Scene plate | Frame | Aspect ratio | `component.scene.ratio` | `{semantic.imagery.ratio.master}` | Master | Derived ratios require crop review |
| Scene plate | Atmosphere | Minimum grain | `component.scene.texture.min` | `{semantic.texture.identity.min}` | Identity | Scale with delivered resolution |
| Scene plate | Atmosphere | Maximum grain | `component.scene.texture.max` | `{semantic.texture.identity.max}` | Identity | Mask away from information layer |
| Scene plate | Field | Minimum dark ratio | `component.scene.dark.min` | `{semantic.imagery.dark.min}` | Identity | Review below threshold |
| Scene plate | Field | Ordinary dark target | `component.scene.dark.max` | `{semantic.imagery.dark.max}` | Identity | May exceed for sparse variants |
| Silhouette subject | Core | Fill | `component.subject.core` | `{semantic.imagery.subject.core}` | All | Remains contour-legible without rim |
| Silhouette subject | Warm rim | Colour | `component.subject.rim.hot` | `{semantic.imagery.light.hot}` | Warm-lit | Local edge stain, not uniform outline |
| Silhouette subject | Cool rim | Colour | `component.subject.rim.cool` | `{semantic.imagery.light.cool}` | Cool-lit | Local edge stain, not uniform outline |
| Light pool | Dominant field | Colour | `component.light-pool.hot` | `{semantic.imagery.light.hot}` | Warm-dominant | May invert with cool counterpart |
| Light pool | Counterfield | Colour | `component.light-pool.cool` | `{semantic.imagery.light.cool}` | Cool-dominant | Area remains unequal |
| Light pool | Peak | Colour | `component.light-pool.peak` | `{semantic.imagery.light.convergence}` | Focal | Attached to primary event |
| Light pool | Peak | Maximum area | `component.light-pool.peak.max` | `{semantic.imagery.peak.max}` | Focal | Review above 5% |
| Gathering | Center | Colour | `component.gathering.center` | `{semantic.imagery.light.convergence}` | Luminous center | Bodies occlude or bracket the pool |
| Gathering | Participants | Fill | `component.gathering.subject` | `{semantic.imagery.subject.core}` | All | Count and relationship remain legible |
| Procession | Route | Colour | `component.procession.route` | `{semantic.imagery.light.hot}` | Warm-route default | Cool-dominant variant may repoint semantically |
| Procession | Repetitions | Fill | `component.procession.subject` | `{semantic.imagery.subject.core}` | All | Scale decays with irregular spacing |
| Scene support plate | Container | Background | `component.scene-support.background` | `{semantic.surface.overlay}` | Text/control | Blocks texture and bloom |
| Scene support plate | Copy | Colour | `component.scene-support.text` | `{semantic.text.primary}` | Text/control | Contrast independent of crop |

## Component Token Families

- **Action controls:** primary, secondary, destructive, disabled, and focus-visible states.
- **Form controls:** label, value, help, boundary, focus, invalid, and disabled anatomy.
- **Navigation and selection:** default, current, selected, focus, and compact behavior.
- **Feedback and status:** info, success, warning, error, progress, retry, and recovery.
- **Content and data display:** panels, overlays, text hierarchy, and clean support surfaces.
- **Domain modules:** scene plate, silhouette subject, light pool, gathering, procession, and scene support plate.

## Override Rules

- A component override must reference another compatible `semantic.*` token and document the purpose-bearing variant.
- Local raw values, opacity hacks, and primitive/global/alias references are rejected in review.
- Platform variants may transform units, focus rendering, and typography while preserving semantic intent.
- Mode overrides happen in the semantic or mode layer; component token names remain stable.
- Generated UI must use these contracts or explicitly report a component gap.

## Anti-Patterns

- `component.button.background: #E85A2F` or any raw/global/alias binding.
- A decorative component variant with no behavioral or content purpose.
- Status components that swap only colour, scene components that expose only a generic “style” prop, or focus defined by blur.
- One component token reused across unrelated anatomy merely because the current values match.
- Local application overrides that bypass mode, platform, contrast, or reduced-motion transforms.
