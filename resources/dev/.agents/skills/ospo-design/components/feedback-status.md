# Feedback And Status

Output path: `components/feedback-status.md`

## Feedback Covered

- Alerts, inline messages, banners, toasts, snackbars, dialogs, prompts, and popovers.
- Loading, empty, error, success, warning, information, offline, paused, and stale states.
- Recovery, retry, undo, escalation, persistence, and accessible announcement.

## User Or Maker Problem

This family lets people know what the system received, what changed, what is still happening, what failed, and how to recover. Makers receive a scope-and-risk model that prevents every event from becoming a toast or modal and keeps the language’s visual stillness from turning into silent or ambiguous behavior.

## Anatomy And Boundaries

| Component or module | Anatomy | Boundary | Related component |
| --- | --- | --- | --- |
| Inline message | Status icon, heading/message, affected scope, optional action | Local to a field, component, or task; persists while relevant | Form field, panel |
| Banner | Region-level icon, heading, explanation, action/dismiss | Cross-page or system state; not for one field | Navigation shell |
| Toast/snackbar | Short message, optional one action, timer/persistence policy | Nonblocking and redundant with durable state; not for critical errors | Undo, status history |
| Alert | Explicit urgency semantics, message, optional action | Immediate announcement only when interruption is justified | Banner, dialog |
| Dialog/modal | Title, description, content, actions, close policy, focus boundary | Blocking decision or consequential confirmation; not routine notification | Button, form |
| Popover | Trigger relationship, contextual content, optional actions, dismiss behavior | Supplemental context near a trigger; not essential information with no alternate path | Tooltip, menu |
| Progress/loading | Task label, determinate/indeterminate indicator, state, cancel/retry | Communicates real work; not decorative motion | Sequence/progress |
| Empty state | Explanation, reason/context, primary next action, optional illustration | Absence of content; not an error unless expected content failed to load | List, search |
| Recovery panel | Failure summary, preserved state, retry/alternate/support path | Owns repair after a failed operation | Form, upload, background task |

## Variants

| Variant | Purpose | Visual difference | Behavioral difference |
| --- | --- | --- | --- |
| Information | Neutral context or change | Mineral accent plus information icon/label | Usually polite status announcement |
| Success | Completed goal | Stable check and success label; restrained accent | Confirms durable result; no compulsory celebration |
| Warning | Risk or degraded state before failure | Amber/strong boundary plus warning icon | May require acknowledgement or choice |
| Error | Failed action or invalid state | Strong error accent, icon, explicit recovery | Persists until resolved/dismissed deliberately |
| Offline/paused | Work cannot continue now | Stable paused/offline symbol and retained progress | Resume/retry/background behavior |
| Empty | Valid absence | Sparse clean panel, optional small illustration | Offers direct next action |
| Blocking | Consequential decision or required action | Opaque dialog, clear hierarchy, no image texture | Focus is contained; explicit actions required |

Variants express meaning and scope. Colour-named, glowing, “dramatic,” and mood-only variants are unsupported.

## States

| State | Visual behavior | Interaction behavior | Content behavior |
| --- | --- | --- | --- |
| Default/informational | Stable message and icon | Readable; dismiss only if no longer needed | State fact and relevance |
| Hover/focus | Action receives ordinary focus/hover; message itself does not glow | Keyboard actions available | Labels unchanged |
| Active/pressed | Feedback action responds immediately | Retry/undo/dismiss commits once | Action name remains specific |
| Dismissed | Removed without layout surprise; durable state remains elsewhere when needed | Focus returns logically | Do not erase unresolved failure |
| Loading | Labelled progress on clean surface | Cancel/background/retry by task contract | Name work and preservation |
| Success | Stable completion, loading removed | Next action available | Name result and object |
| Warning | Persistent until risk passes or user acknowledges where required | Consequence/action available | State risk before action |
| Error | Persistent local or regional message | Preserve state; retry/alternate/support | Problem, scope, recovery |
| Offline/paused | Stable retained context | Resume or retry when possible | Saved/pending status explicit |

## Scope, Urgency, And Persistence

- Use inline feedback for one field or component, a banner for section/system state, a toast for noncritical transient confirmation, and a dialog only for blocking or consequential decisions.
- `status`/polite announcement is the default for progress and completion. Reserve urgent alert behavior for events requiring immediate attention.
- A toast must not be the only record of a consequential result, error, receipt, or undo state. Keep durable state in the affected view/history.
- Dismissal does not resolve the underlying problem. Do not let a user hide an error and then appear complete.
- Match persistence to reading and action needs; pause transient timers on hover/focus where relevant and support platform accessibility settings.
- One action produces at most one immediate control response, one state-level message, and one optional nonvisual cue.

## Loading And Latency

