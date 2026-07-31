# Prompt Pack

Output path: `outputs/prompt-pack.md`

This pack supplies one executable, nonderivative demonstration route plus controlled variants. It proves the language can survive a completely different subject without relying on frontier props or a copied scene.

## Prompt-Pack Intake

- **Intent:** generate a new identity illustration that demonstrates the full visual grammar.
- **Asset type:** single stylized editorial illustration.
- **Target surface:** cover, poster, or landing-page hero.
- **Final use:** internal visual proof and prompt baseline; production use requires channel-specific review.
- **Audience or viewing context:** general adult editorial audience, first read at thumbnail and ordinary screen size.
- **Dimensions, ratio, or safe area:** `1536×2048`, 3:4 portrait; keep the recognition core inside the central 72% width and 76% height.
- **Format and transparency needs:** high-quality PNG master plus reviewed JPEG derivative; opaque background.
- **Exact rendered text:** none.
- **Subject:** exactly one large radio telescope dish on a sparse mineral plain; no people.
- **Scene, surface, or UI context:** nocturnal, light-starved outdoor field with one diagonal dish axis and no descriptive stars.
- **Measurable requirements:** dark plus charcoal area `50–65%`; pale convergence at most `5%`; visibly unequal warm/cool territory; one subject; one governing axis; fine identity texture `3–6%` luminance amplitude at master scale.
- **Constraints:** silhouette reads at thumbnail; dark core remains intact; image uses lost-and-found coloured edges rather than a uniform outline.
- **Avoid list:** Western props, historical costume, people, animals, additional machinery, buildings, text, logos, watermarks, glossy 3D, vector linework, cyberpunk neon, sepia, smooth gradients, and broad white fog.
- **Risk classes:** low human/cultural representation risk because the route contains no person or culturally specific object; ordinary accessibility and asset-permission review still applies.
- **Approval gates:** composition, count, crop, palette relationship, texture, thumbnail Recognition, greyscale, CVD simulation, final encoding, and channel accessibility.
- **Destination:** portrait editorial cover/hero.
- **Assumptions:** sRGB delivery; no live or raster text; no supplied reference image; static output.
- **Blockers:** none for internal proof. Production placement still requires an identified channel, audience, usage permission, and accessible surrounding content.

## Language Context Packet

| Context source | Role in prompt work | Authority | Prompt-facing constraints | Review gates |
| --- | --- | --- | --- | --- |
| `DESIGN.md` | Primary source-free language contract | Highest | One event, carbon majority, unequal thermal fields, silhouette, scarce convergence, particulate edge | Reconstruction and drift rubric |
| `foundations/` | Visual, material, image, voice, and meaning rules | High | Portrait-first field, diagonal axis, lost-and-found edge, matte porous finish, restrained narrative | Thumbnail, crop, light, surface, cultural checks |
| `tokens/`, `components/`, `patterns/`, `applications/` | System and surface constraints | High | Area ratios, palette roles, Scene Plate/Silhouette Anchor, identity intensity | Token, pattern, channel, and component checks |
| `accessibility/` and `outputs/ai-readiness-audit.md` | Accessibility and generated-output controls | High | Greyscale/CVD survival, no essential text, exact count, no invented objects, clean support content | Pass/fail accessibility and AI audit |

Context rules:

- Treat `DESIGN.md` as the highest-authority source-free contract.
- Use support files only to clarify asset route, visible constraints, acceptance gates, and generated-output risks.
- Keep internal records, file locations, permission notes, review notes, and reasoning outside the model-facing prompt.
- Do not reopen original references for ordinary prompt work; run a new extraction only when the user requests it or the package cannot answer a material question.

## Prompt Contract

| Prompt ID | Asset route | Final use | Prompt schema | Acceptance gates |
| --- | --- | --- | --- | --- |
| `EF-ILL-001` | Static illustration, editorial cover, 3:4 portrait, general adult audience | Internal proof, cover/hero baseline | Single image with exact subject/count/regions and no text | One dish; one axis; dark majority; unequal thermal light; scarce peak; grain; no forbidden motifs |

