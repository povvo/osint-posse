# Alias Tokens

Output path: `tokens/alias-tokens.md`

Aliases name stable design materials and shield semantic intent from raw scale changes. Alias chains are one hop: each alias target is a global token, and semantic or mode tokens may then reference the alias. Components must never consume aliases directly.

## Alias Map

### Palette And Surface

| Token | Alias target | Reason | Allowed consumers |
| --- | --- | --- | --- |
| `alias.palette.field.deep` | `{global.color.carbon.950}` | Stable absorptive field independent of a raw shade number | Semantic surfaces, mode tokens, media transforms |
| `alias.palette.field.alternate` | `{global.color.carbon.900}` | Separates a second dark plane without inventing elevation | Semantic surfaces, mode tokens |
| `alias.palette.field.lifted` | `{global.color.carbon.800}` | Highest routine dark support material | Semantic surfaces, borders |
| `alias.palette.thermal.hot.primary` | `{global.color.ember.500}` | Primary expressive warm territory | Semantic accents, imagery, mode tokens |
| `alias.palette.thermal.hot.highlight` | `{global.color.ember.400}` | Accessible lighter warm and bloom step | Semantic accents, imagery |
| `alias.palette.thermal.hot.dark` | `{global.color.ember.700}` | Warm role that survives a light shell | Light-mode semantic accents |
| `alias.palette.thermal.hot.shadow` | `{global.color.umber.600}` | Chromatic warm shadow and mediation | Imagery and surface transforms |
| `alias.palette.thermal.cool.primary` | `{global.color.mineral.300}` | Pale mineral territory and luminous support | Semantic foreground, imagery |
| `alias.palette.thermal.cool.mid` | `{global.color.mineral.500}` | Restrained cool atmosphere | Imagery, non-text surfaces |
| `alias.palette.thermal.cool.dark` | `{global.color.mineral.700}` | Cool role that survives a light shell | Light-mode semantic accents |
| `alias.palette.mediator.warm` | `{global.color.sand.300}` | Dust-like bridge and secondary pale foreground | Semantic foreground, imagery |
| `alias.palette.mediator.mid` | `{global.color.sand.500}` | Muted warm bridge | Non-text surfaces, imagery |
| `alias.palette.convergence.cool` | `{global.color.frost.100}` | Scarce pale convergence and primary dark-mode text | Semantic foreground, focus, imagery |
| `alias.palette.convergence.warm` | `{global.color.parchment.100}` | Warm convergence alternative | Semantic foreground, imagery |
| `alias.palette.shell.light` | `{global.color.parchment.50}` | Matte light-mode base | Mode tokens |
| `alias.palette.ink.light-mode` | `{global.color.ink.950}` | Stable light-mode foreground | Mode tokens |

### Typography

| Token | Alias target | Reason | Allowed consumers |
| --- | --- | --- | --- |
| `alias.type.family.interface` | `{global.font.family.primary}` | Durable functional voice | Semantic type roles, platform transforms |
| `alias.type.family.editorial` | `{global.font.family.editorial}` | Optional display texture | Semantic display roles |
| `alias.type.family.data` | `{global.font.family.data}` | Clearly scoped structured-data voice | Semantic data roles |
| `alias.type.size.caption` | `{global.font.size.200}` | Stable small factual step | Semantic caption/data |
| `alias.type.size.label` | `{global.font.size.300}` | Stable control-label step | Semantic label/control |
| `alias.type.size.body` | `{global.font.size.400}` | Base readable copy step | Semantic body |
| `alias.type.size.lead` | `{global.font.size.450}` | Elevated body step | Semantic lead |
| `alias.type.size.heading.small` | `{global.font.size.600}` | Minor heading step | Semantic heading |
| `alias.type.size.heading.large` | `{global.font.size.700}` | Major heading step | Semantic heading |
| `alias.type.size.display` | `{global.font.size.900}` | Editorial ceiling | Semantic display, responsive transforms |
| `alias.type.weight.body` | `{global.font.weight.body}` | Body floor | Semantic body/caption |
| `alias.type.weight.emphasis` | `{global.font.weight.emphasis}` | Stable emphasis | Semantic body/label |
| `alias.type.weight.control` | `{global.font.weight.control}` | Stable action weight | Semantic control |
| `alias.type.weight.display` | `{global.font.weight.display}` | Short display weight | Semantic heading/display |
| `alias.type.line.reading` | `{global.font.line.body}` | Readable paragraph rhythm | Semantic body/lead |
| `alias.type.line.heading` | `{global.font.line.heading}` | Multi-line heading rhythm | Semantic heading |
| `alias.type.line.compact` | `{global.font.line.display}` | Short display rhythm | Semantic display |

### Space, Shape, Elevation, And Motion