- Under roughly 100ms, show the result directly. Near 1s, show a labelled local Loading state. For longer work, add progress or elapsed context, cancel/background behavior, and failure recovery.
- Use determinate progress when measurable; never manufacture a percentage.
- Keep the previous stable context visible while refreshing unless showing it would be misleading. Label stale or updating data.
- Skeletons may preserve layout for content-heavy views, but they must not shimmer continuously in reduced motion or imply data that may not exist.
- A spinner or atmospheric edge reveal is never sufficient without a task label.
- Distinguish loading, queued, paused, offline, failed, cancelled, and complete.

## Recovery And Escalation

- Preserve user input, selected files, filters, position, and completed substeps where safe.
- State the problem in plain language, name the affected scope, and provide a specific retry or alternate path.
- Use undo for reversible actions and confirmation for irreversible or high-risk actions; risk determines strength.
- If retry may duplicate a transaction, explain verification and idempotency rather than encouraging blind repetition.
- Escalation states what support needs, what data will be shared, expected response, and any safe self-service alternative.
- Unknown outcomes are described honestly: “We couldn’t confirm whether the payment completed. Check transactions before retrying.”

## Content And Naming Rules

- Use headings only when they improve scanning: “Upload failed,” “Connection lost,” “Report submitted.”
- Messages follow fact → impact/scope → next action.
- Avoid “Oops,” “Something went wrong,” “Success!”, “Warning!” without detail, blame, humour, or poetic mystery.
- Action labels name repair: “Retry upload,” “Review card details,” “Restore draft,” “Contact support.”
- Empty states explain why the area is empty and how to add/find content; do not anthropomorphize emptiness as loneliness.
- Allow wrapping, localization, pluralization, locale-aware numbers/dates, and sufficiently long reading time.

## Token Dependencies

| Part | Required token | Override boundary |
| --- | --- | --- |
| Status surface | `component.status.background` | Clean functional surface |
| Info accent | `component.status.info.accent` | Info meaning only |
| Success accent | `component.status.success.accent` | Check and copy required |
| Warning accent | `component.status.warning.accent` | Consequence required |
| Error accent | `component.status.error.accent` | Recovery required |
| Status copy | `component.status.text` | No opacity-only weakening |
| Progress track/value/label | `component.progress.*` | Determinate when measurable |
| Dialog surface/scrim | `component.dialog.background`, `component.dialog.scrim` | Opaque, modal semantics only |
| Dialog focus | `component.dialog.focus.ring` | Native equivalent accepted |
| Message actions | `component.button.*` | Follow hierarchy/risk contract |

## Accessibility And Localization

- Associate inline errors with their source controls and summarize submission failures when useful.
- Announce status with appropriate live-region/native semantics; do not move focus for routine toasts or completion.
- Move focus into a modal dialog at its meaningful start, contain it while modal, support Escape where safe, and return it to the trigger on close.
- Do not announce every progress increment or auto-dismiss before assistive-technology users can review the message.
- Icon, text, boundary/shape, and programmatic state redundantly encode meaning; colour and sound are supplemental.
- Support keyboard, switch, touch, zoom, large text, high contrast, reduced motion, RTL, and long translations.
- Alert sound/haptic has a simultaneous visual and semantic equivalent and respects device/user settings.
- Popovers and tooltips are reachable by keyboard and pointer, dismissible, hoverable where required, and never the sole location for essential guidance.

## Code And API Contract

```text
FeedbackMessage {
  id: stable message id
  kind: info | success | warning | error | offline | paused
  scope: inline | section | global | transient
  title?: localized string
  message: required localized string
  action?: one named action
  dismissible?: boolean
  announce: polite | assertive | none
  persistent: boolean
}

Dialog {
  id: stable dialog id
  title: required localized string
  description?: localized string
  modal: boolean
  actions: ordered purpose-bearing controls
  initialFocus: meaningful element
  returnFocusTo: trigger id
  closePolicy: explicit rules
}
```

- Progress requires label, kind, state, and numeric bounds when determinate.
- A transient message with an action must pause dismissal during focus/interaction and provide a durable alternate path when consequential.
- Unsupported: arbitrary severity colour, unlabeled spinner, auto-dismissed critical error, focusless modal, decorative alert, and generic `showToast(message)` for all feedback.

## Examples And Anti-Patterns

- **Do:** “Upload failed. Your file is still selected. Retry upload.”
- **Do:** “Report submitted” in the page with a receipt link; a short toast may echo the result.
- **Do:** show “Offline — changes saved on this device” with resume/sync status.
- **Avoid:** a pulsing orange glow as the only error, a cyan check as the only success, or multiple stacked toasts.
- **Avoid:** blocking dialogs for routine confirmations, hidden recovery behind “More,” or silent background failure.
- **Avoid:** atmospheric smoke, grain, and blur on alerts, dialogs, progress text, or focus.

## Related Patterns

- Forms and validation.
- Actions and destructive confirmation.
- Sequence, progress, pause, and completion.
- Behavioral states, interruption, undo, and recovery.
- Accessibility and platform feedback patterns.
