# Primitive Tokens

Output path: `tokens/primitive-tokens.md`

Primitive tokens hold raw material only. Semantic and component layers must reference aliases or semantic roles rather than reaching into this table directly. Colour values include a hex fallback and perceptual OKLCH definition; the implementation pipeline should select one canonical storage model and generate the other.

## Primitive Value Inventory

### Colour

| Token | Type | Raw value | Unit/model | Range role | Notes |
| --- | --- | --- | --- | --- | --- |
| `primitive.color.carbon.950` | colour | `#0D0E0E`; `oklch(16.3% 0.002 197)` | sRGB / OKLCH | Deepest dark | Identity field and structural silhouette |
| `primitive.color.carbon.900` | colour | `#141817`; `oklch(20.4% 0.006 179)` | sRGB / OKLCH | Dark | Alternate field and pressed surface |
| `primitive.color.carbon.800` | colour | `#32383A`; `oklch(33.6% 0.009 220)` | sRGB / OKLCH | Lifted dark | Support surface; not body text |
| `primitive.color.ember.500` | colour | `#E85A2F`; `oklch(64.7% 0.185 37)` | sRGB / OKLCH | Vivid warm | Primary expressive warm |
| `primitive.color.ember.400` | colour | `#E5894E`; `oklch(71.7% 0.135 52)` | sRGB / OKLCH | Lighter warm | Amber highlight and compact accent |
| `primitive.color.ember.700` | colour | `#A83B22`; `oklch(50.4% 0.149 34)` | sRGB / OKLCH | Dark warm | Light-mode warm accent |
| `primitive.color.umber.600` | colour | `#8A493A`; `oklch(48.1% 0.092 34)` | sRGB / OKLCH | Warm shadow | Transition and edge contamination |
| `primitive.color.umber.700` | colour | `#6D4A3D`; `oklch(44.4% 0.052 41)` | sRGB / OKLCH | Muted warm dark | Dust-shadow mediation |
| `primitive.color.mineral.300` | colour | `#A1B7B7`; `oklch(76.3% 0.024 197)` | sRGB / OKLCH | Pale cool | Cool luminous plane and support text |
| `primitive.color.mineral.500` | colour | `#5E7470`; `oklch(54.0% 0.027 183)` | sRGB / OKLCH | Muted cool | Haze and cool midtone |
| `primitive.color.mineral.600` | colour | `#46656A`; `oklch(48.5% 0.037 209)` | sRGB / OKLCH | Dark cool | Light-mode structural cool |
| `primitive.color.mineral.700` | colour | `#35585E`; `oklch(43.6% 0.042 210)` | sRGB / OKLCH | Deeper cool | Light-mode accent and boundary |
| `primitive.color.sand.300` | colour | `#C6A985`; `oklch(75.1% 0.060 73)` | sRGB / OKLCH | Pale warm neutral | Dust, secondary highlight, support text |
| `primitive.color.sand.500` | colour | `#9B8165`; `oklch(62.0% 0.051 69)` | sRGB / OKLCH | Mid warm neutral | Mediation and subdued surfaces |
| `primitive.color.frost.100` | colour | `#D8E2DC`; `oklch(90.3% 0.013 160)` | sRGB / OKLCH | Pale cool-neutral | Dark-mode primary text and convergence |
| `primitive.color.parchment.100` | colour | `#E5D5C1`; `oklch(88.1% 0.032 74)` | sRGB / OKLCH | Pale warm-neutral | Warm convergence and light support |
| `primitive.color.parchment.50` | colour | `#E7DDD0`; `oklch(90.2% 0.021 75)` | sRGB / OKLCH | Light shell | Matte light-mode field |
| `primitive.color.ink.950` | colour | `#121313`; `oklch(18.6% 0.002 197)` | sRGB / OKLCH | Light-mode text | Carbon ink on light surfaces |
| `primitive.alpha.0` | number | `0` | scalar | Transparent | No contribution |
| `primitive.alpha.8` | number | `0.08` | scalar | Trace | Subtle atmosphere or tonal lift |
| `primitive.alpha.16` | number | `0.16` | scalar | Low | Particulate colour or quiet border |
| `primitive.alpha.24` | number | `0.24` | scalar | Low-mid | Atmospheric layer |
| `primitive.alpha.36` | number | `0.36` | scalar | Mid | Maximum ordinary haze layer |
| `primitive.alpha.72` | number | `0.72` | scalar | High | Strong media overlay only |
| `primitive.alpha.92` | number | `0.92` | scalar | Near-opaque | Text support plate minimum |
| `primitive.alpha.100` | number | `1` | scalar | Opaque | Functional and critical surfaces |

### Typography

