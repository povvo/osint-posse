# Domain And Platform Patterns

Output path: `patterns/domain-platform-patterns.md`

## Platform Conventions

| Platform | Navigation | Forms | Feedback | Native behavior | Exceptions |
| --- | --- | --- | --- | --- | --- |
| Web | Semantic links, landmarks, deep URLs/history, responsive header/side navigation, skip path | Native HTML labels/inputs first; custom composite widgets follow current WAI-ARIA patterns | Inline/status regions, banners, dialogs, durable state; toasts are supplemental | Keyboard, `:focus-visible`, browser zoom/reflow, autofill, password managers, forced colours, reduced motion | Identity media may use CSS/offline transforms, but functional content remains semantic and texture-free |
| iOS/iPadOS | Native navigation stack, tab bar, sidebar, toolbar, system back gesture | Native text fields, pickers, switches, sheets, keyboard and content types | Inline feedback, native alerts/sheets where warranted, platform haptics sparingly | Dynamic Type, VoiceOver, Increase Contrast, Reduce Motion, external keyboard, 44pt design target | Atmospheric transitions cannot replace native navigation or delay actions |
| Android | Native navigation, app bar, navigation bar/rail/drawer, system Back | Native/Material fields, pickers, switches, autofill, IME actions | Inline messages, snackbars for recoverable transient action, dialogs/notifications by scope | Font scaling, TalkBack, keyboard/D-pad, high-contrast capabilities, animation scale, 48dp target | Material colour roles may map semantically; do not force identical iOS/web chrome |
| Windows | Native title/app bars, NavigationView, menus, resizable adaptive panes | WinUI/XAML controls, validation, keyboard-first forms, system pickers | Info bars, teaching tips, ContentDialog, notifications by scope | Narrator, visible keyboard focus, text scale, high-contrast resources, system animation setting, window resize | Dense desktop Tables/toolbars may use compact spacing while preserving targets/focus |
| React Native | Shared route model with per-platform native stacks/tabs/drawers | Native-backed controls or carefully reviewed components with platform input behavior | Shared semantic state rendered through platform-appropriate feedback | `AccessibilityInfo`, `allowFontScaling`, platform target size, hardware keyboard/TV focus where applicable | Branch when native purpose differs; do not conceal differences behind one web-like component |

## Platform Equivalence Contracts

| Shared purpose | Web | iOS/iPadOS | Android | Windows | Invariant |
| --- | --- | --- | --- | --- | --- |
| Primary destination | Real link within nav landmark | Native tab/sidebar/stack destination | Native bar/rail/drawer/stack destination | NavigationView/menu destination | Visible label, current state, deep/restorable context |
| Go back | Browser/history or explicit back link when needed | Native back button/gesture | System Back/up semantics | Native back/history command | Reverses navigation; preserves prior state |
| Choose from simple list | Native select/radio | Native picker/menu/list | Native dropdown/radio/list | Native ComboBox/radio/list | Label, selection, keyboard/screen-reader state |
| Confirm consequence | Inline/undo or accessible dialog | Native alert/sheet/dialog by risk | Native dialog/sheet by risk | ContentDialog by risk | Action/object/consequence/reversibility explicit |
| Show transient undo | Snackbar/toast plus durable state | In-context banner/undo appropriate to app | Snackbar with action | Teaching tip/info bar/notification by scope | Not the only record; focus/reading time protected |
| Indicate focus | Solid `:focus-visible` outline | Native external-keyboard focus | Native keyboard/D-pad focus | Native focus visual | Visible, persistent, high contrast, not glow |
| Reduce motion | `prefers-reduced-motion` branch | System Reduce Motion | Animation duration scale/accessibility setting | System animation setting | Static hierarchy and state cue preserve meaning |
| Present identity scene | Responsive image with focal metadata | Pre-rendered asset in adaptive container | Pre-rendered asset in adaptive container | Resolution-aware decoded asset | Recognition core, alt/purpose, clean support content |

## Domain Patterns

