# Mode Tokens

Output path: `tokens/mode-tokens.md`

Modes compose orthogonally: colour scheme (`light` or `dark`), contrast preference (`standard` or `high contrast`), and motion preference (`full` or `reduced`). The matrix shows the effective override for each concern; `—` means the current colour-mode value is retained.

## Theme Mode Matrix

### Surfaces And Foregrounds

| Token | Light mode | Dark mode | High contrast mode | Reduced motion mode | Notes |
| --- | --- | --- | --- | --- | --- |
| `semantic.surface.canvas` | `{alias.palette.shell.light}` | `{alias.palette.field.deep}` | `Canvas` | — | Dark is the identity-bearing mode; light is a matte translation |
| `semantic.surface.canvas.alternate` | `{alias.palette.convergence.warm}` | `{alias.palette.field.alternate}` | `Canvas` | — | Add boundary in high contrast |
| `semantic.surface.raised` | `{alias.palette.convergence.cool}` | `{alias.palette.field.lifted}` | `Canvas` | — | Elevation uses system border/shadow in high contrast |
| `semantic.surface.overlay` | `{alias.palette.shell.light}` | `{alias.palette.field.deep}` | `Canvas` | — | Opaque behind text in every mode |
| `semantic.surface.critical` | `{alias.palette.shell.light}` | `{alias.palette.field.deep}` | `Canvas` | — | Zero texture and bloom |
| `semantic.surface.disabled` | `{alias.palette.convergence.warm}` | `{alias.palette.field.alternate}` | `Canvas` | — | Use system disabled semantics where available |
| `semantic.surface.scrim` | `rgb(18 19 19 / 0.52)` | `rgb(13 14 14 / 0.72)` | `Canvas` at `0.85` opacity | — | Background must become inert |
| `semantic.text.primary` | `{alias.palette.ink.light-mode}` | `{alias.palette.convergence.cool}` | `CanvasText` | — | Primary text pair is validated per mode |
| `semantic.text.secondary` | `{alias.palette.thermal.cool.dark}` | `{alias.palette.thermal.cool.primary}` | `CanvasText` | — | Do not express hierarchy through opacity alone |
| `semantic.text.muted` | `{alias.palette.thermal.hot.shadow}` | `{alias.palette.mediator.mid}` | `GrayText` | — | Must remain readable |
| `semantic.text.inverse` | `{alias.palette.convergence.cool}` | `{alias.palette.field.deep}` | `HighlightText` | — | Used only on validated opposing surface |
| `semantic.text.on-accent` | `{alias.palette.convergence.cool}` | `{alias.palette.field.deep}` | `HighlightText` | — | Light-mode primary surface is darker |
| `semantic.text.disabled` | `{alias.palette.thermal.hot.shadow}` | `{alias.palette.mediator.mid}` | `GrayText` | — | Programmatic state remains required |
| `semantic.text.link` | `{alias.palette.thermal.cool.dark}` | `{alias.palette.thermal.cool.primary}` | `LinkText` | — | Underline body links |
| `semantic.icon.primary` | `{alias.palette.ink.light-mode}` | `{alias.palette.convergence.cool}` | `CanvasText` | — | No duotone in high contrast |
| `semantic.icon.secondary` | `{alias.palette.thermal.cool.dark}` | `{alias.palette.thermal.cool.primary}` | `CanvasText` | — | Essential icons require labels/accessible names |

### Boundaries, Actions, Selection, And Status

