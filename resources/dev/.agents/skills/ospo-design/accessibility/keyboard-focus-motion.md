# Keyboard, Focus, And Motion

Output path: `accessibility/keyboard-focus-motion.md`

## Keyboard And Focus Contract

| Element family | Focus order | Focus visual | Keyboard behavior | Escape/recovery |
| --- | --- | --- | --- | --- |
| Links and Buttons | DOM/native task order; one target per action | Crisp 2px minimum ring with offset or equivalent native visual | Link activates with Enter; Button with Enter/Space | No Escape behavior unless it owns an overlay/disclosure |
| Text Fields/text areas | Label/help/error precede or associate with field; source order matches reading | Ring plus focused boundary; error remains distinguishable | Native editing, selection, clipboard, autocomplete, IME; Tab leaves | Escape may clear Search or revert controlled edit only when documented |
| Checkbox/radio/switch | Group legend then options; label activates target | Container/mark focus, not colour alone | Space toggles; radio arrows move within group per platform | Restore prior selection only through explicit cancel/undo |
| Select/combobox | Label then input/trigger then popup options | Focus stays clear on input/trigger and active option | Native select behavior or current composite-widget pattern; arrows/typeahead/Enter as appropriate | Escape closes without accidental commit and returns/retains Focus |
| Menu | Trigger then menu according to platform pattern | Trigger and active menu item each visibly focused | Open via trigger; arrows navigate items; Enter/Space activates as defined | Escape closes and returns Focus to trigger |
| Tabs | Tab list before active panel content | Focused tab distinct from Selected tab | Arrow keys move among tabs; activation model documented; Tab enters panel | Focus remains on tab when switching; no trap |
| Accordion/disclosure | Trigger appears in reading order before controlled panel | Trigger Focus remains visible in both expanded states | Enter/Space toggles; panel content follows | Collapse keeps Focus on trigger |
| Dialog/modal | Invoking control precedes overlay; initial Focus at title, first field, or safest action | Native/high-contrast-visible Focus inside opaque overlay | Tab/Shift+Tab contained only while truly modal; actions use native keys | Escape closes only when safe; close returns Focus to invoker or logical successor |
| Tooltip/popover | Trigger remains in order; interactive popover content follows trigger | Trigger Focus visible; popover targets ordinary focus | Tooltip does not receive focus; interactive popover uses ordinary controls | Escape dismisses; pointer hover/focus content remains available long enough |
| Navigation | Skip path first where needed; landmarks and destinations in reading/task order | Current and Focus states remain distinct | Links use Enter; menu/tab composite patterns as appropriate | Back reverses navigation; route change moves Focus only to meaningful context |
| Data Table/grid | Caption/controls then cells in semantic order; native Table preferred | Focus/selection cell or row clearly distinguished | Sorting/filtering controls ordinary; interactive grids follow platform grid pattern | Escape exits edit/menu; preserves selected row/filter |
| Drag/drop/reorder | Alternative controls appear with item; targets follow item order | Source and target state visible with text/shape | Keyboard “Move up/down/to…” or browse alternative required | Escape cancels and restores original order/selection |
| File upload | Label/browse action then selected-file rows/actions | Browse, remove, retry, cancel each visibly focused | Enter/Space opens picker; drag is optional | Cancel transfer preserves clear file state; Retry targets failed file |
| Identity media | Usually not focusable unless a link/control | Action target receives clean Focus outside texture | Play/pause/captions/description controls use native media behavior | Escape exits full screen; reduced-motion/static alternative available |

## Focus Management Rules

- Source/DOM/accessibility order follows meaning; visual z-plane, crop, and atmosphere do not determine Focus order.
- Do not use positive tab indices or make noninteractive decorative surfaces focusable.
- Programmatic Focus movement is limited to genuine context changes: opening/closing a modal, navigating to a new view, reaching a validation summary, or restoring a removed trigger.
- A single-page route change updates title/current location and moves or announces context without surprising loss of task state.
- Removing the focused element moves Focus to the nearest meaningful control or section, never to the document start by accident.
- Sticky headers, toasts, dialogs, and browser chrome do not fully obscure the focused target; use scroll margin/padding where needed.
- Focus remains visible on Selected, invalid, pressed, and disabled-adjacent states. It is never replaced by hover or a soft glow.
- High-contrast/forced-colour mode uses native/system focus colours and solid geometry.

