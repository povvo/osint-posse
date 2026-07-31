# Pattern Language

Output path: `patterns/pattern-language.md`

## Taxonomy

| Term | Definition | Parent | Related terms | Forbidden synonyms |
| --- | --- | --- | --- | --- |
| Absorptive Field | A continuous dark-majority plane that conceals nonessential detail and protects one event | Perceptual foundation | Clean Support, Silhouette Anchor, Thermal Opposition | Black background, dark theme, void decoration |
| Thermal Opposition | Unequal ember/mineral light territories whose near-opposition organizes depth and attention | Perceptual foundation | Luminous Convergence, Particulate Edge | Teal-and-orange filter, complementary gradient |
| Silhouette Anchor | A dark subject mass that preserves category, count, stance, and relationship at thumbnail size | Perceptual foundation | Iconic Vigil, Paired Encounter, Processional Passage | Shadow person, faceless character, cutout |
| Luminous Convergence | A scarce pale intersection attached to the primary event | Perceptual foundation | Thermal Opposition, Luminous Gathering | White glow, bloom layer, highlight everywhere |
| Particulate Edge | A lost-and-found boundary formed by chromatic grain around an intact structural core | Surface pattern | Silhouette Anchor, Thermal Opposition | Noise filter, film damage, chromatic aberration |
| Singular Axis | One vertical, horizontal, radial, curved, or diagonal gesture that governs reading and motion | Spatial pattern | All scene families, Quiet Disclosure | Composition line, decorative streak |
| Iconic Vigil | One principal silhouette held in a large field with a directional expectation | Scene pattern | Silhouette Anchor, Singular Axis | Cowboy hero, lone gunman, character poster |
| Luminous Gathering | Multiple dark masses bracket or encircle one shared bright center | Scene pattern | Luminous Convergence, Clean Support | Campfire scene, ritual aesthetic, round layout |
| Paired Encounter | Two related masses use imperfect symmetry, thermal difference, or gap to express relation | Scene pattern | Silhouette Anchor, Singular Axis | Duel, lawmen, versus screen |
| Processional Passage | Repeated masses diminish along a curved or diagonal route to create time and depth | Scene pattern | Singular Axis, Sequence Progress | Wagon trail, migration aesthetic, carousel |
| Clean Support | Opaque, low-texture surface that makes information independent of imagery and crop | Functional-perceptual bridge | Absorptive Field, Explicit Recovery | Glass card, caption scrim, text glow |
| Quiet Disclosure | A brief axis-consistent reveal that clarifies state without disturbing the field | Behavioral pattern | Singular Axis, Clean Support | Cinematic animation, slow mode |
| Explicit Recovery | Error or interruption state that preserves context, names the problem, and offers repair | Behavioral-functional pattern | Clean Support, Feedback Status | Error toast, try again later |
| Stable Completion | A persistent result state with affected object, receipt/history, and next action | Behavioral-functional pattern | Explicit Recovery, Sequence Progress | Celebration screen, success confetti |
| Native Shell | Platform-conventional navigation, controls, focus, forms, and permissions carrying restrained visual tokens | Platform pattern | Clean Support, Quiet Disclosure | Cross-platform skin, web view everywhere |
| Narrative Module | Optional contextual subject, prop, setting, or domain detail inserted after core grammar is established | Domain/brand pattern | Scene families, cultural review | Brand motif, frontier asset, authenticity cue |

## Pattern Grammar

- **Naming rules:** use purpose or perceptual function, not colour, component location, scene prop, historical period, or mood adjective. Singular noun phrases are preferred.
- **Relationship rules:** every scene pattern requires Absorptive Field, Silhouette Anchor, Thermal Opposition, Singular Axis, and Particulate Edge. Luminous Convergence is optional but scarce. Functional content within or beside a scene requires Clean Support.
- **Functional/perceptual/domain/platform separation:** functional patterns describe what a person can do; behavioral patterns describe state and time; perceptual patterns describe recognition; domain patterns add real vocabulary/constraints; platform patterns select native implementation.
- **Anti-pattern handling:** name the failure, explain which contract it violates, and route to the nearest valid pattern. Do not create a decorative variant to preserve a failed idea.
- **Rationale style:** state user intent, perceptual or behavioral mechanism, required components/tokens, accessibility boundary, and why a simpler neighbouring pattern is insufficient.
- **Historical truth:** rejected alternatives are recorded as current design decisions, not claims about original authorship, period, medium, or cultural history.
- **Alias rule:** informal shorthand may appear in discussion, but documentation and APIs use canonical terms. Forbidden synonyms must not become component or token names.

## Pattern Selection

