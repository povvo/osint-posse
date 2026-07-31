# Actions And Triggers

Output path: `components/actions-triggers.md`

## Actions Covered

- Primary, secondary, tertiary, destructive, disabled, and icon Buttons.
- Links, disclosure triggers, Button groups, and platform-native floating actions.
- Trigger hierarchy based on purpose, consequence, and persistence rather than decorative colour.

## User Or Maker Problem

This family lets a person initiate an action, navigate, reveal content, select a command, or commit a consequential change while preserving clear hierarchy, immediate feedback, keyboard/touch access, and recovery. Makers receive one contract that prevents links from behaving like buttons, controls from becoming atmospheric, and visual variants from multiplying without purpose.

## Anatomy And Boundaries

| Component or module | Anatomy | Boundary | Related component |
| --- | --- | --- | --- |
| Button | Container, visible label, optional leading/trailing icon, focus indicator, optional progress indicator | Performs an action in the current context; does not navigate to a new resource | Status message, dialog, form |
| Link | Text label, optional external/download indicator, focus treatment, destination semantics | Navigates to a resource or location; does not impersonate a submit action | Navigation item, breadcrumb |
| Icon button | Target container, familiar icon, accessible name, optional visible label/badge | Only for quickly recognised actions in clear context; not a solution for tight layouts | Tooltip, menu trigger |
| Disclosure trigger | Button, direction/state icon, controlled-region relationship | Expands/collapses owned content; does not navigate | Accordion, menu, popover |
| Button group | Group label when needed, ordered Buttons, shared spacing, group-level help | Coordinates related actions; does not erase individual names or states | Toolbar, segmented choice |
| Floating action | Platform-native elevated target, icon, label where platform pattern supports it | Reserved for one persistent high-frequency primary action; omitted on platforms/domains where it conflicts with convention | Native navigation shell |

## Variants

| Variant | Purpose | Visual difference | Behavioral difference |
| --- | --- | --- | --- |
| Primary | Most important next action in one local decision group | Warm semantic action surface with dark foreground | Ordinary action; at most one visible primary per group |
| Secondary | Valid alternative or less prominent action | Lifted dark/light surface with clear boundary | Same event semantics as primary |
| Tertiary | Low-emphasis local command | Text/quiet surface with visible hover/focus | Same action semantics; never used when discoverability is critical |
| Destructive | Deletes, revokes, removes, or causes material loss | Darker consequential surface plus explicit label | May require confirmation, undo, or recovery proportional to risk |
| Icon | Familiar compact action | 20–24-unit icon inside full target | Requires accessible name; visible label for unfamiliar meaning |
| Disclosure | Shows or hides owned content | State icon plus label; no colour-only state | Updates expanded/collapsed state and controlled-region relationship |
| Floating | Persistent native primary action | Native platform form; no custom atmospheric glow | Appears only where platform/domain convention supports it |

Ghost is not a separate decorative variant: use tertiary or a link based on behavior. A disabled appearance is a state, not a variant.

## States

| State | Visual behavior | Interaction behavior | Content behavior |
| --- | --- | --- | --- |
| Default | Stable semantic surface, readable label, optional icon | Available | Verb-plus-object label |
| Hover | One value/boundary change, no glow or layout shift | Pointer only; no state commitment | Label unchanged |
| Focus-visible | Crisp 2px minimum ring with offset, independent of hover | Keyboard focus; Enter/Space for Button, Enter for link | Accessible name and description exposed |
| Active/pressed | Brief value change or `1–2px` container compression | Commits once; debounce/deduplicate where needed | Label normally unchanged |
| Selected/toggled | Persistent marker, fill, or state label | Only on controls with toggle semantics | Announces pressed/selected state |
| Disabled | Lower prominence but readable content; no hover | Removed from activation; native disabled semantics | Explain prerequisite nearby when useful |
| Loading | Stable width, labelled progress indicator, focus retained | Prevent duplicate commit; allow cancel where meaningful | Use “Saving…” or equivalent task label; preserve original action context |
| Success | Action returns to usable state or transitions to result | Completion announced in context | Confirm affected object/state outside the Button |
| Error | Button remains usable or becomes retry action | Focus stays unless error requires directed correction | Error message names problem and recovery; Button may become “Retry upload” |

## Hierarchy And Risk Rules

