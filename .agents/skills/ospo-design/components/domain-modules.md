# Domain Modules

Output path: `components/domain-modules.md`

## Domain Modules Covered

- E-commerce, education, finance, cooking, service journeys, and omnichannel continuity.
- Product/checkout, learning/discussion, market/transaction, recipe/timer, case/appointment, and handoff/receipt modules.
- Domain vocabulary, data accuracy, trust, regulation, safety, and platform Constraint handling.

## User Or Maker Problem

This family shows how to extend the visual language into recurring domain-specific work without flattening every product into generic Cards or allowing atmosphere to obscure price, progress, risk, measurement, safety, or service status. A domain Module is legitimate only when its purpose and behavior recur.

## Domain Equivalence Map

| Domain | Module | Core user purpose | Constraint | Expression boundary |
| --- | --- | --- | --- | --- |
| E-commerce | Product tile/detail | Inspect and choose a real product | Accurate colour, condition, price, availability, shipping, returns | Identity treatment may frame editorial media; inspection images remain accurate and clean |
| E-commerce | Cart/checkout | Review commitment and complete purchase | Totals, fees, taxes, delivery, consent, payment, undo/correction | Use native/trusted form patterns; no cinematic delay or hidden cost |
| Education | Learning activity | Understand, practice, submit, receive feedback | Clear objectives, accessible materials, attempt state, save/resume | A “passage” motif may introduce a module; instructions and assessment remain literal |
| Education | Discussion | Read, reply, cite, moderate | Identity, authorship, safety, thread order, reporting | Do not represent real people as anonymous silhouettes |
| Finance | Quote/market field | Inspect value, change, timestamp, source | Precision, stale state, units, market time, risk | Brand colours do not replace conventional gain/loss labels, signs, arrows, and values |
| Finance | Transaction/portfolio | Review holdings or commit money movement | Confirmation, fraud/security, pending/failed state, audit receipt | Maximum clarity; atmosphere confined to chapter/marketing surfaces |
| Cooking | Recipe/ingredient scaler | Prepare food with correct amounts and sequence | Units, allergens, substitutions, serving scale, provenance | Editorial dish image may be atmospheric only if inspection and doneness remain clear elsewhere |
| Cooking | Step/timer | Execute a time/temperature-sensitive action | Hands-free use, timer alerts, safety, pause/resume | No fake fire/glow feedback; exact values stay crisp |
| Service journey | Appointment/case tracker | Understand current status and next action | Eligibility, documents, deadlines, privacy, escalation | A route motif may supplement explicit labelled stages |
| Service journey | Support handoff | Transfer context without repetition or data loss | Consent, transcript/state, ownership, expected response | Stable receipt and recovery outrank mood |
| Omnichannel | Handoff/receipt | Continue across device, location, or channel | Identity, expiry, offline state, deep link, QR/code fallback | Preserve semantics and state; channel chrome may adapt natively |

## Anatomy And Boundaries

| Component or module | Anatomy | Boundary | Related component |
| --- | --- | --- | --- |
| Product summary | Accurate media, name, variant, price, stock, delivery context, primary action | Summarizes one purchasable item; does not hide material terms | Card, Button |
| Checkout summary | Items, quantities, line totals, fees/tax, delivery, payment state, edit links, final total | Owns review and commitment; does not market additional ambiguity | Form, confirmation dialog |
| Learning activity | Objective, content, instructions, response area, save/submit, feedback, progress | Owns one learning task; does not impersonate assessment if ungraded | Form, progress |
| Discussion entry | Author identity, timestamp, content, reply/context, moderation actions | Owns one contribution and its provenance | List, status |
| Market field | Instrument label, value, change with sign/unit, timestamp, source/stale state | Owns one financial datum; not a decorative ticker | Table, chart |
| Transaction review | Source/destination, amount/currency, fees/rate, timing, risk, confirmation, receipt | Owns a consequential money action | Dialog, status |
| Recipe step | Step number/name, instruction, quantities, timer/temperature, safety cue, completion | Owns one preparation action | Sequence, timer |
| Service stage | Stage name, status, completion evidence, next requirement, due date, contact/escalation | Owns one case phase; does not imply completion by position alone | Progress, status |
| Channel handoff | Source channel, destination, transferred state, expiry, secure token/deep link, fallback | Owns continuity; does not expose secrets in display copy | Receipt, QR/deep link |

## Variants

| Variant | Purpose | Visual difference | Behavioral difference |
| --- | --- | --- | --- |
| Editorial entry | Introduce a domain chapter or story | Full identity scene with clean support copy | Navigates to functional content |
| Functional summary | Scan and compare domain objects | Clean panel/list/Table with compact accent | Sorting, filtering, selection, exact values |
| Guided task | Complete ordered work | Explicit Steps and actions, optional quiet route cue | Validation, save, resume, error recovery |
| High-stakes review | Confirm financial, health/safety-adjacent, legal, or irreversible action | Maximum contrast, zero texture, explicit totals/consequences | Stronger confirmation and receipt |
| Omnichannel handoff | Continue elsewhere | Compact receipt/status with native code/link | Expiry, security, resume, fallback |

