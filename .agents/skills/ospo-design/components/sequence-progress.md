# Sequence And Progress

Output path: `components/sequence-progress.md`

## Sequences Covered

- Ordered Steps, wizards, guided tasks, onboarding, setup, review, and submission.
- Determinate and indeterminate Progress, timers, background work, and Completion states.
- Save, pause, cancel, resume, retry, back, skip, branch, and exit behavior.

## User Or Maker Problem

This family helps people understand what has happened, what is happening, what remains, and whether they can safely pause or leave. It translates the visual language’s route and procession cues into explicit sequence structure without making a glowing path or animation the only progress indicator.

## Anatomy And Boundaries

| Component or module | Anatomy | Boundary | Related component |
| --- | --- | --- | --- |
| Step indicator | Sequence label, step names or count, current/completed/upcoming/error states | Reports structure and location; does not own step content or navigation | Wizard controller |
| Wizard controller | Step content region, Back/Next/Save/Exit actions, validation, persistence | Owns progression, branching, and data preservation | Form, Button |
| Determinate progress | Task label, track, value, text/percentage, optional cancel | Represents measurable work, not arbitrary waiting theatre | Status message |
| Indeterminate progress | Task label, compact nonpositional indicator, elapsed/delay handling | Represents work with unknown measure; not a substitute for timeout/recovery | Loading pattern |
| Timer | Purpose label, remaining time, warning, pause/extend/expiry behavior | Communicates a real limit; never decorative countdown | Warning/dialog |
| Checkpoint/resume | Saved position, timestamp/context, resume/restart choices | Owns restoration state, not authentication or storage policy | Completion/status |
| Completion panel | Result summary, affected object, next action, optional receipt/details | Confirms a terminal outcome; does not erase history or recovery | Status, actions |

## Variants

| Variant | Purpose | Visual difference | Behavioral difference |
| --- | --- | --- | --- |
| Linear named steps | Stable, understandable workflow | Labelled ordered list with clear current marker | Back/Next moves through known sequence |
| Compact count | Narrow screen or many simple steps | “Step 2 of 5” plus current title | Same sequence semantics; full list available elsewhere if needed |
| Branching phases | Conditional journey | Named phases without misleading fixed total | Next step depends on choices; summary explains branch |
| Determinate task | Bytes/items/known stages measurable | Stable track and numeric value | Updates at meaningful intervals; exposes current value |
| Indeterminate task | Unknown duration | Small labelled indicator, no fake percentage | Escalates to cancel/retry/background options |
| Background task | User can leave safely | Persistent status entry and later Completion | Continues across navigation; notifies according to permission |
| Timed task | Real expiry or security limit | Remaining time plus warning | Supports extension/pause where allowed |

## States

| State | Visual behavior | Interaction behavior | Content behavior |
| --- | --- | --- | --- |
| Upcoming | Quiet label/marker | Not interactive unless direct navigation is allowed | Step name remains readable |
| Current | Strong marker, surface, and semantic state | Owns focus/content region | Current title and requirements visible |
| Complete | Check/label, not colour alone | May be revisitable when safe | “Complete” or result summary available |
| Optional/skipped | Distinct text/state | Skip is reversible where possible | Name as optional/skipped, not disabled |
| Blocked | Clear reason and prerequisite | Cannot advance; repair path available | Explain what remains |
| Loading | Stable current context plus labelled progress | Prevent duplicate commit; allow safe cancel/background | Name the task and preservation |
| Paused/offline | Progress retained, stable pause/offline state | Resume/retry/exit available | Explain what is saved |
| Error | Error marker plus local/global message | Preserve progress and data; retry or alternate path | Name failed scope and recovery |
| Complete | Stable result; loading removed | Next action available; no forced redirect | Confirm outcome and affected object |
| Expired | Clear terminal/warning state | Restart, extend, or contact path as policy permits | Explain consequence and preserved data |

## Sequence Behavior

- Show Steps only when they improve orientation. A two-action dialog does not need a stepper.
- Name steps by user goal or content, not internal processing stage.
- Validate the current step before advancing, but preserve entered values and allow Back unless risk or policy makes it unsafe.
- If future steps depend on current answers, use named phases or update the total transparently; do not show a false fixed count.
- Optional steps are labelled optional before entry. Skip does not imply failure.
- Save checkpoints after meaningful commits and before long network work. State whether progress is local, synced, pending, or unsaved.
- On return, summarize restored context and let the user resume or restart without losing the saved version accidentally.
- Completion is a stable state, not an automatic redirect. Name what completed, provide a receipt/details when relevant, and offer the next useful action.

