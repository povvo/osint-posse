# Spatial Grammar

Output path: `foundations/spatial-grammar.md`

## Composition Type

- **Progressive compression, expansion, convergence, containment, inversion, field, grid, or hybrid:** a field-and-axis hybrid. The expressive layer is a sparse cinematic field; the information layer uses an orderly 8px-based grid.
- **Primary composition law:** one iconic event occupies the middle or lower field while uninterrupted darkness surrounds or rises above it. Every scene has one governing gesture: vertical ascent, horizontal aim, radial gathering, paired stance, curved passage, or diagonal recursion.
- **Secondary composition law:** a single luminous plane or route counterbalances the dark subject mass. Supporting forms appear in small, irregular groups rather than an evenly distributed pattern.
- **Reading order:** silhouette or cluster first, governing axis second, atmospheric territory third, particulate detail last.

## Figure-To-Ground

- **Focal scale relationship:** an iconic portrait may occupy 38–70% of frame height; a relational cluster 30–58%; a procession begins with one mass at 18–36% and decays rapidly into smaller repeats.
- **Dominance or subordination:** subjects dominate through contour and contrast, not surface detail. The ground remains visually active but semantically subordinate.
- **Reversal moments:** a light pool or route may temporarily become the figure while dark bodies become enclosing ground. Use this reversal only once per composition.
- **Background participation:** the background conceals, separates, and establishes atmosphere. It should not accumulate descriptive scenery merely to fill space.
- **Thumbnail requirement:** blur or reduce the composition to 10% size. The subject category, main count or relationship, and governing axis must still read.

## Power Axis

- **Vertical axis:** ascent, apparition, vigil, or monumental atmosphere.
- **Horizontal axis:** tension, directed attention, threshold, or opposition.
- **Radial axis:** gathering, negotiation, ritual, or shared focus.
- **Diagonal or curved axis:** travel, migration, pursuit, or depth.
- **Centered versus off-axis:** center the primary mass for archetypal stillness; shift it off-axis only when the empty region carries a clear directional expectation.
- **Authority signal:** stable stance, low visual center of gravity, broad dark mass, and uninterrupted surrounding field.
- **Deference or tension signal:** unequal spacing, cropped foreground brackets, temperature imbalance, or an axis that extends toward an unseen destination.

## Containment

- **Barriers:** avoid decorative borders. Containment comes from the viewport, dark void, foreground occlusion, terrain walls, or a concentrated light pool.
- **Frames:** identity plates prefer a 3:4 portrait frame. Functional surfaces may use any ratio but should preserve the one-event hierarchy.
- **Crops:** crop secondary atmosphere before recognition contours. Do not cut the identifying bend of a limb, head profile, animal hump, wheel, route turn, or other category-defining feature.
- **Safe areas:** keep the recognition core inside the central 72% of width and 76% of height when multi-format delivery is expected. Reserve a calm text zone of at least 32px or 8% of the short edge, whichever is larger.
- **Edge behavior:** allow one directional element or atmospheric field to touch or exceed an edge. Keep all other major masses comfortably inset so the escape feels intentional.
- **Support containers:** UI and copy use opaque, low-texture surfaces with `8–16px` internal padding on compact controls and `24–40px` on content panels.

## Depth And Layering

| Plane | Contents | Depth mechanism | Interaction rule |
| --- | --- | --- | --- |
| Foreground | Shadow, cropped bracket, enlarged subject fragment, or opening route | Scale, occlusion, low-detail dark mass, directional crop | May frame or lead; must not block the only recognition cue or essential control |
| Midground | Principal subject, relational cluster, focal light pool | Strongest contour, highest local temperature contrast, limited pale convergence | Owns the primary event and receives focus or narrative emphasis |
| Background | Sparse landmark, atmosphere, receding repetitions, terrain wall | Scale diminution, haze, reduced chroma, softened edge, value compression | Establishes direction and context; remains noninteractive unless promoted to the midground |
| Void | Unoccupied dark field | Tonal continuity and absence of detail | Protects hierarchy, houses quiet copy, and absorbs transitions |

Use four z-bands for implementation: `void 0`, `atmosphere 10`, `subject 20`, `information 40`. Temporary overlays begin at `60`; critical dialogs and system permission surfaces remain crisp and unaffected by atmospheric transforms.

## Density Profile

- **Sparse, dense, variable, compressed, breathable, or cinematic:** cinematic and sparse for identity; ordinary task-appropriate density for functional screens.
- **Density by screen class:** on narrow screens, reduce supporting objects before reducing the principal subject below recognition size. On wide screens, expand the void and directional field rather than duplicating focal content.
- **Density by state:** resting states show one accent and few labels; active states may reveal one additional control cluster; error and recovery states become more explicit, not more atmospheric.
- **Minimum touch and reading comfort:** maintain platform touch-target floors independently of visual compactness. Use at least 44×44 CSS px on touch surfaces unless a stricter platform rule applies.
- **Spacing cadence:** use a 4px primitive with an 8px default rhythm: `4, 8, 12, 16, 24, 32, 48, 64, 96`. Large scene gaps may use proportional values, but controls remain on the core cadence.

## Responsive Composition Families

| Family | Governing geometry | Narrow adaptation | Wide adaptation |
| --- | --- | --- | --- |
| Iconic vigil | One dominant vertical mass plus one thin directional cue | Preserve full contour; shorten the cue only after protecting its direction | Keep subject near a third; expand the expected-action side |
| Luminous gathering | Dark brackets around a bright center | Stack copy outside the light pool; reduce peripheral props | Increase ring spacing while keeping the center singular |
| Paired encounter | Two related vertical masses with imperfect symmetry | Preserve both silhouettes; crop atmosphere first | Separate slightly and allow a larger tension gap |
| Processional passage | Curved or diagonal route with decaying repeated masses | Retain the first mass, one intermediate, and destination cue | Extend the route and add depth, not lateral clutter |

## Gestalt Relationships

- **Proximity:** proximity defines alliance or gathering; wide gaps create suspicion, solitude, or scale.
- **Similarity:** repeated silhouettes establish category and rhythm, but size, temperature, or stance must vary enough to avoid mechanical cloning.
- **Enclosure:** use darkness, terrain, foreground shoulders, or a light pool instead of stroked boxes.
- **Continuity:** a rifle-like line, gaze, shadow, path, plume, table edge, or herd diagonal should carry the eye through the event.
- **Common region:** reserve conventional cards and dividers for information architecture. Expressive content shares a region through light and atmospheric continuity.

## Optical Notes

- **Optical centering:** dark silhouettes often feel heavier than their bounds. Offset them 1–3% toward the brighter side or open side after visual review.
- **Overshoot:** hats, horns, smoke, and soft halos may exceed geometric alignment by 1–2% to appear optically even.
- **Stroke and border perception:** textured or glowing edges appear thicker. Essential UI outlines remain crisp and may need lower nominal width than a neighbouring soft rim.
- **Asymmetric spacing compensation:** give the dark or visually dense side more breathing room; do not enforce mathematical symmetry when temperature and mass are unequal.

## Anti-Patterns

- Evenly filling the frame, centering every element, or distributing props like a catalogue.
- Multiple focal flares, competing axes, excessive landmarks, or explanatory background detail.
- Card grids or hard boxes imposed over the expressive field without a functional reason.
- Cropping away recognition contours to preserve a rigid aspect ratio.
- Fake depth from heavy drop shadows, glossy elevation, or indiscriminate parallax.
- Treating cinematic sparsity as permission for tiny controls, unlabeled navigation, or inefficient task layouts.