| Token | Light mode | Dark mode | High contrast mode | Reduced motion mode | Notes |
| --- | --- | --- | --- | --- | --- |
| `semantic.border.subtle` | `{alias.palette.mediator.mid}` | `{alias.palette.field.lifted}` | `CanvasText` | — | May be omitted only when nonessential |
| `semantic.border.standard` | `{alias.palette.thermal.cool.dark}` | `{alias.palette.thermal.cool.mid}` | `CanvasText` | — | Essential graphics target 3:1 |
| `semantic.border.strong` | `{alias.palette.ink.light-mode}` | `{alias.palette.thermal.cool.primary}` | `CanvasText` | — | Used with shape/marker |
| `semantic.border.focus` | `{alias.palette.thermal.hot.dark}` | `{alias.palette.convergence.cool}` | `Highlight` | — | Solid 2px minimum plus offset |
| `semantic.focus.ring` | `{semantic.border.focus}` | `{semantic.border.focus}` | `Highlight` | — | Never glow or blur |
| `semantic.action.primary.surface` | `{alias.palette.thermal.hot.dark}` | `{alias.palette.thermal.hot.primary}` | `Highlight` | — | One primary per decision group |
| `semantic.action.primary.foreground` | `{alias.palette.convergence.cool}` | `{alias.palette.field.deep}` | `HighlightText` | — | Validate at actual render |
| `semantic.action.primary.hover` | `{alias.palette.thermal.hot.shadow}` | `{alias.palette.thermal.hot.highlight}` | `Highlight` | — | Add non-colour state change |
| `semantic.action.primary.pressed` | `{alias.palette.field.deep}` | `{alias.palette.thermal.hot.shadow}` | `Highlight` | — | Brief response |
| `semantic.action.secondary.surface` | `{alias.palette.convergence.cool}` | `{alias.palette.field.lifted}` | `Canvas` | — | Strong system border in high contrast |
| `semantic.action.secondary.foreground` | `{alias.palette.ink.light-mode}` | `{alias.palette.convergence.cool}` | `CanvasText` | — | Same legibility obligation |
| `semantic.action.destructive.surface` | `{alias.palette.thermal.hot.dark}` | `{alias.palette.thermal.hot.dark}` | `Highlight` or platform danger colour | — | Explicit copy and recovery required |
| `semantic.action.destructive.foreground` | `{alias.palette.convergence.cool}` | `{alias.palette.convergence.cool}` | `HighlightText` | — | Verify contrast on platform override |
| `semantic.selection.surface` | `{alias.palette.thermal.cool.dark}` | `{alias.palette.thermal.cool.primary}` | `Highlight` | — | Check/marker and accessible state accompany colour |
| `semantic.selection.foreground` | `{alias.palette.convergence.cool}` | `{alias.palette.field.deep}` | `HighlightText` | — | Stable selected state |
| `semantic.status.info.accent` | `{alias.palette.thermal.cool.dark}` | `{alias.palette.thermal.cool.primary}` | `LinkText` or system info | — | Icon plus label |
| `semantic.status.success.accent` | `{alias.palette.thermal.cool.dark}` | `{alias.palette.mediator.warm}` | System success colour or `CanvasText` | — | Check plus completion copy |
| `semantic.status.warning.accent` | `{alias.palette.thermal.hot.dark}` | `{alias.palette.thermal.hot.highlight}` | System warning colour or `CanvasText` | — | Warning icon plus consequence |
| `semantic.status.error.accent` | `{alias.palette.thermal.hot.dark}` | `{alias.palette.thermal.hot.dark}` | System error colour or `CanvasText` | — | Error icon, message, and recovery |
| `semantic.progress.track` | `{alias.palette.convergence.warm}` | `{alias.palette.field.lifted}` | `Canvas` with `CanvasText` boundary | — | Stable track |
| `semantic.progress.value` | `{alias.palette.thermal.cool.dark}` | `{alias.palette.thermal.cool.primary}` | `Highlight` | — | Numeric/text progress where useful |

### Imagery And Texture

| Token | Light mode | Dark mode | High contrast mode | Reduced motion mode | Notes |
| --- | --- | --- | --- | --- | --- |
| `semantic.imagery.field` | `{alias.palette.shell.light}` for support imagery; retain dark field for identity plates | `{alias.palette.field.deep}` | `Canvas` | — | Light mode does not automatically invert identity artwork |
| `semantic.imagery.subject.core` | `{alias.palette.ink.light-mode}` | `{alias.palette.field.deep}` | `CanvasText` | — | Contour remains primary |
| `semantic.imagery.light.hot` | `{alias.palette.thermal.hot.dark}` | `{alias.palette.thermal.hot.primary}` | `Highlight` or `CanvasText` | — | Not a status role |
| `semantic.imagery.light.cool` | `{alias.palette.thermal.cool.dark}` | `{alias.palette.thermal.cool.primary}` | `CanvasText` | — | Not a status role |
| `semantic.imagery.light.convergence` | `{alias.palette.shell.light}` or `{alias.palette.convergence.cool}` by plate | `{alias.palette.convergence.cool}` | `CanvasText` | — | Keep area scarce |
| `semantic.texture.functional` | `{alias.media.texture.none}` | `{alias.media.texture.none}` | `{alias.media.texture.none}` | `{alias.media.texture.none}` | Always clean |
| `semantic.texture.shell` | `{alias.media.texture.none}` | `{alias.media.texture.matte}` | `{alias.media.texture.none}` | — | Light/high contrast remove shell grain |
| `semantic.texture.identity.min` | `{alias.media.texture.identity.low}` | `{alias.media.texture.identity.low}` | `{alias.media.texture.none}` | — | High contrast uses clean masses |
| `semantic.texture.identity.max` | `{alias.media.texture.identity.high}` | `{alias.media.texture.identity.high}` | `{alias.media.texture.none}` | — | Never behind essential content |