| Token | Type | Raw value | Unit/model | Range role | Notes |
| --- | --- | --- | --- | --- | --- |
| `primitive.font.family.sans` | fontFamily | `ui-sans-serif, system-ui, sans-serif` | stack | Primary | Replace with an approved open-aperture humanist family |
| `primitive.font.family.serif` | fontFamily | `ui-serif, Georgia, serif` | stack | Secondary | Optional editorial display |
| `primitive.font.family.mono` | fontFamily | `ui-monospace, SFMono-Regular, monospace` | stack | Data | Technical content only |
| `primitive.font.size.200` | dimension | `0.8125rem` | rem | 13px-equivalent | Caption/data floor |
| `primitive.font.size.300` | dimension | `0.875rem` | rem | 14px-equivalent | Labels |
| `primitive.font.size.400` | dimension | `1rem` | rem | Body base | Functional text floor |
| `primitive.font.size.450` | dimension | `1.125rem` | rem | Body lead | 18px-equivalent |
| `primitive.font.size.500` | dimension | `1.25rem` | rem | Lead/small heading | 20px-equivalent |
| `primitive.font.size.600` | dimension | `1.5rem` | rem | Heading | 24px-equivalent |
| `primitive.font.size.700` | dimension | `2rem` | rem | Heading | 32px-equivalent |
| `primitive.font.size.800` | dimension | `3rem` | rem | Large heading | 48px-equivalent |
| `primitive.font.size.900` | dimension | `4.5rem` | rem | Display ceiling | 72px-equivalent |
| `primitive.font.weight.regular` | fontWeight | `400` | numeric | Body | Do not go lighter for body |
| `primitive.font.weight.medium` | fontWeight | `500` | numeric | Emphasis | Labels and body emphasis |
| `primitive.font.weight.semibold` | fontWeight | `600` | numeric | Control/heading | Crisp hierarchy |
| `primitive.font.weight.bold` | fontWeight | `700` | numeric | Display | Short headings only |
| `primitive.font.line.compact` | number | `1.05` | scalar | Display | Optical display rhythm |
| `primitive.font.line.heading` | number | `1.18` | scalar | Heading | Short multi-line headings |
| `primitive.font.line.body` | number | `1.6` | scalar | Body | Default reading rhythm |
| `primitive.font.line.caption` | number | `1.45` | scalar | Caption | Compact factual copy |
| `primitive.font.tracking.tight` | dimension | `-0.02em` | em | Display | Optical only |
| `primitive.font.tracking.normal` | dimension | `0` | em | Body | Default |
| `primitive.font.tracking.label` | dimension | `0.02em` | em | Label | Maximum routine tracking |

### Space, Shape, And Stroke

| Token | Type | Raw value | Unit/model | Range role | Notes |
| --- | --- | --- | --- | --- | --- |
| `primitive.grid.base` | dimension | `4px` | px | Base | All digital spacing derives here |
| `primitive.space.0` | dimension | `0` | px | Zero | Reset |
| `primitive.space.1` | dimension | `4px` | px | XS | Optical nudge, not touch padding |
| `primitive.space.2` | dimension | `8px` | px | S | Label/icon gap |
| `primitive.space.3` | dimension | `12px` | px | S+ | Compact control padding |
| `primitive.space.4` | dimension | `16px` | px | M | Default compact inset |
| `primitive.space.6` | dimension | `24px` | px | L | Content grouping |
| `primitive.space.8` | dimension | `32px` | px | XL | Panel inset |
| `primitive.space.12` | dimension | `48px` | px | 2XL | Section gap |
| `primitive.space.16` | dimension | `64px` | px | 3XL | Scene/content separation |
| `primitive.space.24` | dimension | `96px` | px | 4XL | Hero-scale void |
| `primitive.radius.0` | dimension | `0` | px | Square | Scene plates and strict surfaces |
| `primitive.radius.1` | dimension | `2px` | px | Subtle | Small functional elements |
| `primitive.radius.2` | dimension | `4px` | px | Default | Inputs and compact controls |
| `primitive.radius.3` | dimension | `8px` | px | Soft | Panels and larger controls |
| `primitive.radius.4` | dimension | `12px` | px | Maximum routine | Large cards/dialogs |
| `primitive.radius.full` | dimension | `999px` | px | Pill/circle | Tags, avatars, round controls only |
| `primitive.stroke.hairline` | dimension | `1px` | px | Fine | Dividers and ordinary boundaries |
| `primitive.stroke.strong` | dimension | `2px` | px | Strong | Icons and focus ring |
| `primitive.stroke.critical` | dimension | `3px` | px | Maximum | High-contrast/critical emphasis |
| `primitive.target.touch` | dimension | `44px` | px | Minimum target | Increase if platform guidance is stricter |

### Elevation, Blur, And Overlay

