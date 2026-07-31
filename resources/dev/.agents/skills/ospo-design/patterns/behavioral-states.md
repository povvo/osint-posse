# Behavioral States

Output path: `patterns/behavioral-states.md`

## State Inventory

| State | Trigger | Visual response | Interaction contract | Recovery |
| --- | --- | --- | --- | --- |
| Default | Component becomes available in stable context | Clean surface, readable content, visible affordance | Native semantics and ordinary input methods available | Return here after transient interaction when no persistent state changed |
| Hover | Fine pointer enters target | One value, boundary, or underline change; no glow/layout shift | Supplemental only; never reveals exclusive content | Pointer exit restores prior persistent state |
| Focus | Keyboard, switch, voice, or programmatic navigation reaches target | Crisp 2px minimum Focus indicator with offset, independent of hover | Enter/Space/arrow behavior follows component/platform contract; focus order is logical | Focus remains visible; on close/removal, moves to meaningful successor or invoking control |
| Active/pressed | Pointer/key contact begins or action commits | Brief value change or `1–2px` compression | Commits once; prevents accidental duplicate submission | Release returns to default, Selected, Loading, or result state |
| Selected | User chooses a persistent option/current destination | Marker/check plus surface, weight, shape, and programmatic state | Can be toggled only when control semantics permit; current navigation may be nonreselecting | Deselection restores default; single-select moves selection atomically |
| Disabled | Prerequisite, permission, policy, or state makes action unavailable | Lower prominence but readable label; no hover | Native disabled behavior; not interactive | Explain prerequisite nearby or provide alternate path; re-enable without losing context |
| Read-only | Data may be inspected but not edited | Ordinary readable value with clear noneditable treatment | Selection/copy and navigation remain where appropriate | Provide edit route or reason if editing is expected |
| Loading | User/system begins work that is not immediate | Stable context plus labelled progress; no indefinite decorative motion | Prevent duplicate commit; permit safe cancel/background | Complete, fail with Retry, pause/offline, or restore previous state |
| Paused/offline | Work cannot continue or is intentionally paused | Stable pause/offline icon, retained progress/value | Resume, retry, cancel, or continue offline by capability | Preserve state and disclose what is local, pending, or stale |
| Success/complete | Goal or operation finishes | Stable completion mark; loading removed | Result is inspectable; next useful action available | Undo when reversible; receipt/history when consequential |
| Warning | Risk, expiry, degraded state, or consequence is detected | Warning icon, boundary, explicit message; no colour-only cue | Acknowledge, repair, continue, or cancel according to risk | Remove when condition clears; preserve choice and context |
| Error | Validation, network, system, or permission failure occurs | Error icon/boundary/message adjacent to affected scope | Preserve input/state; announce appropriately; do not force unrelated focus | Specific correction, Retry, alternate path, undo, or escalation |
| Expanded/collapsed | Disclosure/menu/accordion trigger activates | Trigger state/icon and controlled region update along one axis or instantly | `expanded` and ownership semantics stay synchronized; Escape/outside behavior depends on component | Close returns Focus to trigger; reduced motion uses cut/short fade |
| Empty | Valid query/collection contains no items | Clean explanatory state, optional small illustration, direct next action | Distinguishes initial empty from filtered-zero | Add item, clear filters, or navigate to source |
| Stale | Displayed data may no longer be current | Timestamp/stale marker without erasing readable previous data | Refresh available; decisions may be blocked if currency is essential | Successful refresh clears; failure becomes explicit offline/error |

## State Priority

When multiple conditions coexist, communicate the state that most affects safe action:

1. Critical error or blocking permission.
2. Offline/paused/stale when currency matters.
3. Loading/pending.
4. Disabled/read-only.
5. Selected/expanded.
6. Focus.
7. Hover/pressed.
8. Default.

Focus remains visually visible even on selected, invalid, or warning states. A state priority never removes the lower-level semantic attributes needed by assistive technology.

## Interaction Contracts

- **Drag and drop:** provide a keyboard/button alternative, visible grab/target state, instructions, cancel, original-order preservation, and undo. Drag is never the only uploader or reordering path.
- **Reveal and hide:** trigger owns a named region, state is programmatically exposed, motion follows the governing axis under `300ms`, reduced motion uses a cut/short fade, and closing restores focus appropriately.
- **Confirmation:** strength matches risk. Name the action, object, scope, consequence, and reversibility. Routine reversible work uses direct action plus undo.
- **Undo:** make reversible destructive outcomes stable and accessible for a reasonable domain-specific interval; retain a durable alternate route when a transient snackbar is insufficient.
- **Retry:** repeat only the failed, idempotent operation when possible. Preserve inputs and explain duplicate-risk verification when idempotency is uncertain.
- **Resume:** restore checkpoint, state, timestamp, and context; distinguish local, synced, pending, and stale data; offer restart without deleting the saved version accidentally.
- **Responsive behavior:** visual layout may reflow, but semantic state, focus order, selection, expanded ownership, error association, scroll position, and Recovery remain invariant.
- **Interruption:** new input retargets/reverses in-flight motion rather than queuing it. Essential actions respond within 100ms even when a scenic transition is running.
- **Timeout:** warn before expiry, expose remaining time and consequence, allow extension when required, and preserve work where possible.

## Transition Matrix

| From | Allowed next states | Forbidden shortcut |
| --- | --- | --- |
| Default | Focus, active, selected, expanded, loading, disabled | Default directly to success without a causal action/system event |
| Active | Loading, success, error, selected, default | Multiple simultaneous commits |
| Loading | Success, error, paused/offline, cancelled/default | Infinite loading with no escalation |
| Error | Focus/correction, loading via retry, default after repair | Dismissed error presented as success |
| Disabled | Default when prerequisite clears | Hover/pressed while programmatically disabled |
| Expanded | Collapsed, selected action, loading | Removing trigger before focus can return |
| Stale | Loading via refresh, default on successful refresh, error | Silently treating stale data as current |

## Feedback Timing

- Local acknowledgement begins within `100ms`.
- Ordinary state reveal uses `180–300ms`; exits are faster.
- At roughly `1s` of waiting, expose a labelled Loading state.
- Longer waits add progress/elapsed context, cancel/background behavior, and failure Recovery.
- Status announcements are throttled; do not announce every progress tick, hover, or decorative change.

## Accessibility Contract

- Every visual state has a semantic equivalent and, where meaning matters, a text/icon/shape cue.
- Focus is never inferred from hover, glow, colour, or animation.
- Selected, pressed, expanded, checked/mixed, disabled, invalid, busy, current, progress, and live status use native/ARIA-equivalent semantics.
- Programmatic focus movement is limited to genuine context changes, validation summaries, or blocking overlays and is announced through meaningful headings/labels.
- Reduced motion preserves causality through stable before/after composition and explicit state cues.
- High contrast removes texture/bloom and uses system colours/solid boundaries without losing state distinctions.

## Anti-Patterns

- Colour-only states, glow-only Focus, hover-only information, or animation-only progress.
- A disabled control used to conceal requirements, an error that discards input, or a spinner with no task name.
- Treating selected, focused, active, and current as interchangeable.
- Queued animations, uninterruptible transitions, fake progress, silent background failure, or auto-dismissed critical Recovery.
- Responsive layouts that reset selection, focus, form values, scroll, or expanded state.