## Progress And Timing Rules

- Use determinate Progress when the system can measure bytes, items, or stages. Do not invent a smooth percentage from elapsed time alone.
- Update values at a readable cadence; avoid high-frequency announcements and visual jitter.
- For work under roughly 100ms, show direct result. Around 1s, show a labelled loading state. For longer work, provide progress or elapsed context, cancel/background behavior, and failure recovery.
- Indeterminate motion is compact, controlled, and absent or replaced in reduced-motion mode. Text continues to identify the task.
- A Timer explains why time exists, what happens at zero, when warnings occur, and whether the user can pause, extend, or preserve work.
- Never use fake scarcity, countdown anxiety, or a decorative animated route.

## Content And Naming Rules

- Use “Step 2 of 5: Review details,” not a bare “2/5.”
- Progress labels name the operation: “Uploading 3 files… 42%.”
- Completion copy names the result: “Report submitted,” not “You’re all set!” alone.
- Error copy distinguishes a failed step from a failed overall sequence.
- “Save and exit,” “Cancel upload,” “Resume setup,” and “Start again” state the consequence.
- Keep labels localizable, allow wrap, and avoid journey/frontier metaphors such as trail, quest, expedition, or crossing unless they are literal domain terms.

## Token Dependencies

| Part | Required token | Override boundary |
| --- | --- | --- |
| Progress track | `component.progress.track` | Stable, nonpulsing |
| Progress value | `component.progress.value` | Mode may replace; must remain non-colour-redundant |
| Progress label | `component.progress.label` | Always identifies the task |
| Current step surface | `component.nav.surface.selected` or `component.choice.selected.background` | Current/selected semantics only |
| Current marker | `component.choice.selected.mark` | Pair with text/programmatic state |
| Completion accent | `component.status.success.accent` | Check and copy required |
| Warning/error accents | `component.status.warning.accent`, `component.status.error.accent` | Consequence/recovery required |
| Navigation actions | `component.button.*` | Follow action hierarchy |
| Transition duration | `semantic.motion.reveal.duration` | Reduced-motion branch required |

## Accessibility And Localization

- Expose current step, total when truthful, completed/skipped/error state, progress value/min/max, and busy status programmatically.
- Do not announce every percentage change. Announce meaningful milestones or user-requested detail.
- Focus moves to the new step heading after progression when context changes; Back restores a meaningful location.
- Keyboard, switch, voice, and touch access cover every step action. The visual route is decorative to assistive technology.
- Ensure progress does not depend on warm/cool colour, animation, spatial position, or sound.
- Support 200% zoom, large text, 35%+ expansion, RTL, local time/date/number formatting, and pluralization.
- Reduced motion uses static current/completed markers, immediate changes or short fades, and explicit labels.
- Time limits meet applicable accessibility requirements for warning, adjustment, extension, and essential exceptions.

## Code And API Contract

```text
Sequence {
  id: stable workflow id
  steps: ordered list of Step records (id, label, optional flag, status)
  currentStepId: required
  totalKnown: boolean
  canBack: boolean
  canExit: boolean
  saveState: unsaved | saving | saved | failed
  onNext / onBack / onSkip / onSaveExit / onResume / onRestart
}

Progress {
  label: required
  kind: determinate | indeterminate | background
  value?: number
  min?: number
  max?: number
  state: running | paused | offline | failed | complete
  cancellable?: boolean
  retryable?: boolean
}
```

- A determinate Progress instance requires valid numeric bounds and current value.
- A branching sequence must not expose a fixed total unless it is accurate for the current branch.
- Unsupported: arbitrary luminous route, fake percentage, hidden label, auto-advance after reading, and uninterruptible editorial animation.

## Examples And Anti-Patterns

- **Do:** preserve all form data when upload fails at step 4, show the file-level error, and offer retry.
- **Do:** show a static “3 of 8 files uploaded” state in reduced motion.
- **Do:** let a person resume a saved setup with a clear timestamp and restart alternative.
- **Avoid:** making completion a confetti event or redirecting before the result can be reviewed.
- **Avoid:** an animated orange path with no text status, a spinner with no task name, or a countdown with no expiry explanation.
- **Avoid:** disabling Back to simplify code while silently discarding earlier choices.

## Related Patterns

- Forms and validation.
- Actions and triggers.
- Navigation and wayfinding.
- Feedback, status, loading, undo, and recovery.
- Behavioral state and reduced-motion contracts.