- One primary Button per local decision group; page-level and modal groups may each have one when contexts are distinct.
- Arrange safe/likely action first according to platform and locale convention; do not rely on colour or left/right position alone.
- Consequential actions name the consequence: “Delete 18 files,” not “Continue.”
- Use a dialog only when the action is blocking, irreversible, unusually risky, or requires a choice that cannot be recovered inline.
- Prefer undo for reversible actions. Confirmation is not a substitute for recovery.
- A Button never becomes disabled merely to hide an unmet validation rule; expose requirements before commit.

## Content And Naming Rules

- Use sentence case and a concrete verb plus object: “Save draft,” “Share report,” “Remove access.”
- Keep ordinary labels to roughly two to four words; allow expansion and wrapping when translation requires it.
- Do not use “Yes,” “No,” “OK,” “Submit,” or “Continue” when a specific action can be named.
- External links indicate destination or behavior when surprising. Download links include file type/size when helpful.
- Icon Buttons use visible labels unless the action is universally familiar in context; all receive an accessible name.
- Loading labels identify the operation. Do not replace a label with an unlabeled spinner.
- Avoid frontier idioms, weapon metaphors, and poetic action language.

## Token Dependencies

| Part | Required token | Override boundary |
| --- | --- | --- |
| Primary container | `component.button.primary.background` | Purpose-bearing variant only |
| Primary label/icon | `component.button.primary.foreground` | Never local raw colour |
| Secondary container | `component.button.secondary.background` | Purpose-bearing variant only |
| Secondary label/icon | `component.button.secondary.foreground` | Never opacity-only hierarchy |
| Destructive container | `component.button.destructive.background` | Consequential actions only |
| Destructive label/icon | `component.button.destructive.foreground` | Must retain declared contrast |
| Disabled parts | `component.button.disabled.*` | No hover/press override |
| Focus | `component.button.focus.ring` | Platform-native focus may replace if contract is met |
| Content gap | `component.button.content.gap` | May expand for large text/localization |
| Padding | `component.button.padding` | Density may change padding, never target floor |
| Feedback timing | `component.button.feedback.duration` | Reduced-motion mode may shorten |

## Accessibility And Localization

- Use native `<button>` for actions and `<a href>` for navigation on the web; equivalent native controls on other platforms.
- Keyboard: Button activates with Enter and Space; link with Enter; focus order follows task order; no positive tab index.
- Visible focus is never clipped by container overflow or atmospheric imagery.
- Target design goal: 44×44 CSS px/pt on web/iOS, 48×48dp on Android, and current native/stricter guidance elsewhere. WCAG conformance is evaluated independently.
- Labels remain visible at 200% zoom and with platform text scaling; permit at least 35% localization expansion and avoid fixed-height Buttons.
- Announce loading, pressed/expanded state, result, and errors with native accessibility semantics. Do not repeatedly announce decorative state.
- Colour is never the only distinction among primary, destructive, selected, disabled, or error states.
- Icon-only controls expose names; tooltips do not replace names or visible labels for unfamiliar actions.

## Code And API Contract

```text
Button {
  variant: primary | secondary | tertiary | destructive
  size: compact | default
  type: button | submit | reset
  label: required localized string
  iconStart?: Icon
  iconEnd?: Icon
  disabled?: boolean
  loading?: boolean
  pressed?: boolean
  expanded?: boolean
  controlsId?: string
  describedBy?: string
  onActivate: event
}
```

- `label` remains present in the accessibility tree during loading.
- `loading` and `disabled` are distinct: loading communicates work and may offer cancel; disabled communicates unavailable.
- `pressed` is allowed only for toggle Buttons; `expanded` only for disclosure ownership.
- Unsupported props: arbitrary colour, glow, texture, raw duration, icon-only without accessible name, and a generic `styleVariant`.
- Link uses a real destination and navigation event; it is not rendered through the Button API.

## Examples And Anti-Patterns

- **Do:** “Save draft” as primary and “Cancel” as secondary; preserve focus and show “Draft saved” in context.
- **Do:** “Delete 18 files” with consequence text and undo where feasible.
- **Do:** use a labelled disclosure Button with `expanded` state and a controlled region.
- **Avoid:** two primary Buttons competing in one dialog.
- **Avoid:** glowing icon Buttons over textured imagery, invisible focus, or 24px targets.
- **Avoid:** a link styled as a Button that fires a destructive action, or a Button styled as a link that navigates.
- **Avoid:** spinner-only loading, disabled submit with no explanation, or “Something went wrong” with no retry path.

## Related Patterns

- Forms and validation.
- Navigation and wayfinding.
- Feedback, status, dialogs, undo, and recovery.
- Behavioral states and reduced motion.
- Platform-native action patterns.
