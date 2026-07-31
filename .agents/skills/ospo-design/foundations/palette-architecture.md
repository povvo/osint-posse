# Palette Architecture

Output path: `foundations/palette-architecture.md`

## Palette Identity

- **Colour story:** a light-absorbing carbon field is split by an ember family and a mineral-air family. Dusty sand and umber mediate the collision; a pale frost tone appears only where the two luminous territories converge.
- **Hue family and temperature:** warm hues center on red-orange and burnt amber; cool hues center on desaturated cyan, blue-green, and slate. Keep the warm and cool centroids close to perceptual opposites rather than drifting toward magenta/green or yellow/blue.
- **Saturation and chroma behavior:** saturation is selective. Ember may be vivid, cool light stays mineral and partially greyed, and the majority of the field remains nearly achromatic. A useful starting balance is 50–65% void/charcoal, 18–30% warm light and spill, 7–16% cool light and haze, 3–10% sand/umber mediation, and no more than 5% pale convergence.
- **Lightness range:** use an extreme range with a compressed dark majority. Structural black sits near the luminance floor; coloured midtones step rapidly into isolated bright pools. Avoid lifting the entire shadow range.
- **Emotional role of colour:** black creates watchfulness, ember creates danger and ceremony, mineral cyan creates distance and apparition, sand creates memory and dust, and pale convergence creates temporary revelation.

## Palette Separation

| Territory | Owned colours | Boundary rule | Emotional or functional role |
| --- | --- | --- | --- |
| Absorptive void | `#0D0E0E`, `#141817`, `#32383A` | Must remain continuous enough to hold silhouettes; never surround every object with a halo | Structure, concealment, rest, primary shell |
| Ember field | `#E85A2F`, `#E5894E`, `#8A493A` | Expands as ground, flare, or edge stain; do not assign it uniformly to all foreground content | Attention, heat, urgency, ceremony |
| Mineral field | `#A1B7B7`, `#5E7470`, `#46656A` | Appears as rim, atmosphere, counterplane, or calm support; keep chroma lower than ember | Distance, orientation, cool air, informational calm |
| Dust mediation | `#C6A985`, `#9B8165`, `#6D4A3D` | Bridges value, not hue; use where warm and cool particulate fields mix | Grounding, age, transition, secondary content |
| Convergence light | `#D8E2DC`, `#E5D5C1` | Confine to a narrow highlight, focal pool, or accessibility-critical foreground | Revelation, peak hierarchy, readable text or icon |

## Convergence Behaviour

- **Merge, collide, invert, absorb, or remain separate:** ember and mineral territories collide through particulate interleaving and soft edge spill. They do not blend into a smooth neutral gradient. The void may absorb either territory before the opposite pole appears.
- **Trigger for convergence or divergence:** convergence occurs only at the focal event, a route, a rim, or an active state. Divergence dominates passive space.
- **Interface equivalent:** one expressive accent may bloom against the shell while cool text, focus, or informational structure remains crisp. Active and selected states may show a thin dual-temperature edge plus a non-colour shape change.
- **Forbidden convergence:** equal orange/cyan halves, broad beige-grey blending, full-spectrum neon, large neutral-white washes, or a uniform teal-and-orange grade over every surface.

## Container Principle

- **Shell or surface relationship to colour:** the shell is absorptive, not neutral in the ordinary UI sense. It should appear to remove light and allow one luminous event to own the field.
- **Container quality:** use near-black carbon for identity-bearing dark mode. Secondary surfaces are slightly lifted charcoal or mineral-black, separated by value and texture rather than bright borders.
- **Surface-colour interaction:** expressive colour may stain an edge or local region but should not tint every container. Support text and controls sit on calm dark islands outside the noisiest bloom. In light mode, use matte parchment with dark carbon structure and smaller, darker accents.

## Light Quality

- **Direction:** directional enough to describe a governing axis, but often distributed through ground, haze, or an apparently luminous surface.
- **Hardness:** structurally hard at the silhouette core and optically soft at the illuminated perimeter.
- **Temperature:** bi-thermal. One warm source or plane and one cool counterfield are the default; neither should look like neutral studio light.
- **Intensity:** high local contrast with restrained total bright area. Pale convergence is a peak, not a background.
- **Static, fading, pulsing, or shifting behavior:** still imagery uses frozen bloom. Motion may drift or decay slowly; rapid hue cycling and rhythmic neon pulsing are prohibited.

