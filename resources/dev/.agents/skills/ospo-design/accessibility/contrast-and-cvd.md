# Contrast And CVD

Output path: `accessibility/contrast-and-cvd.md`

Reference ratios below are calculated from opaque sRGB token fallbacks with the WCAG relative-luminance formula. They are screening values, not a compliance certificate: re-test the final font, size, weight, opacity, composite, state, platform rendering, image crop, and user mode.

## Contrast System

| Pair | Minimum Contrast | Reference/preferred contrast | Use case | Repair |
| --- | --- | --- | --- | --- |
| `frost.100` on `carbon.950` | `4.5:1` normal text | Reference `14.57:1` | Dark primary text, critical icon | Reduce pale area if halation occurs; do not lower text opacity |
| `mineral.300` on `carbon.950` | `4.5:1` normal text | Reference `9.18:1` | Dark secondary text/link | Add underline/weight for link; use frost for smaller text |
| `sand.300` on `carbon.950` | `4.5:1` normal text | Reference `8.67:1` | Warm support text/highlight | Keep usage short; avoid status-only meaning |
| `sand.500` on `carbon.950` | `4.5:1` normal text | Reference `5.27:1` | Muted dark-mode metadata | Increase to sand.300/frost if font, texture, or display weakens it |
| `carbon.950` on `ember.500` | `4.5:1` normal text | Reference `5.26:1` | Dark-mode primary action label | Revalidate hover/pressed surfaces; use larger/stronger text only as secondary repair |
| `frost.100` on `ember.700` | `4.5:1` normal text | Reference `4.78:1` | Destructive action label | Tight pair: prefer solid fills, no opacity/texture, and test platform rendering |
| `ink.950` on `parchment.50` | `4.5:1` normal text | Reference `13.87:1` | Light primary text | Preserve matte shell and avoid colour wash beneath copy |
| `mineral.700` on `parchment.50` | `4.5:1` normal text | Reference `5.78:1` | Light secondary/link | Underline links; move to ink for compact text |
| `umber.600` on `parchment.50` | `4.5:1` normal text | Reference `5.06:1` | Light muted metadata | Use ink/mineral.700 when font is thin or small |
| `frost.100` on `mineral.700` | `4.5:1` normal text | Reference `5.84:1` | Light-mode selected surface | Add check/selected semantics |
| `ink.950` on `mineral.300` | `4.5:1` normal text | Reference `8.84:1` | Dark-mode selected surface/label | Maintain solid surface |
| `ink.950` on `sand.300` | `4.5:1` normal text | Reference `8.34:1` | Pale warm status surface | Pair with icon/text semantics |
| `mineral.500` against `carbon.950` | `3:1` essential non-text | Reference `3.87:1` | Standard dark boundary/icon | Use mineral.300/frost for focus or thin/small geometry |
| `frost.100` against `carbon.950` | `3:1` focus/non-text | Reference `14.57:1` | Focus ring and critical boundary | Keep solid 2px minimum geometry and offset |
| `carbon.800` against `carbon.950` | No essential-information use | Reference `1.62:1` | Decorative/nonessential plane separation only | Add standard boundary or value step when the edge matters |

## Pairing Rules

- Normal text targets at least `4.5:1`; qualifying large text at least `3:1`; essential non-text information at least `3:1` where the criterion applies.
- Focus targets a crisp, solid `2px` minimum perimeter and clear contrast against adjacent colours. A soft halo does not count as reliable focus.
- Pure black/pure white is not the automatic pair. Use warm/mineral off-white on carbon and inspect halation at low brightness.
- Never composite text through haze, grain, blend modes, or chromatic channel offsets.
- If responsive cropping makes contrast variable, place text on an opaque support surface rather than sampling or strengthening a glow.
- A pair close to its threshold, such as frost on dark ember, receives extra review across font rendering, disabled/loading states, and low-quality displays.

## CVD-Safe Encoding

### Confusion Pairs

- Ember orange, umber, and sand can converge under protan/deutan conditions when their lightness is similar.
- Muted mineral teal can collapse toward charcoal in low light or tritan simulation.
- Warm versus cool field ownership may remain atmospheric, but it cannot communicate unique state, category, direction, or value.
- Thin coloured rims may disappear even when the underlying silhouette remains; essential subject recognition must come from mass and contour.

### Redundant Encoding

| Meaning | Colour cue | Required redundant encoding |
| --- | --- | --- |
| Information | Mineral accent | Information icon and explicit label/message |
| Success/Completion | Sand/mineral or platform success accent | Check, “Complete”/result copy, persistent state |
| Warning | Amber accent | Warning icon, consequence, named action |
| Error | Dark ember/platform error accent | Error icon, problem text, affected scope, Recovery |
| Selected/current | Mineral selected surface | Check/marker, shape/weight change, programmatic Selected/current state |
| Focus | Pale ring | Solid geometry, offset, keyboard focus semantics |
| Gain/loss or positive/negative data | Domain/platform colours where appropriate | Sign, arrow direction, direct label, value, line/marker pattern |
| Route/direction | Warm/cool or luminous line | Arrow, ordered labels, position, text direction |

- Do not reuse one shape for every status and merely recolour it.
- Direct labels outrank legends when space permits.
- Chart series use line style, marker, direct label, and/or pattern in addition to hue.
- Disabled state remains readable and programmatically unavailable; opacity is not the only cue.

## Dark-Mode CVD Adjustments

- Preserve a substantial lightness step between carbon, mineral midtone, and pale foreground.
- Promote essential cool boundaries from mineral.500 to mineral.300/frost rather than increasing saturation alone.
- Keep hot and cool territories spatially separate enough that their boundary survives hue loss.
- Ensure the subject core and negative cuts remain readable in greyscale before adding coloured rims.
- Avoid small umber-on-carbon text and thin teal-on-charcoal controls.
- Test at low display brightness, with glare, and after image compression.

## High-Contrast Theme Behavior

- Replace brand surfaces with system `Canvas`, `CanvasText`, `Highlight`, `HighlightText`, `LinkText`, and platform equivalents.
- Remove grain, bloom, translucent container dependence, and duotone functional icons.
- Use solid boundaries, native focus, visible current/selected markers, text labels, and pattern/shape redundancy.
- Identity imagery may remain available as nonessential media, but all information and actions must survive with the image hidden or simplified.
- Do not force brand hex values through forced-colour modes.

## Image And Media Checks

1. Convert to greyscale; verify one event, subject category, relationship/count, and governing axis.
2. Simulate protan, deutan, and tritan perception at normal and reduced size.
3. Downsample to thumbnail; confirm recognition without thin coloured rims.
4. Test bright environment and low-brightness viewing; deepen structural boundaries rather than saturating everything.
5. Inspect the final compressed export at 100%; colour subsampling must not erase necessary contour separation.
6. Verify alt text and nonvisual state/context; atmosphere is never the only carrier.

## Validation And Repair Order

1. Fix semantics and Redundant encoding.
2. Add or strengthen clean support surfaces.
3. Adjust lightness before chroma or hue.
4. Adjust weight, size, boundary thickness, or spacing.
5. Re-run all modes, CVD simulations, actual-component tests, and device review.

## Anti-Patterns

- Declaring a token pair accessible from its hex values without testing the rendered component.
- Increasing saturation to fix Contrast, or using a glow to imitate a focus boundary.
- Warm/cool colour as the only status, selected, route, gain/loss, or chart-series encoding.
- Applying CVD simulation only to the palette while ignoring image contours, compression, opacity, and chart marks.
- Keeping brand colours in high-contrast mode when system colours communicate more reliably.
