# Global Tokens

Output path: `tokens/global-tokens.md`

Global tokens expose a calibrated, implementation-wide scale. Each global token has one primitive reference and no product meaning. Semantic tokens may reference globals; components may not. The `Reference` form below uses brace syntax compatible with W3C Design Tokens-style aliasing.

## Global Scale Contract

### Colour Ramps

| Token | Scope | Scale | Reference | Applies to | Relationship |
| --- | --- | --- | --- | --- | --- |
| `global.color.carbon.950` | All modes | Carbon 950 | `{primitive.color.carbon.950}` | Field, silhouette, ink | Deepest identity dark |
| `global.color.carbon.900` | All modes | Carbon 900 | `{primitive.color.carbon.900}` | Alternate dark | One lift above deepest |
| `global.color.carbon.800` | All modes | Carbon 800 | `{primitive.color.carbon.800}` | Raised dark | Highest routine dark |
| `global.color.ember.700` | All modes | Ember 700 | `{primitive.color.ember.700}` | Dark warm accent | Light-mode capable warm |
| `global.color.ember.500` | All modes | Ember 500 | `{primitive.color.ember.500}` | Vivid warm | Identity warm peak |
| `global.color.ember.400` | All modes | Ember 400 | `{primitive.color.ember.400}` | Warm highlight | Lighter, less chromatic step |
| `global.color.umber.700` | All modes | Umber 700 | `{primitive.color.umber.700}` | Warm dark mediation | Dust shadow |
| `global.color.umber.600` | All modes | Umber 600 | `{primitive.color.umber.600}` | Warm mid mediation | Edge contamination |
| `global.color.mineral.700` | All modes | Mineral 700 | `{primitive.color.mineral.700}` | Deep cool | Light-mode boundary |
| `global.color.mineral.600` | All modes | Mineral 600 | `{primitive.color.mineral.600}` | Cool structural | Cool accent |
| `global.color.mineral.500` | All modes | Mineral 500 | `{primitive.color.mineral.500}` | Cool midtone | Haze |
| `global.color.mineral.300` | All modes | Mineral 300 | `{primitive.color.mineral.300}` | Pale cool | Luminous support |
| `global.color.sand.500` | All modes | Sand 500 | `{primitive.color.sand.500}` | Neutral midtone | Warm mediation |
| `global.color.sand.300` | All modes | Sand 300 | `{primitive.color.sand.300}` | Pale warm | Dust highlight |
| `global.color.frost.100` | All modes | Frost 100 | `{primitive.color.frost.100}` | Pale cool-neutral | Primary dark-mode foreground |
| `global.color.parchment.100` | All modes | Parchment 100 | `{primitive.color.parchment.100}` | Pale warm-neutral | Warm convergence |
| `global.color.parchment.50` | All modes | Parchment 50 | `{primitive.color.parchment.50}` | Light shell | Primary light-mode field |
| `global.color.ink.950` | All modes | Ink 950 | `{primitive.color.ink.950}` | Light-mode foreground | Primary light-mode ink |

### Type Scale