## Contract Fields

- **Subject and key visible details:** exactly one radio telescope; dark filled dish and support structure; recognizable concave dish profile; support legs remain separated; dish tilts diagonally toward the upper left.
- **Scene, backdrop, surface, or UI context:** uninterrupted near-black upper field and sparse mineral ground; no stars, buildings, people, vehicles, labels, or secondary equipment.
- **Composition and spatial relationships:** telescope in lower-middle field, slightly right of center; upper `42–48%` predominantly unoccupied; diagonal dish axis is the only directional gesture.
- **Palette roles and colour proportions:** carbon/charcoal `50–65%`; warm ember ground/spill `18–28%`; cool mineral rim/haze `7–14%`; dust mediation `3–8%`; pale convergence no more than `5%`.
- **Lighting, shadow, and atmosphere:** warm ground plane from lower right; narrower cool rim and haze from upper left; small pale intersection on the dish edge; long soft shadow reinforces the diagonal.
- **Material, texture, finish, and depth:** matte absorptive dark core, dry pigment-like atmosphere, multiscale granular stipple, soft chromatic edge dispersion, low-detail three-plane depth.
- **Typography or exact rendered text:** no text, letters, numerals, marks, signage, captions, logos, or watermark.
- **Reference-image roles:** none.
- **Binding requirements for attributes, counts, and regions:** the warm field binds to lower-right ground; cool light binds to the left/upper dish rim; pale convergence binds to one short rim section; exactly one telescope occupies the midground.
- **Accessibility, localisation, or cultural constraints:** subject and axis survive greyscale/CVD and thumbnail reduction; no culturally specific, human, sacred, historical, or weapon imagery.

## Positive Prompt

Final Positive prompt:

```text
Create a static 3:4 portrait editorial illustration at 1536 by 2048 pixels with exactly one large radio telescope dish as the sole subject. Place the telescope in the lower-middle field, slightly right of centre, with its concave dish tilted diagonally toward the upper left; keep the upper 45 percent as an uninterrupted near-black field and preserve the dish rim, separated support legs, and diagonal stance as a readable dark silhouette at thumbnail size.

Build the image from a light-absorbing carbon-black structural field covering roughly 55 percent of the frame. Let a broad ember-orange ground plane rise from the lower right and occupy about 24 percent, while a much narrower desaturated mineral-cyan rim and haze enters from the upper left and occupies about 10 percent. Attach one small pale frost convergence highlight to a short section of the dish rim, never more than 5 percent of the image. Keep the telescope core dark and opaque; light may stain and erode only selected perimeter regions.

Render the scene as low-detail atmospheric illustration with four to six value bands, matte dry-pigment material, broad soft ground spill, a long soft diagonal shadow, and fine multiscale granular stipple across dark, midtone, and luminous regions. Use lost-and-found particulate edges rather than line art or a uniform glow. The first read is one telescope and one diagonal axis; the second read is unequal warm and cool light; the close read is chromatic grain and softened edge dispersion. No text or additional objects.
```

Prompt assembly checks:

- Asset route appears in the first sentence: pass.
- Subject, action/stance, setting, and focal point are visible: required.
- First two composition instructions are load-bearing: one telescope position and upper-field reserve.
- Palette, surface, and motif rules are concrete: ratios, bindings, finish, and edge behavior are explicit.
- Attributes sit next to the objects they modify: dish, ground, rim, and shadow are bound.
- Counts are grouped by region or role: exactly one telescope, one peak highlight, no secondary objects.
- Exact rendered text is addressed: no text.
- Abstract intent is translated into visible mechanisms: void, axis, light territories, silhouette, and texture.

## Negative Constraints