### Motion

| Token | Light mode | Dark mode | High contrast mode | Reduced motion mode | Notes |
| --- | --- | --- | --- | --- | --- |
| `semantic.motion.feedback.duration` | `{alias.motion.feedback}` | `{alias.motion.feedback}` | `{alias.motion.feedback}` | `80ms` or immediate | Preserve acknowledgement |
| `semantic.motion.reveal.duration` | `{alias.motion.reveal}` | `{alias.motion.reveal}` | `{alias.motion.reveal}` | `100ms` opacity or immediate | No spatial travel required |
| `semantic.motion.axis.duration` | `{alias.motion.axis}` | `{alias.motion.axis}` | `{alias.motion.axis}` | `0–100ms` | Replace with cut or short fade |
| `semantic.motion.editorial.duration` | `{alias.motion.editorial}` | `{alias.motion.editorial}` | `0ms` by default | `0ms` | Optional atmosphere disabled |
| `semantic.motion.response.easing` | `{alias.motion.ease.response}` | `{alias.motion.ease.response}` | `{alias.motion.ease.response}` | `linear` | Avoid spring |
| `semantic.motion.reveal.easing` | `{alias.motion.ease.reveal}` | `{alias.motion.ease.reveal}` | `{alias.motion.ease.reveal}` | `linear` | State cue remains |
| `semantic.motion.axis.easing` | `{alias.motion.ease.axis}` | `{alias.motion.ease.axis}` | `{alias.motion.ease.axis}` | `linear` | No implied travel |
| `semantic.motion.exit.easing` | `{alias.motion.ease.exit}` | `{alias.motion.ease.exit}` | `{alias.motion.ease.exit}` | `linear` | Immediate or brief fade |

## Mode Activation

- Light/dark follows explicit user choice first, then platform preference. Do not force dark mode because it carries more identity.
- High contrast and forced colours override both light and dark appearance where the platform exposes them.
- Reduced motion is evaluated independently from colour and contrast and applies from first render.
- Identity imagery may remain dark inside a light product shell if it has an accessible boundary and all functional content sits outside or on a stable support plate.
- Persist user overrides, avoid flashes of the wrong theme, and expose mode metadata to embedded content where safe.

## Adaptation Rules

- Dark mode is not inversion: it preserves the carbon majority, selective chroma, scarce peak light, and low elevation.
- Light mode is not a washed-out scene: it uses matte parchment, carbon ink, and compact darker accents. Full identity plates may stay dark.
- High contrast is a separate mode: system colours, solid boundaries, zero grain/bloom on functional content, and redundant state encoding.
- Reduced motion replaces travel, parallax, ambient drift, and long fades with static hierarchy, immediate cuts, labels, and stable state markers.
- A platform status override may introduce conventional system colours, but the semantic token name and recovery contract stay fixed.

## Anti-Patterns

- Implementing light mode by inverting pixels or dark mode by lowering every lightness equally.
- Treating high contrast as “more saturated” or reduced motion as simply setting `animation-duration: 0` without state cues.
- Mode-specific component names, local hex overrides, or a second token tree per platform.
- Recolouring identity imagery automatically without checking recognition, cultural meaning, and crop.
- Forcing dark mode, ignoring user preferences, or rendering a wrong-theme flash before hydration.
