# Navigation And Wayfinding

Output path: `components/navigation-wayfinding.md`

## Navigation Covered

- Headers, navigation bars, app bars, side Navigation, menus, and native back behavior.
- Breadcrumbs, tabs, disclosure/accordions, pagination, footers, and deep links.
- Wayfinding, current location, progress context, Platform adaptation, responsive behavior, and state restoration.

## User Or Maker Problem

This family helps people understand where they are, what nearby destinations exist, how to move, and how to return without making the product’s atmospheric imagery carry information architecture. Makers receive an equivalence contract that preserves platform-native navigation, explicit current state, keyboard/focus behavior, and responsive continuity.

## Anatomy And Boundaries

| Component or module | Anatomy | Boundary | Related component |
| --- | --- | --- | --- |
| App/header bar | Product/context identity, page title, primary destinations or menu trigger, task actions | Establishes current context; does not hold every action | Side nav, overflow menu |
| Side navigation | Landmark/container, labelled destination list, current marker, optional groups/collapse | Persistent top-level or section navigation on suitable widths | Header, navigation item |
| Bottom/tab bar | Native container, small destination set, icon, visible label, current state | Peer top-level destinations; not arbitrary actions or workflow steps | Native app shell |
| Menu | Trigger, labelled command/destination list, groups, checked/disabled state, focus management | Temporary choices; not a substitute for visible primary navigation | Popover, Button |
| Breadcrumb | Ordered ancestor links, current page text, accessible name | Shows hierarchy; does not replace back-stack semantics | Page title, link |
| Tabs | Tab list, labelled tabs, active tab, associated panels | Switches peer views in one context; not a multi-step process | Segmented control, stepper |
| Accordion | Disclosure Button, controlled panel, expanded state | Reveals content in place; it is not navigation unless the trigger is a real link | Disclosure trigger |
| Pagination | Previous/next, page or position controls, current indicator, result context | Moves among discrete result pages; not an unlabeled infinite stream | Results list |
| Footer | Secondary navigation, legal/support links, metadata | Low-priority destinations; never the only route to a critical action | Header |
| Route/progress cue | Current step, completed/upcoming states, labels | Indicates sequence; does not replace task content or navigation controls | Sequence/progress |

## Variants

| Variant | Purpose | Visual difference | Behavioral difference |
| --- | --- | --- | --- |
| Persistent side | Wide-screen product hierarchy | Calm lifted/dark rail with visible labels | Remains available; collapses only with explicit responsive rule |
| Compact header | Narrow screen orientation/actions | Title plus native back/menu/actions | Uses native screen stack and overflow |
| Bottom destination | Mobile peer destinations | Native bar, icon plus label, persistent current state | Preserves per-destination history where platform expects it |
| Tabs | Peer content views | Strong current marker, no atmospheric glow | Arrow-key or platform-native tab behavior |
| Breadcrumb | Deep web hierarchy | Quiet inline chain with current page | Each ancestor is a real link |
| Menu | Temporary command list | Opaque clean overlay, grouped items | Opens from trigger, roves focus, closes predictably |
| Pagination | Long result set | Current page/position and previous/next | Updates URL/history and restores focus/scroll appropriately |

Variants follow information architecture and platform convention. “Minimal,” icon-only, glowing, immersive, and image-overlay are not navigation variants.

## States

| State | Visual behavior | Interaction behavior | Content behavior |
| --- | --- | --- | --- |
| Default | Readable label and stable affordance | Available | Destination or command name |
| Hover | One value/underline change | Pointer only | No label change |
| Focus-visible | Crisp ring or native focus visual | Keyboard focus; activation follows native element | Accessible name and current/expanded state exposed |
| Active/pressed | Brief response, no route-dependent animation delay | Activates once | No speculative state before navigation succeeds |
| Current/selected | Persistent surface/marker plus `current` semantics | Usually not reactivated unless refresh behavior is explicit | Label remains visible |
| Disabled/unavailable | Readable state, no hover | Not activatable | Explain prerequisite for commands; avoid disabled destinations when hiding is clearer |
| Loading transition | Existing context remains stable; local labelled progress where needed | Prevent duplicate navigation, allow back/cancel where safe | State what is loading |
| Error | Current context retained with clear recovery | Retry or alternate route | Explain route/content failure, not “navigation error” alone |
| Expanded/collapsed | Trigger icon and panel state agree | Predictable focus and Escape/outside behavior by component type | Trigger label remains stable |

## Wayfinding Rules

- Every view exposes a meaningful page/screen title and current location to assistive technology.
- Current state uses at least two signals: marker/surface plus semantic state or text. Colour alone is insufficient.
- Preserve URLs/deep links on the web and native back stacks on apps. The Back action reverses navigation, not an arbitrary visual transition.
- Restore scroll, focus, filter, and draft state when returning where user expectation supports it.
- Use a single information-architecture axis. A visual route or luminous line may support orientation in editorial content, but never replace labels, current state, or hierarchy.
- Reserve breadcrumbs for meaningful hierarchy; do not generate them from URL segments without content semantics.
- Tabs switch peer panels in place. Steps represent progression. Links navigate. Buttons act. Do not blend these roles.
- Infinite scrolling requires a reachable footer or alternate pagination/load-more path, position preservation, and an announcement strategy.

