# AI-Readiness Audit

Output path: `outputs/ai-readiness-audit.md`

AI generation is constrained assembly, not permission to improvise a parallel design system. The generated artifact must name its retrieved contracts, unresolved gaps, modes, states, and validation results.

## AI-Readiness Controls

| Risk | Prevention rule | Repair rule |
| --- | --- | --- |
| Hallucination of a component | Retrieve the component inventory and pattern selection table before generation; use only canonical component names | Replace with an existing component or record a clearly named component gap for human decision |
| Invented variant or prop | Validate every variant/prop against the component API contract | Remove the prop, choose a purpose-bearing supported variant, or propose a contract change separately |
| Raw values for colour, space, type, radius, shadow, or motion | Static-scan generated code/prompts for raw values outside approved media recipes | Bind to a `component.*` or `semantic.*` token and regenerate all modes |
| Unsupported states | Build a state inventory before UI generation and compare it with required default, hover, Focus, pressed, Selected, disabled, Loading, warning, error, success, empty/offline, and Recovery behavior | Add the missing contractually supported state; do not invent a visual state without semantics and recovery |
| Broken token mapping | Resolve the canonical graph and reject component references below the semantic layer | Repair the token path at the correct layer and regenerate platform artifacts |
| Mode omission | Require light, dark, high-contrast, and Reduced-motion outputs/tests for relevant components | Add mode transforms upstream; never patch one screenshot or component |
| Platform flattening | Select native Platform pattern before rendering visual tokens | Replace web-like custom chrome with native equivalent while preserving semantic intent |
| Inaccessible generated UI | Run semantic, Keyboard, Focus, contrast, target, text-scaling, CVD, motion, label, error, and Recovery checks | Repair component/state/content contracts before adjusting aesthetics |
| Invented data or product claim | Use supplied typed data and mark missing fields; never fill unknown price, status, identity, history, measurement, or completion | Request/route the missing value or render a truthful unavailable/loading/error state |
| Exact text/count failure in imagery | Keep essential text live; when text/count is genuinely part of an asset, verify every string/object/count after generation | Regenerate or edit with a deterministic layout tool; do not ship pseudo-text |
| Object-binding failure | Prompt and review subject, count, relationship, axis, and focal light as separate constraints | Simplify composition, rebind the light/prop to the intended subject, and recheck thumbnail recognition |
| Prompt drift | Use the canonical prompt slots and negative constraints; ban creator names and vague mood-only prompts | Rebuild from observable facts, one scene family, tokens, and failure checks |
| Visual overfitting | Require subject/module variation while retaining mass/light/space/texture invariants | Remove copied scene arrangement or prop dependence; rebuild with a different subject and axis |
| Unlicensed asset reuse | Generate from source-free operational facts and use only assets with explicit production permission | Remove the asset/pixel derivative and substitute newly commissioned, generated, or licensed material |
| Cultural stereotype | Require module-specific context review for land, migration, firearms, Indigenous-coded forms, animals, and historical costume | Remove the module or replace it with researched context; never claim generic authenticity |
| Stale context | Attach package/version/hash to generated output and fail when referenced token/component IDs no longer resolve | Refresh retrieval, migrate deprecated IDs, and regenerate |
| High-stakes automation | Require domain review, confirmation, audit, error, and Recovery contracts; prohibit inferred completion or consent | Return a bounded draft and flag the unresolved review rather than simulating approval |

## Machine-Readable Context

- **Component contracts:** canonical name, purpose, anatomy, variants, states, token dependencies, content schema, accessibility, Keyboard, responsive behavior, API, and forbidden props.
- **Pattern schemas:** canonical Taxonomy term, parent, related/conflicting patterns, selection intent, required components/tokens, and anti-patterns.
- **Token grammar:** typed primitive → global → alias → semantic → component graph, mode precedence, platform transforms, and drift rules.
- **Repository instructions:** read order, generated-file boundary, validation commands, naming, mode/platform matrix, and change protocol.
- **Generated-output review:** artifact type, intended use, retrieved IDs, declared gaps, state/mode coverage, accessibility results, asset permissions, and reviewer status when one exists.
- **Prompt context:** scene family, subject/count, relationship, axis, palette territories, area ratios, light binding, texture recipe, crop metadata, negative constraints, and failure tests.

## Context Retrieval Order

1. Read `SKILL.md`, which routes to `DESIGN.md`.
2. Read the Use Contract, Design DNA, Accessibility, Drift Boundaries, and relevant application recipe.
3. Retrieve only the component, pattern, token, and platform files needed by the task.
4. For visual assets, retrieve imagery, palette, spatial, surface, application, and prompt guidance.
5. For functional UI, retrieve component/state, semantic/component/mode/platform tokens, and accessibility guidance.
6. Load audit/handoff material only for review tasks, never as ordinary production prompt content.

## Generation Contract

Before producing output, the agent states internally:

- user goal, channel, Platform, Domain, density, and modes;
- selected canonical patterns and components;
- data/content fields supplied versus missing;
- state and Recovery map;
- token paths and permitted overrides;
- accessibility and localization obligations;
- any asset/cultural review boundary.

After producing output, the agent validates:

- no raw values, invented components, unsupported variants, or missing states;
- no essential text baked into imagery;
- all token paths and mode branches resolve;
- Platform behavior is native-equivalent;
- contrast, CVD, Keyboard, Focus, target, text scaling, and Reduced motion pass;
- identity media meets one-event, silhouette, thermal, convergence, and texture checks;
- unknown claims remain unknown and permissions are respected.

## Generated UI Decision Rule

```text
If a canonical component supports the purpose:
  use it with documented variants and states.
Else if a documented pattern composes existing components:
  assemble that pattern.
Else:
  stop, emit a component/pattern gap, and request a decision.
```

An ephemeral or predictive interface is not exempt. It must still expose stable labels, state, undo/Recovery, accessibility semantics, and a way to understand why an action is available.

## Raw Values Policy

- Application and component code may not hard-code brand colours, spacing, type, radius, shadow, duration, easing, or texture.
- Dynamic geometry derived from content may be permitted with documented bounds; it must not substitute for semantic spacing/state.
- Generated media recipes may contain resolution-relative formulas from the package, not copied raw pixel effects.
- An exception requires purpose, scope, owner when known, expiry/review trigger, and a reason an existing token is incorrect.

## Unsupported States Policy

- A visual state without a semantic/behavioral contract is rejected.
- A semantic state without visible, non-colour, accessible feedback is rejected.
- Loading without task label, error without Recovery, success without a known result, disabled without clear prerequisite where useful, and Selected without state semantics are rejected.
- Unknown outcome never maps to success; it maps to pending/unknown with verification.

## Prompt Review Gates

- Exact subject category, count, relationship, and axis.
- Warm/cool area remains unequal and the pale convergence remains scarce.
- Dark structural core survives thumbnail and greyscale.
- Grain is multiscale, nonrepeating, and absent from functional information.
- No creator name, copied composition, pseudo-text, watermark, brand mark, or culturally unsafe shorthand.
- All output ratios preserve recognition core and safe-text metadata.

## Anti-Patterns

- Giving an agent the whole archive when a routed context packet would be safer and clearer.
- Asking for “something on-brand” without use case, state, platform, or constraints.
- Accepting visually plausible output that invents data, copy, props, components, or completion.
- Adding a raw colour because the nearest token “doesn’t look right” instead of repairing the semantic/transform layer.
- Treating AI review as optional after prompt quality appears high.