| Token | Scope | Scale | Reference | Applies to | Relationship |
| --- | --- | --- | --- | --- | --- |
| `global.font.family.primary` | All text | Family primary | `{primitive.font.family.sans}` | UI/body | Default family |
| `global.font.family.editorial` | Optional display | Family secondary | `{primitive.font.family.serif}` | Editorial titles | Never required for function |
| `global.font.family.data` | Structured data | Family mono | `{primitive.font.family.mono}` | Code/coordinates/tables | Use only for real data |
| `global.font.size.200` | All platforms | 200 | `{primitive.font.size.200}` | Captions/data | Smallest routine scale step |
| `global.font.size.300` | All platforms | 300 | `{primitive.font.size.300}` | Labels | Compact step |
| `global.font.size.400` | All platforms | 400 | `{primitive.font.size.400}` | Body | Body base |
| `global.font.size.450` | All platforms | 450 | `{primitive.font.size.450}` | Lead/body large | Accessibility-friendly lift |
| `global.font.size.500` | All platforms | 500 | `{primitive.font.size.500}` | Lead/small heading | Bridge step |
| `global.font.size.600` | All platforms | 600 | `{primitive.font.size.600}` | Heading | Section step |
| `global.font.size.700` | All platforms | 700 | `{primitive.font.size.700}` | Heading | Major step |
| `global.font.size.800` | Wide/editorial | 800 | `{primitive.font.size.800}` | Large heading | Responsive maximum on narrow screens |
| `global.font.size.900` | Wide/editorial | 900 | `{primitive.font.size.900}` | Display | Rare hero ceiling |
| `global.font.weight.body` | All text | Regular | `{primitive.font.weight.regular}` | Body | Minimum normal body weight |
| `global.font.weight.emphasis` | All text | Medium | `{primitive.font.weight.medium}` | Emphasis | Stable on dark surfaces |
| `global.font.weight.control` | Functional | Semibold | `{primitive.font.weight.semibold}` | Labels/buttons | Action hierarchy |
| `global.font.weight.display` | Editorial | Bold | `{primitive.font.weight.bold}` | Short display | Never long-form |
| `global.font.line.display` | Editorial | Compact | `{primitive.font.line.compact}` | Display | Short lines only |
| `global.font.line.heading` | All modes | Heading | `{primitive.font.line.heading}` | Headings | Multi-line capable |
| `global.font.line.body` | All modes | Body | `{primitive.font.line.body}` | Paragraphs | Reading default |
| `global.font.line.caption` | All modes | Caption | `{primitive.font.line.caption}` | Metadata | Compact but readable |

### Space And Shape

| Token | Scope | Scale | Reference | Applies to | Relationship |
| --- | --- | --- | --- | --- | --- |
| `global.space.0` | All layout | 0 | `{primitive.space.0}` | Reset | No gap |
| `global.space.1` | All layout | 1 | `{primitive.space.1}` | Optical | One base unit |
| `global.space.2` | All layout | 2 | `{primitive.space.2}` | Compact | Two units |
| `global.space.3` | All layout | 3 | `{primitive.space.3}` | Compact-plus | Three units |
| `global.space.4` | All layout | 4 | `{primitive.space.4}` | Default inset | Four units |
| `global.space.6` | All layout | 6 | `{primitive.space.6}` | Group | Six units |
| `global.space.8` | All layout | 8 | `{primitive.space.8}` | Panel | Eight units |
| `global.space.12` | All layout | 12 | `{primitive.space.12}` | Section | Twelve units |
| `global.space.16` | Expressive layout | 16 | `{primitive.space.16}` | Large section | Sixteen units |
| `global.space.24` | Expressive layout | 24 | `{primitive.space.24}` | Hero void | Twenty-four units |
| `global.radius.square` | All components | 0 | `{primitive.radius.0}` | Scene plates | Hard edge |
| `global.radius.subtle` | All components | 1 | `{primitive.radius.1}` | Small control | Minimal softening |
| `global.radius.control` | All components | 2 | `{primitive.radius.2}` | Input/button | Default |
| `global.radius.panel` | All components | 3 | `{primitive.radius.3}` | Panel | Calm containment |
| `global.radius.overlay` | All components | 4 | `{primitive.radius.4}` | Dialog | Maximum routine rounding |
| `global.radius.round` | Specific components | Full | `{primitive.radius.full}` | Badge/avatar | Not a general default |
| `global.stroke.standard` | All components | Strong | `{primitive.stroke.strong}` | Icon/focus | 2px base |
| `global.target.touch` | Touch inputs | Minimum | `{primitive.target.touch}` | Hit area | Platform may override upward |

### Elevation, Motion, And Media

