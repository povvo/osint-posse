# Surface Language

Output path: `foundations/surface-language.md`

## Material Quality

- **Dominant materials:** absorptive carbon, suspended mineral dust, dry pigment, chalky light, coarse paper memory, and soft atmospheric residue.
- **Finish:** overwhelmingly matte and porous. Highlights bloom through particles rather than reflecting from a glossy skin.
- **Weight:** structural darks feel heavy; illuminated edges feel weightless and friable. Maintain this contrast instead of giving every layer equal material density.
- **Temperature:** surfaces receive temperature from light rather than owning a fixed “warm material” or “cool material” identity.
- **Tactility:** visual texture suggests a dry, rubbed, printed, or dust-laden surface. Functional controls remain physically clear and do not imitate grit under the fingertip.
- **Material boundary:** this is a rendered surface language, not a claim that an object is literally paper, film, leather, metal, smoke, or paint. Use physical-material nouns as controlled production cues only.

## Environmental Materiality

- **Hard or soft:** dark cores are hard enough to anchor recognition; atmosphere and illuminated boundaries are soft.
- **Sterile or lived-in:** lived-in through particulate variation, not through scratches, stains, torn edges, or decorative ageing.
- **Industrial, domestic, organic, ceremonial, damaged, polished, or clinical:** organic and ceremonial, with deliberate production control. Avoid both sterile digital smoothness and theme-park rusticity.
- **World texture translated into UI surface:** identity imagery may carry full grain and bloom. UI shells use matte near-black with extremely restrained luminance variation. Content, text, focus, inputs, and critical states receive clean, low-noise surfaces.

## Damage And Wear

- **Pristine, weathered, deteriorating, repaired, layered, patinated, or untouched:** optically weathered but structurally intact. Texture suggests accumulated atmosphere rather than a damaged file or distressed object.
- **Allowed surface history:** fine irregular stipple, subtle density variation, pigment-like clustering, softened chromatic edges, mild value mottling, and occasional particulate gaps.
- **Forbidden surface history:** fake film scratches, dust hairs, folded-paper creases, burned corners, torn edges, leather grain, woodgrain overlays, rust, vignette presets, watermarks, deliberate JPEG blocks, or random “vintage” stains.
- **Repair rule:** if texture damages recognition or legibility, restore the structural core and support surface first. Never compensate by increasing bloom.

## Surface Hierarchy

| Surface role | Material behavior | Depth behavior | Token implication |
| --- | --- | --- | --- |
| Base | Absorptive carbon, almost matte, continuous | Visual zero plane; holds void and silhouettes | `surface.base`, grain `0–1.5%`, no shadow |
| Atmospheric | Transparent particulate colour and low-frequency haze | Sits between base and subject; may pass behind or around it | `surface.atmosphere`, blend opacity `8–36%`, blur scaled to viewport |
| Raised | Slightly lifted charcoal or mineral-black with a crisp boundary | One logical step above the base; no glossy float | `surface.raised`, 1px low-contrast border or restrained shadow |
| Image subject | Opaque dark core plus localized chromatic rim | Principal midground; contour outranks texture | `surface.subject`, edge-spill transform, grain `3–6%` luminance amplitude |
| Overlay | Dense carbon support plate with clean type | Clearly above atmosphere; blocks unstable image contrast | `surface.overlay`, opacity `92–100%`, no backdrop-dependent text |
| Critical | Solid high-contrast plate, crisp icon, explicit label | Highest information plane; unaffected by aesthetic transforms | `surface.critical`, zero grain/bloom, validated contrast |

## Light Construction

Build light in five ordered passes:

1. Establish the near-black structural field and subject core.
2. Add one broad warm or cool ground/atmosphere plane at low spatial frequency.
3. Introduce the opposite temperature as a narrower rim, haze, or counterplane.
4. Add a confined pale convergence zone at the focal event.
5. Apply edge diffusion and particulate continuity without lifting the entire black field.

At a 736px short edge, begin with `4–12px` local edge diffusion and `12–40px` atmospheric bloom, then scale proportionally and review optically. Bloom remains colour-bearing; neutral white glow is rare. Cast shadows are long and soft only when they reinforce the governing axis.

## Craft Signal

- **Where maximum polish belongs:** silhouette design, warm/cool value separation, crop logic, focal hierarchy, noise distribution, and accessibility-critical support surfaces.
- **Where restraint belongs:** borders, shadows, props, highlights, copy, animation, and the number of texture layers.
- **Where visible construction belongs:** slight particulate irregularity and edge contamination may reveal the making process. Grids, masks, repeated noise tiles, compression seams, and obvious blur radii must not.
- **Quality test:** the artifact should feel controlled at normal size, iconic at thumbnail size, and richly irregular only when inspected closely.

## Transparency And Opacity

- **Opaque surfaces:** subject cores, base shell, body-text plates, inputs, dialogs, consent, and critical feedback.
- **Translucent surfaces:** haze, edge spill, nonessential light fields, and decorative atmospheric layers.
- **Blur/glass rules:** blur belongs to atmosphere, not to containers. Avoid backdrop glass; it turns absorptive depth into glossy product chrome.
- **Failure cases:** transparent text plates over variable imagery, stacked semi-transparent cards, additive glows that clip channels, or blur that merges two recognition contours.

## Texture Dosage

- **Texture amount:** full-resolution identity imagery may begin at `3–6%` luminance RMS for fine texture. Calm shells use `0–1.5%`; text, icons, focus, data, and critical surfaces use `0%`.
- **Scale:** combine a mostly pixel-scale fine layer with a much weaker `8–24px` density variation. Do not rely on one enlarged monochrome-noise layer.
- **Repetition:** seed per asset and inspect for tiling. Grain should be stochastic and nearly uncorrelated at short lag; repeated speckle constellations are a defect.
- **Colour behavior:** let warm and cool speckles intensify near territory boundaries while keeping the dark core largely achromatic. Avoid RGB-channel misregistration on functional content.
- **Interaction with text and icons:** mask texture away from glyph strokes and essential icon interiors by at least `2px` at 1×; expand the exclusion region with text scaling.
- **Export:** retain a high-quality master before delivery compression. Chroma subsampling and aggressive JPEG encoding can smear coloured particles; validate the final encoded asset at 100% and on a low-density display.

## Production Drift Checks

- Black plus charcoal should remain the majority of an identity-bearing scene.
- Fine grain must be visible in midtones but not read as compression damage.
- A silhouette blurred to thumbnail size must retain category and stance.
- The brightest region must remain spatially scarce and attached to the focal event.
- If removing the texture layer leaves an otherwise generic orange/cyan gradient, the composition and light structure are underdesigned.

## Anti-Patterns

- Generic noise overlays, uniform opacity grain, obvious tiling, or artificial compression artefacts.
- Glossy glassmorphism, bevels, chrome, wet reflections, plastic 3D surfaces, or soft neumorphism.
- Distressed-paper, saloon-wood, leather, sepia, scratch, and burnt-edge clichés.
- Glow on every edge, broad white fog, clipped highlights, or blur used to hide weak silhouettes.
- Grain behind small text, focus indicators, diagrams, data, legal copy, or controls.
- Treating material adjectives as permission to reduce accessibility or platform clarity.