| Token | Alias target | Reason | Allowed consumers |
| --- | --- | --- | --- |
| `alias.space.optical` | `{global.space.1}` | Small perceptual adjustment | Semantic icon/type alignment |
| `alias.space.inline` | `{global.space.2}` | Icon-label and compact inline gap | Semantic layout |
| `alias.space.control` | `{global.space.3}` | Compact control padding | Semantic layout |
| `alias.space.inset` | `{global.space.4}` | Default inset | Semantic layout |
| `alias.space.group` | `{global.space.6}` | Related-content group | Semantic layout |
| `alias.space.panel` | `{global.space.8}` | Panel inset and group separation | Semantic layout |
| `alias.space.section` | `{global.space.12}` | Section separation | Semantic layout |
| `alias.space.scene` | `{global.space.16}` | Expressive scene separation | Semantic editorial layout |
| `alias.space.void` | `{global.space.24}` | Maximum deliberate negative-space step | Semantic hero layout |
| `alias.shape.scene` | `{global.radius.square}` | Unframed plate geometry | Semantic media surfaces |
| `alias.shape.control` | `{global.radius.control}` | Stable input/button shape | Semantic controls |
| `alias.shape.panel` | `{global.radius.panel}` | Stable content containment | Semantic panels |
| `alias.shape.overlay` | `{global.radius.overlay}` | Stable dialog geometry | Semantic overlays |
| `alias.stroke.interactive` | `{global.stroke.standard}` | Durable icon/focus weight | Semantic focus/icon |
| `alias.elevation.rest` | `{global.elevation.base}` | Default nonfloating plane | Semantic surfaces |
| `alias.elevation.raised` | `{global.elevation.raised}` | Functional separation | Semantic menus/panels |
| `alias.elevation.overlay` | `{global.elevation.overlay}` | Blocking layer separation | Semantic dialogs |
| `alias.motion.feedback` | `{global.motion.fast}` | Immediate response duration | Semantic interaction |
| `alias.motion.reveal` | `{global.motion.standard}` | Ordinary disclosure duration | Semantic interaction |
| `alias.motion.deliberate` | `{global.motion.deliberate}` | Larger functional reveal | Semantic interaction |
| `alias.motion.axis` | `{global.motion.axis}` | Directional scene change | Semantic navigation/editorial |
| `alias.motion.editorial` | `{global.motion.editorial}` | Optional atmospheric ceiling | Semantic editorial motion |
| `alias.motion.ease.response` | `{global.motion.ease.response}` | Direct response curve | Semantic interaction |
| `alias.motion.ease.reveal` | `{global.motion.ease.reveal}` | Decelerating reveal curve | Semantic interaction |
| `alias.motion.ease.axis` | `{global.motion.ease.axis}` | Direction-preserving curve | Semantic navigation/editorial |
| `alias.motion.ease.exit` | `{global.motion.ease.exit}` | Faster exit curve | Semantic dismissal |

### Media

| Token | Alias target | Reason | Allowed consumers |
| --- | --- | --- | --- |
| `alias.media.ratio.identity` | `{global.media.ratio.master}` | Stable portrait-first plate | Semantic media and prompt transforms |
| `alias.media.dark.min` | `{global.media.dark.min}` | Lower structural-dark occupancy target | Semantic imagery and validation |
| `alias.media.dark.max` | `{global.media.dark.max}` | Upper ordinary structural-dark target | Semantic imagery and validation |
| `alias.media.peak.max` | `{global.media.peak.max}` | Scarcity ceiling for pale convergence | Semantic imagery and validation |
| `alias.media.texture.none` | `{global.media.texture.clean}` | Functional clean plane | Semantic text/control surfaces |
| `alias.media.texture.matte` | `{global.media.texture.shell}` | Restrained shell texture | Semantic shell |
| `alias.media.texture.identity.low` | `{global.media.texture.identity.low}` | Lower identity grain bound | Semantic imagery transforms |
| `alias.media.texture.identity.high` | `{global.media.texture.identity.high}` | Upper identity grain bound | Semantic imagery transforms |

## Alias Rules

- Use aliases to shield semantic tokens from primitive and global changes.
- Keep alias chains exactly one level deep and inspectable.
- Name aliases by stable design material or relationship, not a component, product, state, file, page, or implementation location.
- A mode may repoint an alias only when the underlying material relationship truly changes. Prefer semantic mode overrides for intent changes.
- Deprecate by mapping the old alias to the new alias for one migration release only, then remove it; do not maintain permanent alias chains.
- Store descriptions and token type with every machine-readable alias so transforms can reject invalid references.

## Anti-Patterns

- Components consuming `alias.*`, `global.*`, or `primitive.*` directly.
- Aliases named `button-orange`, `homepage-dark`, `cowboy-blue`, or any other temporary surface or narrative label.
- More than one intermediate hop between semantic intent and the global scale.
- Repointing aliases locally in application code or redefining the same alias by platform without a transform record.
- Using an alias as a convenient duplicate rather than to protect a stable relationship.
