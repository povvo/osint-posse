# Documentation As Context

Output path: `outputs/documentation-as-context.md`

Documentation is an executable context system. A human or agent should be able to select a pattern, build an artifact, implement states, and review drift without private knowledge or reopening reference material.

## Documentation Contract

| Artifact | Human guidance | Machine guidance | Rationale |
| --- | --- | --- | --- |
| `DESIGN.md` | Full build manual, recipes, principles, states, tokens, drift boundaries, reconstruction checks | First retrieval target; stable headings and explicit routing to support files | Prevents under-context generation and makes the package usable alone |
| `SKILL.md` | How to invoke and navigate the language | Direct router: read `DESIGN.md` first, then only relevant support files | Keeps slash-invoked work source-free and bounded |
| Foundation files | Colour, type, space, motion, surface, imagery, voice, brand rules | Named operational rules, thresholds, anti-patterns, and references to token/pattern families | Separates expressive laws from implementation details |
| Token files | Layer ownership, reference maps, modes, platform transforms, drift checks | Deterministic token paths, values, types, references, precedence, and generation contract | Prevents raw-value sprawl and platform divergence |
| Component files | Purpose, anatomy, variants, states, behavior, content, accessibility, API | Stable component/state names and required semantic/component tokens | Gives design, code, and generation one truth |
| Pattern files | When to choose a functional, behavioral, perceptual, domain, or platform pattern | Canonical Taxonomy, parent/related/conflicting patterns, selection logic | Prevents duplicate components and mood-only choices |
| Accessibility files | Numeric obligations, test cases, alternative behavior | Thresholds and gates attached to modes/components, not a final appendix | Makes access part of construction |
| Application rules | Channel/use-case intensity, crop and adaptation rules | Decision table from use case to foundations/components/patterns | Stops full atmospheric treatment from spreading everywhere |
| Prompt pack | Parameterized positive facts, negative constraints, variants, review failures | Structured slots, required invariants, banned terms, output checks | Produces related assets without creator imitation or scene copying |
| Context pack | Minimum retrieval set for common tasks | Intent-to-file routing and compact invariants | Reduces context load without omitting critical boundaries |
| External extraction metadata | Traceability, validation, gaps, readiness, and reconstruction proof | Not packaged with the generated skill; requested only for audit or review | Keeps extraction evidence separate from design-use guidance |
| External provenance metadata | Asset control, permissions, caveats, open questions, and delivery status | Restricted review context; never fed into production prompts by default | Prevents accidental asset reuse and false provenance |
| `agents/openai.yaml` | Display metadata and default invocation | Machine registration that points users toward the generated skill | Ensures package-level discoverability |

## Truth Classes

- **Operational truth:** what to do now—tokens, recipes, states, component behavior, prompts, tests. Lives in design-use files.
- **Normative truth:** what must not drift—accessibility obligations, layer architecture, identity invariants, review gates. Lives in `DESIGN.md` and governed support files.
- **Historical/evidentiary truth:** why a rule was extracted, traceability, contradiction, rights, and uncertainty. Lives in the external extraction metadata archive.
- **Proposed truth:** an inferred extension awaiting real-product validation. It remains explicitly bounded in operational files and is tracked as a gap/readiness item in external extraction metadata.

Do not mix evidence labels, source IDs, archive paths, rights status, or review routing into source-free design-use documentation.

## Required Human Guidance Sections

Every component, pattern, or application entry includes:

1. Purpose and user/maker problem.
2. When to use and when not to use.
3. Anatomy and ownership boundary.
4. Purpose-bearing variants.
5. Complete States and transitions.
6. Content, naming, and localization.
7. Accessibility, Keyboard, Focus, motion, and Recovery.
8. Token dependencies and override boundary.
9. Code/API contract or implementation equivalence.
10. Examples, anti-patterns, and related patterns.
11. Platform/domain differences.
12. Owner, last reviewed, and maturity when a governance context exists.

## Required Machine Guidance

Machine-consumable records should expose:

- canonical ID and artifact type;
- purpose/intent and prohibited uses;
- parent, related, conflicting, and deprecated IDs;
- required token/component/pattern IDs;
- supported variants and States;
- mode/platform transforms;
- accessibility thresholds and non-colour alternatives;
- content schema and API fields;
- examples and failure checks;
- version, deprecation, review date, and owner when known.

Use stable dot paths and canonical pattern names. Free-form prose augments but does not replace typed fields.

## Retrieval Routing

| Task | Load first | Then load | Avoid unless auditing |
| --- | --- | --- | --- |
| Create a new visual asset | `DESIGN.md` | Imagery, palette, surface, spatial grammar, application rules, prompt pack | Source inventory and proof rationale |
| Build a product screen | `DESIGN.md` | Relevant components, semantic/component/mode/platform tokens, accessibility | Source files |
| Add a component | `DESIGN.md` | Components contract, functional/behavioral patterns, token architecture, accessibility | Unrelated applications |
| Review identity drift | `DESIGN.md` | Visual DNA, design principles, perceptual patterns, token drift, validation | Source pixels unless an evidence audit is authorized |
| Audit provenance/readiness | External extraction metadata archive | Inventory, rights/provenance, validation, and reconstruction records | Ordinary generated prompts |
| Run a slash invocation | `SKILL.md` | `DESIGN.md`, then routed support files | Entire package at once |

## Rationale Standard

A useful Rationale states:

- the user/perceptual problem;
- the mechanism the rule controls;
- the failure prevented;
- the alternative rejected and why;
- the conditions that would justify changing the rule.

Avoid aesthetic preference, invented strategy, attribution, or “because it feels on-brand.”

## Freshness And Ownership

- Every governed record may include `status: draft | candidate | stable | deprecated`, owner, last-reviewed date, next-review trigger, and change note.
- Unknown ownership remains `unassigned`; do not invent a team or approver.
- Documentation is stale when referenced token/component IDs fail, mode/platform behavior differs, examples no longer compile/render, or a review date/trigger is exceeded.
- CI checks links, token paths, required sections, placeholders, and generated-artifact manifests. Human review covers perception, culture, content, and domain safety.
- Deprecations include replacement, migration, and removal boundary.

## Change Contract

1. Change the highest correct layer.
2. Update dependent operational documentation.
3. Regenerate machine artifacts and manifests.
4. Run accessibility, mode, platform, and reconstruction checks.
5. Record decision/Rationale and unresolved risk in the external extraction metadata.
6. Never patch generated output or one application example as the source of truth.

## Anti-Patterns

- A glossy style guide with no states, APIs, thresholds, or “when not to use.”
- Loading the source evidence into every generation request.
- Machine summaries that omit accessibility, cultural risk, Recovery, or forbidden behavior.
- Documentation drift hidden by copied snippets, broken token paths, or locally patched components.
- Invented owner, strategy, provenance, or historical explanation.
- One giant context file when a routed minimal packet can preserve the same contract.
