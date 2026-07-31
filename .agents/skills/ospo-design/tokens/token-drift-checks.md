# Token Drift Checks

Output path: `tokens/token-drift-checks.md`

Drift is any divergence between the canonical token graph, generated platform artifacts, component bindings, rendered accessibility behavior, and the visual reconstruction contract. Automated checks gate structural errors; perceptual checks gate atmosphere and recognition.

## Drift Detection Rules

| Drift type | Detection method | Repair action |
| --- | --- | --- |
| Hard-coded raw value | Scan application and component source for hex, `rgb()`, `hsl()`, `oklch()`, shadows, radii, spacing, font sizes, durations, and cubic-bezier values outside generated files and an explicit exception manifest | Replace with the nearest semantic/component token; add a scale value only when the existing graph cannot express a recurring purpose |
| Broken alias | Parse every `{path.reference}`, verify existence/type, build a directed graph, and reject cycles or chains deeper than the permitted layers | Restore the missing target, correct the type, or migrate through a documented one-release deprecation alias |
| Layer inversion | Detect component references to `primitive.*`, `global.*`, or `alias.*`; detect semantic references to component tokens | Bind component property to a semantic intent; move raw material back to the proper lower layer |
| Mode divergence | Expand every token for light, dark, high contrast, and reduced motion; compare required token sets and unresolved branches | Add the missing mode override or document an intentional invariant; never patch one component locally |
| Platform divergence | Compare canonical graph hash, transform version, name map, and resolved values across generated CSS/Swift/Android/XAML/TypeScript manifests | Regenerate all artifacts from one canonical input and remove handwritten edits |
| Component override sprawl | Count local overrides by component/property; flag repeated values, raw values, and more than two unexplained overrides for the same property family | Promote a recurring purpose to a component variant or semantic token; remove decorative or duplicate overrides |
| Contrast failure | Render actual text, icon, focus, status, and boundary pairs after opacity/compositing; test declared WCAG 2.2 obligations and forced/high-contrast modes | Repair at the semantic or mode token, add a stable support surface, or change weight/size; never add glow |
| Typography drift | Compare family, size role, weight, line-height, tracking, fallback metrics, and user-scaling behavior against semantic roles | Rebind to the semantic type role; fix platform transform rather than hard-coding a local size |
| Spacing drift | Quantize fixed gaps and insets to the 4px primitive/8px cadence; flag one-off constants and target reductions | Use the nearest global/semantic step; keep hit target independent from visible compactness |
| Motion drift | Scan for unapproved keyframes, springs, durations over functional ceilings, infinite animation, and missing reduced-motion branches | Bind to semantic motion purpose, remove decoration, add a static state cue, and honour user settings |
| Status drift | Detect status colours without icon/text/shape redundancy or status tokens reused as decorative accents | Restore semantic status component, explicit copy, accessible announcement, and recovery path |
| Media palette drift | Sample identity art for dark structural area, thermal imbalance, pale-peak area, and broad neutral-white clipping | Rebuild field hierarchy before colour grading; restore unequal warm/cool territories and scarce convergence |
| Silhouette drift | Downsample or blur to thumbnail and run human recognition check for subject category, count/relationship, and governing axis | Simplify contour, open negative cuts, remove interior detail, or enlarge the recognition core |
| Texture drift | Measure/inspect identity grain amplitude, frequency, tiling, and masks; verify zero texture on functional content | Regenerate multiscale grain at output resolution, remove tile/repetition, and expand clean-content mask |
| Content drift | Scan for unlabeled icon controls, embedded translatable text, faux-frontier copy, and unsupported cultural/historical claims | Add clear labels, externalize text, rewrite plainly, and route sensitive modules through review |

## Quantitative Guardrails

| Contract | Target | Severity |
| --- | --- | --- |
| Identity dark plus charcoal area | `50–65%` ordinary target; higher allowed for documented sparse variants | Warning outside target; fail if the structural field no longer reads |
| Thermal area | Default saturated hot:cool approximately `3:1–7:1`; intentional inversion still requires visibly unequal ownership | Warning near equality; fail if the result becomes a balanced split or generic grade |
| Pale convergence | At most `5%` of identity frame | Warning above `5%`; fail when broad white light becomes a field |
| Fine identity texture | `3–6%` luminance amplitude at master scale; shell `0–1.5%`; functional `0%` | Fail on functional content; warning outside image range |
| Functional interaction feedback | Begins within `100ms`; routine transitions under `500ms` | Fail for delayed essential feedback or missing reduced-motion parity |
| Text contrast | Meet the declared WCAG 2.2 criterion at actual size/weight | Fail |
| Essential non-text/focus contrast | At least `3:1` where the criterion applies; focus geometry also validated | Fail |
| Touch target | Platform design target, with web shared target `44×44 CSS px`, iOS `44×44pt`, Android `48×48dp`, and native/stricter rules honoured | Fail when current applicable requirement is unmet |
| Body text | `1rem` web-equivalent floor, weight `400+`, user scaling and 200% reflow supported | Fail for blocked scaling/clipping; warning for unreviewed exceptions |
| Token reference depth | Primitive → global → alias → semantic → component, with no reverse or skipped component binding | Fail |

Quantitative image tests are screening tools. They do not replace optical review of silhouette recognition, colour interaction, cultural meaning, or texture quality.

## Scan And Exception Policy

- Scan source, stylesheets, generated prompts, design exports, and native resources. Exclude generated token artifacts by manifest rather than directory-name guesswork.
- Raw-value exceptions require an owner, purpose, file/line locator, expiry or review date, and reason a token would be incorrect.
- Dynamic values derived from user content or geometry may be exempt, but their bounds and semantic purpose must still be documented.
- A colour that happens to equal a token value is still hard-coded if it does not reference the token.
- Delete expired exceptions before release; do not roll them forward automatically.

## CI Severity

- **Build error:** unresolved reference, cycle, type mismatch, layer inversion, missing required mode, contrast failure, inaccessible focus, component raw value, or failed generated-artifact hash.
- **Release blocker after review:** illegible silhouette, equalized thermal fields, broad convergence light, texture on functional content, culturally unsafe module, or missing recovery.
- **Warning:** orphan primitive, unused semantic token, scale outlier, undocumented transform approximation, or quantitative media metric outside the ordinary range.
- **Information:** token count, mode coverage, platform artifact hashes, exception count, deprecation list, and unused variant report.

## Repair Order

1. Confirm the intended user-facing purpose.
2. Repair semantic meaning or component binding before adjusting appearance.
3. Repair mode behavior before a platform exception.
4. Repair the canonical token or transform before a generated artifact.
5. Re-run all modes, platforms, contrast checks, and perceptual reconstruction checks.
6. Remove the obsolete local override and exception record.

## Hygiene Rules

- Do not collapse primitive, global, alias, semantic, component, mode, platform, transform, and drift outputs into one file.
- Do not ship orphan primitives, unused semantic tokens, undocumented component overrides, unresolved deprecations, or stale exception manifests.
- Detect raw values in code and design artifacts before handoff.
- Record canonical-input and generated-output hashes so a platform file cannot silently drift.
- Review token additions by purpose, not by visual similarity or convenience.

## Anti-Patterns

- Suppressing scan results with broad globs, allowlisting a whole application, or accepting contrast warnings as nonblocking.
- Repairing a component screenshot while leaving the semantic or transform error intact.
- Treating approximate image metrics as proof of authorship, medium, or exact stylistic fidelity.
- Adding aliases until a broken architecture “resolves,” or keeping deprecated aliases permanently.
- Declaring parity because hex values match while typography, focus, density, motion, or user preferences diverge.