## Responsive And Platform Behavior

| Context | Preferred behavior | Invariant |
| --- | --- | --- |
| Narrow web | Header plus labelled menu or compact primary destinations | Page title, current location, keyboard path, deep link |
| Wide web | Persistent side/top navigation where hierarchy warrants | Same destination names and route semantics |
| iOS/iPadOS | Native navigation stack, tab bar, sidebar, toolbar, and back behavior | Semantic destinations, state restoration, accessible labels |
| Android | Native navigation, app bar, navigation rail/bar/drawer, system back | Semantic destinations, state restoration, accessible labels |
| Windows | Native title/app bars, NavigationView/menu/focus patterns | Keyboard focus, current state, resizable layout |
| React Native | Branch to the native convention of the target platform | Shared route model and semantic names, not identical chrome |

Do not force a hamburger, tab bar, or side rail solely for visual consistency. Same purpose may use different native components.

## Content And Naming Rules

- Use stable destination nouns (“Projects,” “Reports”) and concrete command verbs (“Export report”).
- Keep visible labels for top-level destinations. Icons supplement; they do not replace unfamiliar names.
- Avoid clever, poetic, frontier-coded, or organization-internal labels.
- Menu group headings describe a real category; do not overgroup small menus.
- Indicate external destination, new context, download, or destructive command when the behavior may surprise.
- Allow localization expansion and wrapping where platform conventions permit; do not truncate the only distinguishing word.
- Breadcrumb current page is text, not a redundant active link, unless platform behavior explicitly differs.

## Token Dependencies

| Part | Required token | Override boundary |
| --- | --- | --- |
| Default label | `component.nav.label` | Never raw colour or opacity-only |
| Current label | `component.nav.label.selected` | Must pair with selected surface/semantics |
| Current surface | `component.nav.surface.selected` | Purpose is current/selected only |
| Icon | `component.nav.icon` | Visible label required for unfamiliar destination |
| Focus | `component.nav.focus.ring` | Native equivalent accepted |
| Menu/panel surface | `component.panel.background` | Opaque and low texture |
| Menu/panel boundary | `component.panel.border` | May omit when native separation is sufficient |
| Navigation motion | `semantic.motion.axis.*` or native semantic transition | Reduced-motion override required |

## Accessibility And Localization

- Use navigation landmarks with unique accessible labels; include a skip link or native equivalent to bypass repeated navigation.
- Links have real destinations; Buttons control menus/disclosures. Expose `current`, `selected`, `expanded`, `controls`, and disabled state correctly.
- Keyboard focus order follows reading/task order. Menus, tabs, and composite widgets follow current native/WAI-ARIA keyboard contracts.
- Focus moves only when navigation changes context or an overlay opens; return it to the trigger on close.
- Touch targets meet current platform guidance; visible icons may remain smaller.
- Support zoom, large text, window resize, orientation, RTL, high contrast, reduced motion, and translated labels without hiding destinations.
- Announce route/title changes in single-page applications without stealing focus unexpectedly.
- Do not animate large routes, parallax, or page transitions for reduced-motion users.

## Code And API Contract

```text
NavigationItem {
  id: stable route id
  hrefOrRoute: required destination
  label: required localized string
  icon?: Icon
  current?: page | step | location | false
  badge?: { text, accessibleLabel }
  disabled?: boolean
}

NavigationContainer {
  label: required landmark label
  items: NavigationItem[]
  variant: platform-native | header | side | tabs | breadcrumb | pagination
  collapsed?: boolean
  onNavigate
}
```

- Tabs require tab/panel IDs, selected index, focus behavior, and lazy-loading semantics.
- Menus require trigger ID, open state, item roles, grouping, focus entry/return, Escape behavior, and collision handling.
- Unsupported: arbitrary colour variant, icon-only top-level destination, positive tab index, fake link without destination, and local back-stack replacement.

## Examples And Anti-Patterns

- **Do:** retain a labelled current destination and its history when a mobile user switches tabs.
- **Do:** use a processional visual route in an editorial chapter while keeping a standard labelled step list.
- **Do:** update page title, URL, current state, and focus/announcement behavior together.
- **Avoid:** glowing dots as the only wayfinding, image hotspots without labels, or navigation hidden until hover.
- **Avoid:** accordion triggers implemented as links, tabs used as workflow steps, or Buttons used for page navigation.
- **Avoid:** custom cross-platform bars that ignore native back, keyboard, window, and accessibility behavior.

## Related Patterns

- Actions and triggers.
- Sequence and progress.
- Menus, overlays, and feedback.
- Behavioral focus/state contracts.
- Domain and platform patterns.