## Focus Visual Specification

- Use `semantic.focus.ring` and a `2px` minimum solid perimeter with visible separation from adjacent colours; a `4px` target offset is preferred where geometry allows.
- Do not animate, blur, pulse, texture, or chromatically split the ring.
- Ensure the ring is not clipped by `overflow`, masks, media crops, transforms, or rounded containers.
- On dense controls, enlarge the target/container before shrinking the focus geometry.
- Platform-native focus is preferred when it meets visibility, contrast, persistence, and state-distinction requirements.

## Motion Accessibility

### Reduced Motion Replacement

| Full-motion purpose | Reduced motion replacement | Meaning preserved by |
| --- | --- | --- |
| Immediate feedback | `0–80ms` value change or instant state | Text/icon/shape/programmatic state |
| Disclosure | Cut or opacity change under `100ms` | Expanded state and controlled-region relationship |
| Axis transition | Immediate replacement or short fade | Updated title/current state/focus context |
| Atmospheric emergence | Static final image on first frame | Composition and hierarchy |
| Processional/parallax scene | Static route and labelled sequence | Ordered labels/position |
| Indeterminate loader | Static icon plus “Loading…” or restrained nonspatial indicator | Busy state and task label |
| Success reveal | Stable completion mark and result copy | Completion semantics/receipt |
| Error interruption | Immediate error region | Error semantics, message, and Recovery |

### Duration Limits

- Direct interaction acknowledgment begins within `100ms`.
- Routine functional transitions use roughly `100–300ms`.
- Larger product navigation stays under `500ms`.
- Optional editorial emergence may extend to `800ms` only when nonessential, controllable, and absent on repeat/reduced-motion use.
- Exits are typically faster than entries.
- No animation may delay authentication, consent, payment, error Recovery, form submission, or repeated task work.

### Forbidden Parallax, Flash, And Shake

- No scroll-linked parallax, zoom-through-depth, camera shake, full-field wipe, rapid thermal alternation, or continuous animated grain.
- No more than three flashes in a one-second period within applicable flash thresholds; the design default is no flashing.
- No shaking field as the only error cue, pulsing focus, breathing Buttons, looping route animation, or auto-playing processions.
- Avoid large scale/position changes and vestibular motion even when the operating system preference is unavailable; expose a product-level control for optional media.

### Non-Motion State Cues

- Label, icon, shape, boundary, position, explicit value, progress text, and programmatic state carry meaning.
- Before/after composition preserves subject and control location.
- A route uses ordered labels and current/completed markers.
- Loading uses a task name and busy/progress semantics.
- Selection uses check/marker and state; error uses message and Recovery; Completion uses result copy.

## Motion Implementation

- Read the user/platform preference before first render to avoid a motion flash.
- Pause optional media when off-screen, backgrounded, or user-paused; persist the preference.
- Animate transform and opacity where possible; pre-render atmospheric texture rather than animating full-field noise or blur.
- Motion is interruptible. New input retargets or reverses from the current state instead of queuing.
- Auto-updating information provides pause/stop/hide controls when required and does not announce every change.
- Audio and haptic feedback have simultaneous visual/semantic equivalents and respect device settings.

## Verification

- Complete every workflow with keyboard only, including errors, retry, dialog close, drag/reorder alternative, and upload.
- Test forward and reverse Focus order, context changes, removed controls, sticky regions, 200% text, zoom/reflow, and RTL.
- Inspect Focus in light, dark, high contrast/forced colours, selected, invalid, and image-adjacent states.
- Enable Reduced motion before launch and during a session; no required meaning or control may disappear.
- Test with animation scale disabled/slow, screen readers, external keyboards, switch access, and target platform navigation.

## Anti-Patterns

- Focus order matching visual coordinates while reading order differs.
- Glow-only Focus, clipped ring, hover-as-focus, or restoring Focus to a vanished trigger.
- Custom keyboard schemes for familiar controls, keyboard traps, or Escape that discards data.
- Reduced motion implemented as “no feedback,” or a media-query override added after first animation.
- Parallax, shake, pulse, animated grain, or cinematic delay used to make a static state feel on-brand.