```text
No people, faces, hats, firearms, cactus, horses, wagons, bison, shelters, saloons, badges, stars, skulls, feathers, rope, historical costume, or frontier decoration. No second telescope, satellite dish cluster, building, vehicle, fence, cables, signage, star field, moon, planet, text, letters, numerals, logo, caption, pseudo-writing, or watermark. No photoreal glossy metal, polished 3D render, wet reflection, clean vector outline, anime linework, sepia, distressed paper, film scratches, leather or wood texture, neon cyberpunk, balanced orange/cyan halves, smooth complementary gradient, broad neutral-white fog, multiple focal flares, full-edge glow, blurry subject core, tiled noise, or obvious JPEG damage.
```

## Variant Strategy

| Variant | Purpose | Single changed variable | Fixed invariants | Review gate |
| --- | --- | --- | --- | --- |
| A — base | Warm-dominant canonical proof | None; uses the Positive prompt as written | One telescope, position, axis, ratios, silhouette, texture, no text/extra objects | All acceptance gates pass |
| B — cool-dominant | Test thermal inversion | Cool field becomes the larger luminous territory and warm becomes the narrow rim | Subject, count, composition, dark majority, peak scarcity, texture, no text | Thermal ownership is visibly unequal and identity remains |
| C — wide crop | Test channel adaptation | Aspect ratio changes to 16:9 | Telescope recognition core, diagonal axis, dark majority, light binding, texture, no extra objects | Width extends empty field rather than cropping/enlarging the dish |
| D — subject transfer | Test module independence | Replace the radio telescope with exactly one wind-bent signal tree built from a dark trunk and sparse branches | 3:4 layout, field ratios, diagonal stance, light binding, texture, no text | Result belongs without becoming a Western or fantasy scene |

Only one changed variable is introduced per variant. If a change requires new cultural, legal, text, audience, or safety decisions, create a new intake rather than a variant.

## Edit Command

No edit command is active for the base route. For a future edit, name one target region, one operation, the new visible state, and repeat all locked invariants: subject count, recognition core, governing axis, thermal inequality, dark majority, peak scarcity, no text, and clean export.

## Handoff Metadata

- **Model or tool:** any image generator capable of region/count control and 3:4 output; record the actual tool and version at execution.
- **Aspect ratio and size:** 3:4, `1536×2048`.
- **Transparent background:** no.
- **Seed or reference setting:** no reference image; record seed only if the tool exposes one.
- **Reference-image permissions:** no reference image is used by the executable prompt.
- **Output naming:** `ef-ill-001-radio-telescope-v01.png`, then increment the version after each accepted revision.
- **Review owner:** unassigned; execution owner must be named before production release.
- **Source-free context files consulted:** `DESIGN.md`, relevant foundations, token/media rules, pattern language, application rules, accessibility, and AI-readiness audit.

## Failure Checks

- **Exact text, extra text, and typography:** fail on any letter, number, signage, logo, pseudo-writing, caption, or watermark.
- **Count, grouping, and object separation:** fail unless exactly one telescope is present and its dish/support structure remains separated and recognizable.
- **Region placement and focal hierarchy:** fail if the dish leaves the lower-middle field, the upper dark reserve falls outside `42–48%`, or another focal event competes.
- **Attribute binding:** fail if warm ground, cool rim, pale convergence, or diagonal shadow attaches to the wrong region or becomes global grading.
- **Palette, material, Lighting, and texture drift:** fail on equal warm/cool area, missing dark core, peak over `5%`, smooth gradient, glossy surface, uniform glow, tiled noise, or compression-like grain.
- **Accessibility, localisation, and cultural risk:** fail if subject/axis disappears in greyscale/CVD/thumbnail, if text is embedded, or if forbidden human/cultural/frontier motifs appear.
- **Asset permission and context leakage:** fail if any unapproved reference pixels, creator names, internal notes, or review metadata appear in the prompt or output.
- **Delivery:** inspect PNG and final JPEG at 100%, thumbnail, 1×/2× density, bright environment, and low brightness before acceptance.