| Token | Scope | Scale | Reference | Applies to | Relationship |
| --- | --- | --- | --- | --- | --- |
| `global.elevation.base` | All surfaces | 0 | `{primitive.shadow.none}` | Base | No shadow |
| `global.elevation.raised` | Functional | 1 | `{primitive.shadow.low}` | Menu/panel | Restrained separation |
| `global.elevation.overlay` | Functional | 2 | `{primitive.shadow.high}` | Dialog | Strongest elevation |
| `global.motion.fast` | Functional | 1 | `{primitive.duration.2}` | Exit/feedback | 120ms |
| `global.motion.standard` | Functional | 2 | `{primitive.duration.4}` | Reveal/state | 240ms |
| `global.motion.deliberate` | Functional | 3 | `{primitive.duration.5}` | Larger reveal | 300ms |
| `global.motion.axis` | Functional/editorial | 4 | `{primitive.duration.6}` | Spatial move | 420ms |
| `global.motion.editorial` | Optional editorial | 5 | `{primitive.duration.7}` | Atmosphere | 800ms ceiling |
| `global.motion.ease.response` | Functional | Response | `{primitive.ease.immediate}` | Press/feedback | Direct |
| `global.motion.ease.reveal` | Functional | Reveal | `{primitive.ease.reveal}` | Disclosure | Decelerating |
| `global.motion.ease.axis` | Functional/editorial | Axis | `{primitive.ease.axis}` | Scene move | Directional |
| `global.motion.ease.exit` | Functional | Exit | `{primitive.ease.exit}` | Dismissal | Faster |
| `global.media.ratio.master` | Identity imagery | Portrait | `{primitive.ratio.portrait}` | Source composition | 3:4 |
| `global.media.dark.min` | Identity imagery | Lower bound | `{primitive.media.dark.min}` | Dark structural area | 50% frame target |
| `global.media.dark.max` | Identity imagery | Upper target | `{primitive.media.dark.max}` | Dark structural area | 65% frame target |
| `global.media.peak.max` | Identity imagery | Ceiling | `{primitive.media.peak.max}` | Pale convergence | 5% frame maximum |
| `global.media.texture.clean` | Functional | 0 | `{primitive.texture.clean}` | Text/control layer | No texture |
| `global.media.texture.shell` | Shell | 1 | `{primitive.texture.shell}` | Matte field | Very restrained |
| `global.media.texture.identity.low` | Identity imagery | 2 | `{primitive.texture.image.min}` | Fine grain | 3% start |
| `global.media.texture.identity.high` | Identity imagery | 3 | `{primitive.texture.image.max}` | Fine grain | 6% ceiling |

## Density And Breakpoint Scales

| Token | Type | Value | Scope | Reference behavior |
| --- | --- | --- | --- | --- |
| `global.breakpoint.compact` | dimension | `0–599px` | Narrow web | Preserve recognition core; reduce peripheral modules |
| `global.breakpoint.medium` | dimension | `600–1023px` | Tablet/small desktop | Standard 8px rhythm and two-plane layout |
| `global.breakpoint.wide` | dimension | `1024–1439px` | Desktop | Expand void and directional field |
| `global.breakpoint.cinematic` | dimension | `1440px+` | Large display | Cap text measure; do not scale all controls with viewport |
| `global.density.compact` | number | `0.875` | Data-heavy/task views | Never reduce touch target or text floor |
| `global.density.comfortable` | number | `1` | Default product | Standard spacing scale |
| `global.density.editorial` | number | `1.25` | Hero/editorial | Larger section and void spacing |

## Scale-Family Rules

- Colour ramps express material families, not status. Mode and semantic layers assign intent.
- The type scale is hand-tuned; responsive roles interpolate between steps but must preserve weight and line-height obligations.
- Spacing uses a 4px primitive and 8px ordinary cadence. Large proportional voids supplement rather than replace the grid.
- Radius remains restrained. A component cannot become “on brand” merely by making it square or round.
- Elevation is functional and sparse; atmosphere is not elevation.
- Breakpoints describe layout pressure, not device identity. Native platforms map them to their own size classes.

## Anti-Patterns

- Naming a global token by a temporary component or status.
- Creating a second global scale for one platform rather than transforming units and typography systematically.
- Using breakpoint tokens inside imagery prompts or hard-coding device models.
- Skipping the semantic layer and binding components directly to `global.color.*` or `primitive.*`.
- Adding half-steps without documenting why the existing scale cannot serve the need.