| Domain | Module | Vocabulary | Constraint | Example |
| --- | --- | --- | --- | --- |
| E-commerce | Product summary, cart, checkout, receipt | Product, variant, price, stock, delivery, returns, total | Accurate inspection, complete costs/terms, reversible edits, secure payment | An atmospheric campaign plate leads to a clean product page and explicit checkout |
| Education | Lesson/activity, discussion, assessment, progress | Objective, activity, attempt, feedback, rubric, completion | Clear instruction, save/resume, authorship, accessibility, assessment integrity | A passage image opens a module; labelled Steps and feedback remain literal |
| Finance | Quote, position, chart, transaction review, receipt | Value, change, unit, source, timestamp, pending, settled | Precision, stale state, idempotency, risk, audit trail, regulation | Signed values and timestamps accompany a restrained highlighted series |
| Cooking | Recipe, ingredient scaler, step, timer, safety note | Ingredient, quantity, serving, temperature, time, doneness, allergen | Locale units, accurate safety/inspection, hands-free access, timer alternatives | Editorial dish art is separate from clear ingredient/step and doneness imagery |
| Service journey | Eligibility, appointment, case stage, document request, escalation | Status, requirement, due date, owner, next action, contact | Privacy, deadlines, preservation, clear handoff and escalation | A route supports labelled case stages and next requirements |
| Omnichannel | Handoff, receipt, resume link/code, offline state | Continue, saved, synced, pending, expires, verified | Secure transfer, identity, expiry, fallback, continuity | A person begins on web and resumes natively with state and receipt intact |

## Domain-to-Expression Mapping

- **E-commerce:** use identity scenes for campaigns and category/editorial covers. Do not recolour product truth, hide prices, or animate checkout.
- **Education:** use Iconic Vigil for individual reflection, Luminous Gathering for reviewed collaborative content, and Processional Passage for optional chapter art. Keep real learners identifiable by appropriate representation.
- **Finance:** use the carbon shell and quiet typography; treat thermal colours as brand emphasis, not default profit/loss or risk semantics.
- **Cooking:** use warmth as atmosphere, not a safety code. Exact timer, temperature, quantity, allergen, and doneness information stays clean.
- **Service journeys:** the route metaphor may support orientation, but named stages, current status, deadlines, and Recovery remain primary.
- **Omnichannel:** visual treatment may adapt by channel; semantic state, identity, consent, and saved work do not.

## Cross-Platform Coherence

- **Preserve:** semantic intent, component state, data, copy meaning, recovery, token relationships, carbon/thermal restraint, clean information, and the one-event identity grammar.
- **Adapt:** navigation chrome, control anatomy, system colours, typography metrics, target sizes, haptics, feedback surfaces, density, back behavior, permissions, and motion durations.
- **Never flatten:** iOS, Android, Windows, Web, and React Native into one web-styled shell; domain modules into generic Cards; status into brand colours; or accessibility preferences into optional styling.
- **Parity test:** the same task can be completed, understood, interrupted, resumed, and recovered on every supported platform even when the visual component differs.
- **Identity test:** a platform-native artifact still feels related through restrained palette, typography, spacing, clean support, and optional scene imagery—without overriding native behavior.

## Implementation Review

1. Name the user purpose and product Domain.
2. Select the native Platform pattern before applying visual tokens.
3. Map shared semantic and component contracts to native controls.
4. Add the least atmospheric treatment that still creates recognition.
5. Test navigation/back, form input, focus, feedback, large text, high contrast, reduced motion, localization, offline/error, and state restoration.
6. Record platform exceptions in transforms, not local component code.

## Anti-Patterns

- Shipping a single cross-platform component tree that imitates Web controls everywhere.
- Replacing native navigation, forms, dialogs, permissions, focus, or back behavior with cinematic custom UI.
- Treating a domain’s established vocabulary as off-brand and renaming it metaphorically.
- Using warm/cool colour alone for finance, education, service, cooking, or commerce status.
- Identical visual density across mobile, desktop, editorial, and data-heavy contexts.
- Claiming cross-platform coherence because screenshots match while behavior, accessibility, or Recovery diverges.
