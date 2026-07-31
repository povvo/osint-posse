# Motion Personality

Output path: `foundations/motion-personality.md`

## Temporal Character

- **Mechanical, fluid, decelerating, accelerating, rhythmic, disrupted, calm, tense, or still:** tense stillness punctuated by slow, decelerating reveals and brief functional responses.
- **Dominant pacing:** the scene holds longer than expected, then one layer changes along the established compositional axis. Functional controls remain immediate; atmosphere never delays task completion.
- **Emotional meaning of the pacing:** stillness signals watchfulness and weight. A reveal feels like light finding form, not a card performing a trick.
- **Extension boundary:** motion is a conservative extension of a still-first language. When movement does not clarify feedback, causality, orientation, or state, omit it.

## Easing Model

| Motion family | Easing or physics | Duration range | Usage |
| --- | --- | --- | --- |
| Immediate confirmation | Linear or `cubic-bezier(0.2, 0, 0, 1)` | `80–140ms` | Press, toggle response, focus acknowledgement, compact selection |
| Functional reveal | `cubic-bezier(0.16, 1, 0.3, 1)` | `180–300ms` | Disclosure, menu, panel, state detail |
| Axis transition | `cubic-bezier(0.2, 0.75, 0.2, 1)` | `260–420ms` | Scene or section move that follows a vertical, horizontal, radial, or route axis |
| Atmospheric emergence | Opacity plus `cubic-bezier(0.22, 1, 0.36, 1)` | `420–800ms` | Nonessential hero reveal, haze, light pool, title sequence |
| Exit/withdrawal | `cubic-bezier(0.4, 0, 1, 1)` | `120–220ms` | Dismissal, collapse, completed transient feedback |
| Error interruption | No spring; short ease-out plus stable stop | `120–180ms` | Explicit error appearance with text and icon; no shaking required |

Use transforms and opacity where possible. Do not animate expensive blur, full-field grain, or colour filters continuously on constrained devices.

## Functional Motion

- **Orientation:** move content parallel to the composition’s governing axis. A processional view advances along its route; a gathering reveals radially or by opacity; a vigil enters with minimal vertical displacement.
- **State change:** change one property family at a time—visibility, position, scale, or emphasis. Combine opacity with at most one small transform.
- **Causality:** motion begins at the invoked control or focal event and resolves at the affected surface. Never animate from an arbitrary screen edge when the trigger is local.
- **Continuity:** persistent subjects retain position and scale between related states. New information emerges from the dark field or support surface without replacing the whole scene.
- **Feedback:** interaction feedback starts within 100ms. Success, error, and completion use stable text/icon/state changes; atmosphere is secondary.
- **Loading:** prefer a static dark mass with one progressively revealed edge or a determinate route. For indeterminate waits, use a restrained opacity cycle on a small indicator outside the image and provide a text label.

## Rhythm Pattern

- **Metronomic, organic, staggered, interrupted, delayed, or absent:** organic, sparse, and gently staggered.
- **Sequencing rule:** reveal the structural field, then the subject core, then the luminous edge, then supporting text or controls. Use `40–80ms` offsets and no more than four staggered groups.
- **Expectation and violation:** establish stillness first. A single axis-following transition may break it; repeated decorative entrances, bouncing idle states, and constant drift destroy the register.
- **Repetition rule:** repeated subjects may appear with decreasing delay to imply depth, but functional lists should use standard immediate rendering for efficiency and accessibility.

## Transition Type

- **Moment-to-moment:** crossfade or small transform within the same focal event; preserve its silhouette.
- **Action-to-action:** immediate functional response, then a slower contextual reveal if useful.
- **Subject-to-subject:** hold the dark field while one silhouette recedes and another resolves; avoid morphing unrelated shapes.
- **Scene-to-scene:** fade through the void or travel along the established route. Keep total transition below `500ms` for product navigation; longer sequences are opt-in editorial media only.
- **Aspect-to-aspect:** dissolve between atmospheric details while the structural composition remains fixed.

## Entry And Exit Motion

- **Entry behavior:** dark core first, coloured rim second. Limit translation to `8–24px` for UI and `2–5%` of the short viewport dimension for editorial scenes.
- **Exit behavior:** faster and quieter than entry. Reduce opacity or withdraw along the same axis; do not explode into particles.
- **Persistent motion:** none by default. Optional ambient haze or grain drift must be subtle, user-controllable, paused when off-screen, and absent behind text.
- **Interrupted motion:** accept input immediately. Reverse or retarget from the current interpolated state; never queue multiple long transitions.

## Stillness Specification

- **When nothing should move:** while the user reads, decides, enters data, handles consent, reviews an error, or observes the main scene after entry.
- **What stillness communicates:** confidence, space, unresolved tension, and respect for the focal event.
- **How stillness competes with feedback:** it does not. Essential feedback appears promptly through crisp text, icon, shape, and contrast; the surrounding atmosphere remains still.
- **Protected elements:** body text, focus rings, critical alerts, principal recognition contours, and fine particulate texture do not shimmer, jitter, breathe, or pulse.

## Reduced-Motion Translation

- **Non-motion substitutes:** immediate cuts, stable before/after composition, opacity changes under `150ms`, explicit labels, progress values, and static directional markers.
- **State-change backup:** every animated state also changes text, icon, position in the accessibility tree, or a solid boundary. Preserve hierarchy without requiring perceived travel.
- **Forbidden motion:** parallax, zoom-through-depth, continuous grain or smoke drift, rapid thermal colour cycling, camera shake, flashes, large-area wipes, and auto-playing processions.
- **Preference handling:** honour the platform reduced-motion setting on first render and expose a product-level control for any optional editorial animation.

## Anti-Patterns

- Bouncy springs, elastic overshoot, playful squash-and-stretch, or slot-machine celebration.
- Infinite pulsing glows, animated chromatic aberration, glittering grain, or decorative embers.
- Long cinematic transitions placed on navigation, authentication, checkout, error recovery, or repeated workflows.
- Uninterruptible sequences, delayed feedback, hover-only meaning, or movement that precedes the user’s action.
- Multiple axes moving at once, unrelated parallax layers, or morphs that erase subject recognition.
