# Interaction Register

Output path: `foundations/interaction-register.md`

## Ambient Atmosphere

- **Persistent background state:** quiet, dark, watchful, and stable. The interface does not call attention to itself while the user observes or decides.
- **Visual equivalent:** one calm absorptive shell, restrained hierarchy, and a single local accent at the point of current relevance. Grain and bloom belong to identity imagery, not the active control layer.
- **Sound, haptic, or environmental implication:** silent by default. Use platform-standard haptics only for direct manipulation, selection, high-confidence completion, or consequential confirmation. Sound is opt-in, functional, captioned or otherwise redundantly signalled, and never atmospheric in task flows.
- **What the interface feels like before interaction:** deliberate and ready, not dormant. Affordances remain visible and labelled even when the wider scene is sparse.
- **Extension boundary:** interaction behavior is a functional translation of the visual language. Clarity, recovery, and platform convention take priority over mystery.

## Percussive Events

| Event type | Feedback character | Visual form | Haptic/sound equivalent |
| --- | --- | --- | --- |
| Hover | Quiet | One value-step surface lift or underline; no glow-only cue | None |
| Keyboard focus | Crisp and unmistakable | Solid 2px minimum indicator with offset and validated contrast; survives high contrast | None |
| Press | Brief and grounded | `1–2px` compression or a fast value change; return immediately | Optional light platform tick on touch |
| Selection | Stable | Persistent marker, check, shape, or boundary plus label/state announcement | Optional selection tick |
| Expand/reveal | Slow-functional | Axis-aligned disclosure under `300ms`; control updates `aria-expanded` or platform equivalent | None |
| Completion | Quietly affirmative | Stable check/icon, explicit completion copy, optional compact mineral highlight | Optional success haptic where conventional |
| Warning | Heavy but nonblocking | Amber boundary/icon plus explicit consequence and action | Optional warning haptic only when timely |
| Error | Direct, not theatrical | Solid high-contrast boundary, icon, message, and recovery action; focus moves only when appropriate | Platform error haptic; no alarm sound by default |
| Destructive confirmation | Deliberate | Clear action name, consequence, and safe alternative; destructive action visually distinct | Medium confirmation haptic after committed action, not before |

## Feedback Density

- **Maximum response per action:** one immediate control response, one state-level confirmation, and one optional nonvisual cue. Do not stack toast, animation, sound, haptic, and modal for a routine event.
- **Minimum response per action:** visible state change within 100ms and an accessible state announcement when the result is not already evident.
- **When feedback is withheld:** decorative hover on touch, ambient reactions to scrolling, repeated confirmation for continuous manipulation, and nonessential scene motion.
- **When feedback must be explicit:** form validation, save state, payment, consent, permission, network delay, destructive action, undo window, retry, resume, authentication, and any action whose result is off-screen.
- **Persistence:** ephemeral feedback remains long enough to read and pauses on hover/focus where relevant. Consequential state is available in the page or history after a toast disappears.

## Silence

- **Expected feedback intentionally removed:** idle animation, hover sound, decorative particle response, repeated celebratory effects, and narration of obvious local movement.
- **Meaning of the absence:** composure and respect for attention, never uncertainty about whether the system received input.
- **Risk of seeming broken:** sparse visuals can hide latency. After `100ms`, show local acknowledgement; around `1s`, show a labelled loading state; after a context-appropriate threshold, offer progress, cancel, retry, or background continuation.
- **Silence boundary:** never suppress validation, error, completion, focus, security, permission, or recovery feedback.

## Trust Construction

- **Progressive disclosure:** reveal secondary context after the primary choice is understood; keep prerequisites, cost, risk, and irreversible consequences visible before commitment.
- **Reliability:** preserve control position, state, data, and focus across transitions. Do not use atmospheric variation to imply random system behavior.
- **Recovery:** retain user input where safe, explain what happened in plain language, provide retry and alternate path, and offer undo for reversible destructive actions.
- **Escalation:** match interruption strength to risk. Inline feedback for local errors, banners for broader degraded state, dialogs only for blocking or consequential decisions.
- **Latency:** distinguish waiting, offline, failed, paused, and completed. A vague shimmer is not a status.

## State Semantics

| State | Interaction meaning | Visual behavior | Copy behavior |
| --- | --- | --- | --- |
| Default | Available and at rest | Crisp label, stable boundary or affordance, minimal accent | Concrete action label |
| Hover | Pointer is over an available target | One value or underline change; no layout shift | Usually unchanged |
| Focus | Keyboard or assistive input target | Persistent high-contrast ring independent of hover and image texture | Accessible name and description available |
| Active/pressed | Input is being committed | Fast compression or value change; no long animation | Usually unchanged |
| Selected | Choice persists | Marker/check plus boundary, shape, or weight change | State word available to assistive technology |
| Disabled | Currently unavailable | Reduced prominence but readable label; no colour-only distinction | Explain prerequisite when useful; avoid tooltips as the only explanation |
| Loading | Work is in progress | Determinate progress when measurable; otherwise small labelled indicator on a clean surface | State the task; add time or cancel information when useful |
| Paused/offline | Work cannot currently continue | Stable pause/offline icon and retained progress | Explain cause, preservation, and resume path |
| Error | Action failed or input is invalid | Solid boundary, icon, message adjacency, and preserved context | State the problem, affected scope, and specific recovery |
| Warning | Action is possible but consequential | Amber or high-contrast signifier plus consequence | State risk before action; avoid vague “Are you sure?” |
| Success | Goal completed | Stable completion mark; remove loading; no compulsory celebration | Name what completed and any next step |
| Expanded | Additional content is visible | Axis-consistent reveal; trigger remains in place | Trigger reflects expanded state |
| Collapsed | Additional content is hidden | Faster reverse or immediate change in reduced motion | Trigger reflects collapsed state |

## Temporal Phase

- **First-use register:** orient clearly, label unfamiliar concepts, and show one primary path. Atmospheric copy may introduce tone only after the task is understood.
- **Repeated-use register:** shorten explanations, preserve muscle memory, support keyboard and expert paths, and stop replaying entry motion.
- **High-stakes register:** abandon ambiguity. Increase explicitness, contrast, confirmation quality, and recovery detail; reduce texture and motion.
- **End-state register:** hold a stable completion state, summarize the result, provide the next useful action, and avoid forced celebration.

## Keyboard, Focus, And Responsive Contract

- Focus order follows reading and task order, not the visual depth planes.
- All pointer interactions have keyboard and assistive-technology equivalents.
- Opening an overlay places focus at its meaningful start; closing returns focus to the invoking control.
- Reflow may change visual composition, but labels, state, focus, and primary actions remain available without horizontal scrolling at 200% zoom.
- Drag-and-drop always has a non-drag alternative, clear target state, cancel, and recovery.

## Anti-Patterns

- Mystery-meat icons, hidden affordances, hover-only information, or colour-only states.
- Glowing focus instead of a crisp indicator; focus styling that disappears into imagery.
- Silent saves, ambiguous spinners, vanished user input, errors without recovery, or disabled controls with no explanation.
- Bouncy celebration, repeated haptics, ambient sound, alarmist error red, or theatrical modal interruption.
- Delaying functional response to preserve cinematic pacing.
- Treating sparse feedback as a brand virtue when it makes the system feel broken.