## States

| State | Visual behavior | Interaction behavior | Content behavior |
| --- | --- | --- | --- |
| Default | Clean domain hierarchy and exact values | Purpose-appropriate actions | Labels, units, timestamp/provenance where needed |
| Hover/focus | Ordinary platform feedback | Keyboard/touch accessible | No hidden essential terms |
| Selected/active | Marker plus semantic state | Selection or current stage persists | Count/status updates |
| Disabled/ineligible | Readable condition and reason | No invalid commit | Explain prerequisite and alternate route |
| Loading/pending | Existing data retained, labelled progress/pending status | Cancel/background/resume by contract | Distinguish pending from complete |
| Stale/offline | Timestamp and stale/offline marker | Refresh, continue offline, or block honestly | State what may be outdated |
| Error | Affected value/module identified | Preserve data and offer Recovery | Problem, scope, retry/alternate/escalation |
| Complete/confirmed | Stable result and receipt | Next action available | Confirmation ID, terms, timestamp, or evidence as domain requires |

## Content And Naming Rules

- Use the domain’s established nouns and units; do not rename ordinary concepts to fit the visual metaphor.
- Prices, rates, quantities, dates, temperatures, serving sizes, deadlines, and totals include units and locale.
- Show source, timestamp, stale/pending state, and uncertainty wherever decisions depend on currency.
- Consequential actions name object, amount, scope, and reversibility.
- Avoid “trail,” “quest,” “camp,” “outlaw,” “frontier,” “tribe,” “shoot,” or “journey” unless literally accurate and culturally reviewed.
- Preserve authorship and identity in education/discussion/service contexts; anonymous silhouettes are not identity avatars.
- Do not imply regulatory, safety, historical, cultural, medical, or financial authority through solemn visuals.

## Token Dependencies

| Part | Required token | Override boundary |
| --- | --- | --- |
| Functional surface | `component.panel.background`, `semantic.surface.critical` | High-stakes modules use zero texture |
| Primary/secondary copy | `semantic.text.primary`, `semantic.text.secondary` | Exact-value contrast validated |
| Domain action | `component.button.*` | Risk hierarchy applies |
| Form/selection | `component.field.*`, `component.choice.*` | Native semantics retained |
| Status/progress | `component.status.*`, `component.progress.*` | Text/icon/recovery required |
| Data display | Domain data tokens plus content/Table contract | Brand palette is not a data palette |
| Editorial image | `component.scene.*`, `component.scene-support.*` | Accurate inspection alternative required when needed |
| Focus | `semantic.focus.ring` | Native equivalent accepted |

## Accessibility And Localization

- Use semantic domain structures: product names/prices, form labels, assessment instructions, Table headers, units, timers, status, and receipts.
- Provide keyboard, screen-reader, speech, switch, touch, zoom, large-text, high-contrast, reduced-motion, and offline/retry behavior.
- Localize currency, number, date/time, address, name, temperature, mass/volume, measurement systems, pluralization, and legal copy.
- Charts/data use direct labels, signs, units, patterns/shapes, and nonvisual alternatives; colour never carries gain/loss or severity alone.
- Timers have visual, auditory, and haptic equivalents with user controls; critical safety information is persistent.
- Product/food imagery has purpose-based alt text and accurate alternatives. Do not texture diagrams, ingredients, labels, or safety cues.
- Domain teams must review applicable regulation, consent, record retention, privacy, and safety; this visual-language package is not a compliance substitute.

## Code And API Contract

```text
DomainModule {
  domain: explicit product domain
  purpose: recurring user goal
  title: required localized string
  data: typed domain record with units and provenance
  state: default | pending | stale | offline | failed | complete
  actions: ordered purpose-bearing controls
  recovery?: retry, alternate, undo, or escalation contract
  media?: licensed asset with accuracy and alt metadata
  timestamp?: locale-aware instant plus timezone
  constraints: domain validation and policy hooks
}
```

- Each concrete module defines a typed record rather than a generic bag of fields.
- High-stakes modules require review/confirmation/receipt states and idempotent retry behavior where duplicate commit is possible.
- Unsupported: arbitrary domain string with generic Card rendering, raw status colours, unlabeled units, visual-only progress, atmosphere over exact data, and a generic “onSubmit” without state/recovery.

## Examples And Anti-Patterns

- **Do:** frame an editorial product story with an identity scene, then provide neutral accurate product views and complete terms.
- **Do:** show a service route as a decorative line beside labelled stages, due dates, and next requirements.
- **Do:** present market movement with signed values, units, timestamp, direct labels, and accessible Table.
- **Avoid:** using orange for loss and cyan for gain without text/sign/icon, or a dramatic glow to imply financial urgency.
- **Avoid:** styling a cooking timer like a fire, obscuring doneness imagery, or hiding allergens in poetic copy.
- **Avoid:** making checkout, assessment, transaction, or consent wait for cinematic animation.

## Related Patterns

- Actions, forms, navigation, sequence, feedback, content, and data display.
- Domain and platform equivalence contracts.
- Accessibility, localization, cultural review, and rights.
- Imagery art direction and brand-expression boundaries.