| Token | Type | Raw value | Unit/model | Range role | Notes |
| --- | --- | --- | --- | --- | --- |
| `primitive.shadow.none` | shadow | `none` | CSS-like | Base | Preferred default |
| `primitive.shadow.low` | shadow | `0 4px 16px rgb(0 0 0 / 0.35)` | CSS-like | Raised | Functional surfaces only |
| `primitive.shadow.high` | shadow | `0 12px 48px rgb(0 0 0 / 0.50)` | CSS-like | Overlay | Dialog/critical overlay |
| `primitive.blur.edge.1` | dimension | `4px` | px at 736px reference | Fine | Local illuminated edge |
| `primitive.blur.edge.2` | dimension | `12px` | px at 736px reference | Broad | Maximum ordinary edge diffusion |
| `primitive.blur.atmosphere.1` | dimension | `24px` | px at 736px reference | Haze | Scale with short edge |
| `primitive.blur.atmosphere.2` | dimension | `40px` | px at 736px reference | Bloom | Focal atmosphere only |
| `primitive.overlay.support` | number | `0.92` | alpha | Text plate | Increase to opaque when contrast varies |
| `primitive.overlay.scrim` | number | `0.72` | alpha | Modal scrim | Must preserve overlay contrast |

### Motion

| Token | Type | Raw value | Unit/model | Range role | Notes |
| --- | --- | --- | --- | --- | --- |
| `primitive.duration.1` | duration | `80ms` | ms | Immediate | Press acknowledgement |
| `primitive.duration.2` | duration | `120ms` | ms | Fast | Exit or compact feedback |
| `primitive.duration.3` | duration | `180ms` | ms | Functional | Small reveal |
| `primitive.duration.4` | duration | `240ms` | ms | Standard | Panel/state change |
| `primitive.duration.5` | duration | `300ms` | ms | Deliberate | Larger functional reveal |
| `primitive.duration.6` | duration | `420ms` | ms | Scenic | Axis transition ceiling for routine UI |
| `primitive.duration.7` | duration | `800ms` | ms | Editorial | Optional nonessential emergence only |
| `primitive.delay.1` | duration | `40ms` | ms | Stagger | Compact sequence |
| `primitive.delay.2` | duration | `80ms` | ms | Stagger ceiling | Maximum ordinary group offset |
| `primitive.ease.immediate` | cubicBezier | `cubic-bezier(0.2, 0, 0, 1)` | curve | Response | Direct confirmation |
| `primitive.ease.reveal` | cubicBezier | `cubic-bezier(0.16, 1, 0.3, 1)` | curve | Reveal | Decelerating disclosure |
| `primitive.ease.axis` | cubicBezier | `cubic-bezier(0.2, 0.75, 0.2, 1)` | curve | Travel | Governing-axis move |
| `primitive.ease.exit` | cubicBezier | `cubic-bezier(0.4, 0, 1, 1)` | curve | Exit | Faster withdrawal |

### Media

| Token | Type | Raw value | Unit/model | Range role | Notes |
| --- | --- | --- | --- | --- | --- |
| `primitive.ratio.portrait` | number | `3 / 4` | aspect ratio | Master plate | Identity-first composition |
| `primitive.ratio.square` | number | `1 / 1` | aspect ratio | Derived crop | Preserve recognition core |
| `primitive.ratio.editorial` | number | `4 / 5` | aspect ratio | Derived crop | Social/editorial |
| `primitive.ratio.landscape` | number | `16 / 9` | aspect ratio | Derived crop | Extend void or route |
| `primitive.ratio.story` | number | `9 / 16` | aspect ratio | Derived crop | Reduce peripheral modules |
| `primitive.media.dark.min` | number | `0.50` | frame ratio | Lower bound | Dark plus charcoal area |
| `primitive.media.dark.max` | number | `0.65` | frame ratio | Upper target | May exceed for sparse variants |
| `primitive.media.peak.max` | number | `0.05` | frame ratio | Ceiling | Pale convergence scarcity |
| `primitive.texture.clean` | number | `0` | luminance fraction | Functional | Text, icons, controls |
| `primitive.texture.shell` | number | `0.015` | luminance fraction | Restrained | Calm matte shell ceiling |
| `primitive.texture.image.min` | number | `0.03` | luminance fraction | Identity | Fine texture starting point |
| `primitive.texture.image.max` | number | `0.06` | luminance fraction | Identity | Fine texture ceiling before review |
| `primitive.focal.center` | vector | `50% 52%` | x/y | Iconic | Optical center baseline |
| `primitive.focal.lower` | vector | `50% 64%` | x/y | Gathering | Leaves upper void |
| `primitive.focal.route-start` | vector | `25% 78%` | x/y | Procession | Foreground entry |
| `primitive.focal.route-end` | vector | `78% 36%` | x/y | Procession | Distant destination |

## Anti-Patterns

- Components referencing primitive values directly.
- Reusing colour-number names as semantic meaning, such as `ember.500` for every error.
- Hard-coded hex, blur, spacing, duration, or grain values outside the token pipeline.
- Treating reference-scale pixel blur as fixed across all image sizes.
- Generating platform files from different primitive inventories or rounding units inconsistently.
- Expanding the scale with one-off values instead of first testing the nearest existing step.