| Intent | Choose | Required Relationships | Do not choose when |
| --- | --- | --- | --- |
| Make one subject iconic or watchful | Iconic Vigil | Absorptive Field, Silhouette Anchor, Singular Axis, Thermal Opposition | The task requires comparison or identifiable real-person detail |
| Show shared attention or negotiation | Luminous Gathering | Multiple Silhouette Anchors, Luminous Convergence, radial axis | Cultural context makes ceremonial reading unsafe or the center is merely decorative |
| Express a relationship between two entities | Paired Encounter | Two anchors, gap, imperfect symmetry, thermal difference | A versus/duel reading would distort the meaning |
| Express distance, movement, or sequence | Processional Passage | Route axis, scale decay, overlap, atmospheric depth | Exact progress is required without an explicit labelled sequence |
| Place text or controls near identity imagery | Clean Support | Opaque surface, semantic text/focus, texture mask | Image region already has stable tested contrast and content is nonessential |
| Reveal related content | Quiet Disclosure | Trigger ownership, focus contract, reduced-motion state | The change is urgent, blocking, or should be immediate |
| Handle failure/interruption | Explicit Recovery | Error scope, preserved state, retry/alternate/escalation | Never—every failed functional pattern needs a recovery route |
| Confirm durable success | Stable Completion | Result, affected object, next action, optional undo/receipt | The operation is still pending or outcome unknown |
| Adapt to device/platform | Native Shell | Semantic token mapping and platform component | A custom shell would discard native navigation/focus/permission expectations |
| Add setting, object, or subject specificity | Narrative Module | Cultural/rights review and at least five core identity cues | The module is only a cliché or substitute for grammar |

## Pattern Relationships

### Parent–Child

- Perceptual foundations parent the scene patterns.
- Scene patterns parent composition recipes and generated prompt variants.
- Functional components parent behavioral states such as loading, error, and completion.
- Native Shell parents platform variants of actions, forms, navigation, and feedback.
- Narrative Module extends a scene or domain module but never parents identity.

### Required

- `Iconic Vigil → Absorptive Field + Silhouette Anchor + Singular Axis + Thermal Opposition`.
- `Luminous Gathering → Silhouette Anchors + radial Singular Axis + Luminous Convergence`.
- `Paired Encounter → two Silhouette Anchors + unequal spacing/temperature`.
- `Processional Passage → Silhouette Anchors + curved/diagonal Singular Axis + scale decay`.
- `Particulate Edge → intact Silhouette Anchor`; texture cannot repair a weak core.
- `Quiet Disclosure → Focus contract + reduced-motion translation`.
- `Explicit Recovery → Clean Support + status semantics + named action`.

### Related

- Luminous Gathering and Processional Passage can appear in one sequence, but not as competing geometries inside one frame.
- Clean Support may sit within any scene pattern and is mandatory for critical functional content.
- Stable Completion follows a sequence, action, or background task; Explicit Recovery is its non-success sibling.
- Native Shell carries all functional/behavioral patterns across platforms while perceptual tokens adapt.

### Conflicting

- Iconic Vigil conflicts with dense comparison views.
- Particulate Edge conflicts with small text, data, focus, and essential icons.
- Quiet Disclosure conflicts with urgent Alerts that require immediate explicit response.
- Luminous Convergence conflicts with multiple simultaneous focal events.
- Narrative Module conflicts with generic prop repetition or unsupported cultural authenticity.

### Deprecated Or Forbidden

- `Teal Orange Filter` → replace with Thermal Opposition.
- `Grunge Overlay` → replace with Particulate Edge plus clean-content mask.
- `Cowboy Card` → choose a functional Card and optional reviewed Narrative Module.
- `Mystery Interaction` → replace with labelled action, Quiet Disclosure, and explicit state.
- `Cinematic Error` → replace with Explicit Recovery.

## Pattern Record Contract

Every new pattern record states:

- canonical name and purpose;
- parent and related/conflicting patterns;
- required semantic/component tokens;
- required components and states;
- platform and domain variants;
- content and accessibility behavior;
- anti-patterns and migration route;
- design rationale and a review example;
- owner/review signal only when a governance context exists.

If these fields cannot be completed, the proposal is a one-off composition or an unresolved gap, not a system pattern.

## Anti-Patterns

- Naming patterns after colours, pages, props, creators, campaigns, or temporary implementations.
- Treating every repeated visual detail as a pattern or every component as generic.
- Combining Iconic Vigil, Luminous Gathering, Paired Encounter, and Processional Passage in one frame.
- Using “Rationale” to invent strategy, history, or cultural authority.
- Creating pattern aliases without deprecation, or allowing forbidden synonyms into token/API names.
- Choosing a perceptual pattern when the user’s need is functional clarity, exact data, identity, or Recovery.