## Mode Adaptation

| Mode | Palette translation | Risk control |
| --- | --- | --- |
| Light | Matte parchment `#E7DDD0` or cool dust `#D8E2DC` becomes the shell; carbon `#121313` supplies structure; use darker ember `#A83B22` and mineral `#35585E` as compact accents | Do not recreate the hero atmosphere by flooding a light surface with pale orange/cyan. Recheck all text and interactive contrast; suppress grain behind small type |
| Dark | Carbon `#0D0E0E` shell, charcoal `#32383A` support, ember/mineral expressive fields, pale convergence for selected text and focal marks | Keep bright area low to reduce halation; do not use charcoal as body text or apply saturated accents to long passages |
| High contrast | Reduce to carbon, pale frost, and one context-appropriate accent; replace soft rims with solid outlines or patterns | Every status receives text/icon/shape redundancy. Remove grain and bloom from text, focus, and essential boundaries |

## CVD And Ambient Robustness

- **Hue-only distinctions to replace:** warm/cool is an atmospheric relationship, never the sole carrier of status, selection, error, success, direction, or ownership.
- **Lightness and pattern alternatives:** pair state colour with a label, icon, silhouette change, border pattern, position, or motion-independent marker. Preserve at least a 3:1 boundary contrast for essential non-text graphics and WCAG 2.x text contrast at the intended size.
- **Bright-environment survival rule:** deepen structural darks, reduce diffuse bloom, thicken essential contours, and provide an optional clean support plate behind text or controls.
- **Low-light survival rule:** cap large bright pools, prefer warm off-white or pale mineral text to pure white, and keep adjacent dark steps far enough apart to remain distinguishable after display dimming.

## Token Translation

| Token role | Candidate values or ranges | Usage rule |
| --- | --- | --- |
| `color.field.void` | `#0D0E0E` | Identity shell and deepest silhouette core; not the default text/background pair with pure white |
| `color.field.charcoal` | `#32383A` | Lifted support surface and atmospheric dark; not body text |
| `color.light.ember` | `#E85A2F` | Primary expressive flare, active mark, or local edge stain; verify text use separately |
| `color.light.amber` | `#E5894E` | Secondary warm light and accessible compact accent on the void |
| `color.light.mineral` | `#A1B7B7` | Cool luminous plane, high-value support text, or atmospheric rim |
| `color.light.teal-muted` | `#5E7470` | Cool midtone and haze; not small text on the void without contrast validation |
| `color.mediator.sand` | `#C6A985` | Dust, secondary highlight, or warm support text |
| `color.mediator.umber` | `#8A493A` | Warm shadow and transition; never the only difference between states |
| `color.light.convergence` | `#D8E2DC`–`#E5D5C1` | Tiny peak highlight, primary dark-mode text, or critical icon |
| `ratio.field.dark` | `0.50`–`0.65` | Maintain the dark majority in identity-bearing scenes |
| `ratio.field.hot-to-cool` | approximately `3:1`–`7:1` by saturated area | Preserve unequal temperature ownership; invert only intentionally |
| `ratio.field.peak` | `0.00`–`0.05` | Cap pale convergence to retain scarcity and hierarchy |

## Contrast Obligations

- Treat WCAG 2.x as the compliance floor and use perceptual review or APCA as a secondary dark-mode quality signal.
- Test final rendered colours on the target platform; the same hex values can shift with display, colour management, opacity, blur, and texture.
- Keep the identity image and the information layer separable. If an image region cannot provide stable contrast across crops, add a solid support plate rather than a stronger glow.
- Never infer accessibility from palette membership. Validate every text pair, focus indicator, essential icon, and interactive boundary in its actual state.

## Anti-Patterns

- Mid-grey “dark mode” that removes the black-field hierarchy.
- Equal-area orange and cyan, smooth complementary gradients, or colour applied as a universal grading preset.
- Pure white bloom across large regions, clipped channels, or fluorescent saturation on every accent.
- Status semantics that depend on ember versus mineral colour alone.
- Grain, chromatic aberration, or blur on body text, focus rings, small icons, data, or legal content.
- Assigning fixed object meanings such as “all ground is orange” or “all figures are cyan”; colour roles are relational and compositional.
