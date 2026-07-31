# Forms And Inputs

Output path: `components/forms-inputs.md`

## Inputs Covered

- Text Fields, text areas, search Fields, checkboxes, radio buttons, toggles, and switches.
- Selects, dropdowns, comboboxes, autocomplete, date pickers, and file uploaders.
- Labels, helper text, Validation, asynchronous state, submission, and Error recovery.

## User Or Maker Problem

This family lets people enter, review, choose, and correct information without the visual atmosphere obscuring labels, values, focus, constraints, or state. Makers receive explicit distinctions between input types, validation timing, keyboard behavior, and recovery so generated forms do not become collections of styled rectangles.

## Anatomy And Boundaries

| Component or module | Anatomy | Boundary | Related component |
| --- | --- | --- | --- |
| Text field | Persistent label, input, optional prefix/suffix, helper/constraint, error, character count | Owns one short value; does not own form submission or cross-field validation | Form group, Button |
| Text area | Label, multiline input, helper, count, resize affordance where appropriate | Owns free-form multiline value; not rich-text editing | Text field |
| Search field | Search label/name, input, clear action, optional suggestions/status | Finds or filters; does not silently submit unrelated data | Combobox, results list |
| Checkbox | Box, check/mixed mark, label, optional help | Independent boolean or multi-select choice | Checkbox group |
| Radio group | Group label/legend, mutually exclusive options, optional help/error | One choice from a visible set | Select |
| Switch/toggle | Control, state label, setting label, optional description | Immediate binary setting; not an action that needs a separate submit | Checkbox |
| Native select | Label, select control, options, helper/error | One choice from a manageable list; retains native platform behavior | Combobox |
| Combobox/autocomplete | Label, text input, disclosure, listbox, active option, status | Searchable selection with complex keyboard contract | Native select, search |
| Date/time input | Label, editable value, format hint, picker trigger, calendar/time panel, error | Date/time entry; supports manual entry and locale/time-zone clarity | Popover/dialog |
| File uploader | Label, browse action, optional drop region, constraints, file list, per-file progress/error/remove/retry | Selects and transfers files; drag is never the only path | Progress, status |
| Form group | Heading/legend, description, related controls, group error | Groups one decision or data concept | Form, fieldset |
| Form | Named sections, fields, submission actions, error summary, save/progress state | Owns cross-field validation, submission, preservation, and recovery | Status message, dialog |

## Variants

| Variant | Purpose | Visual difference | Behavioral difference |
| --- | --- | --- | --- |
| Text | General short input | Ordinary field | Free text with appropriate autocomplete/input mode |
| Password | Secret input | Reveal/hide control with clear state | Prevent accidental exposure; supports password managers and paste |
| Search | Filter or find | Search and clear affordances | Debounced results, count/status, Escape clears/closes as context requires |
| Multiline | Longer response | Taller resizable field | Preserves line breaks; may show count |
| Checkbox | Independent/multiple choice | Square mark | Space toggles; mixed state allowed only when meaningful |
| Radio | One-of-many choice | Circular mark | Arrow keys move within group per platform pattern |
| Switch | Immediate setting | Native switch form | Change applies immediately and is announced |
| Select | Closed choice list | Native/platform selector | Uses native behavior where list is simple |
| Combobox | Searchable/large choice | Input plus listbox | Editable query, active descendant, filtered list, explicit selection |
| File | Browse/drop upload | Clean bordered region plus file rows | Browse, keyboard, paste where supported, drag/drop, progress, retry |

Variants express input purpose. Atmospheric, glowing, borderless, “minimal,” and colour-named variants are unsupported.

## States

| State | Visual behavior | Interaction behavior | Content behavior |
| --- | --- | --- | --- |
| Default | Opaque clean surface, visible label, standard boundary | Ready | Label and relevant constraint visible |
| Hover | Slight boundary/value change | Pointer only | No content change |
| Focus-visible | Crisp focus ring plus focused boundary | Keyboard/input focus | Label remains visible; help remains available |
| Filled | Value visible with normal foreground | Editable unless read-only | Do not replace label with value |
| Read-only | Stable value and clear noneditable treatment | Select/copy where appropriate; no editing | Explain when edit occurs elsewhere |
| Disabled | Readable but unavailable; no hover | Not focusable/activatable according to native semantics | Explain prerequisite when useful |
| Loading | Local labelled indicator or field-level pending state | Input may remain usable unless conflict is real | “Checking…” or task-specific status |
| Valid | Optional quiet confirmation after meaningful check | No forced focus movement | Do not celebrate routine correctness |
| Error | Strong boundary/icon plus adjacent message | Preserve value; focus remains or moves from summary to field | Name problem and specific correction |
| Offline/interrupted | Stable preserved value and status | Allow retry/resume where possible | State what is saved locally and what is pending |

## Validation And Error Recovery

- State constraints before input where practical: format, range, file type/size, password requirements, and required/optional status.
- Validate on submission and, selectively, on blur. Avoid declaring an incomplete value invalid on every keystroke.
- Use input-time validation only when it prevents impossible input or provides clearly helpful immediate guidance.
- Associate each error programmatically with its field and retain the user’s value unless security or corruption makes that unsafe.
- On failed submission, provide a concise error summary linked to invalid fields. Move focus to the summary when it adds orientation; do not jump unpredictably on inline validation.
- For network or server failure, distinguish field invalidity from submission failure. Preserve all values, state what succeeded, and offer retry.
- Cross-field errors name all affected values and appear at the group level as well as near the repair point.
- Do not disable submit merely because the form is incomplete if doing so hides what remains; allow submission to reveal a complete, accessible validation result unless the domain requires a different pattern.

## Content And Naming Rules

- Every input has a persistent visible label. Placeholder text is an example or hint, never the sole label.
- Mark optional or required fields consistently in text; explain the convention once. Do not use colour or an asterisk without explanation.
- Helper text is concise and prospective. Error text is specific and corrective.
- Use locale-aware examples for names, addresses, phone numbers, dates, times, decimals, and currencies.
- Do not split names or identities into assumed cultural structures unless the domain requires it.
- File constraints name accepted formats, maximum size/count, and privacy implications before selection.
- Switch labels describe the setting, not “On/Off” alone. The control exposes current state programmatically.
- Search result status announces count changes without interrupting every keystroke.

## Token Dependencies

| Part | Required token | Override boundary |
| --- | --- | --- |
| Field surface | `component.field.background` | Opaque semantic surface only |
| Value | `component.field.value` | Never opacity or texture override |
| Label | `component.field.label` | May increase emphasis, not disappear |
| Help text | `component.field.help` | Must remain readable |
| Standard boundary | `component.field.border` | Platform native may replace if equivalent |
| Focus boundary/ring | `component.field.focus.*` | Native focus accepted if visible and persistent |
| Error boundary/icon/text | `component.field.error.*` | Error always includes copy and recovery |
| Disabled surface | `component.field.disabled.background` | No local opacity shortcut |
| Form actions | `component.button.*` | Follow actions contract |
| Progress | `component.progress.*` | Determinate when measurable |

## Accessibility And Localization

- Use native input semantics, labels, fieldsets/legends, error association, autocomplete, and input modes.
- Keyboard access covers every control. Combobox, date picker, and listbox follow the current platform/WAI-ARIA pattern rather than a custom key scheme.
- Preserve visible focus, logical tab order, screen-reader order, and a non-drag path for upload/reorder.
- Controls meet platform target guidance; checkbox/radio labels enlarge the activation target.
- Support browser zoom, 200% text reflow, native text scaling, speech input, password managers, autofill, copy/paste, and high contrast.
- Do not block paste, zoom, or password-manager insertion. Do not impose arbitrary time limits.
- Error, required, checked, mixed, expanded, selected, invalid, busy, and progress states are exposed programmatically.
- Allow 35%+ text expansion, multiline labels/help/errors, mirrored layouts, and local date/number formats.
- Texture, bloom, chromatic split, and image backgrounds are prohibited behind fields and validation.

## Code And API Contract

```text
Field {
  id: required stable identifier
  name: required submission key
  label: required localized string
  value: controlled or native value
  type: text | email | url | tel | password | search | number | date | time
  required?: boolean
  optionalLabel?: string
  helperText?: string
  error?: { id, message, recovery? }
  autocomplete?: valid platform token
  inputMode?: native input mode
  readOnly?: boolean
  disabled?: boolean
  busy?: boolean
  onInput / onChange / onBlur
}
```

- Checkbox/radio/switch APIs require group name/state semantics and visible labels.
- Combobox APIs require input value, selected value, open state, active option, results, loading, empty, and error states.
- Uploader APIs require accepted types, size/count limits, file rows, progress, cancel, remove, retry, and failure reason.
- Unsupported: arbitrary raw colours, placeholder-only label, error boolean without message, custom keyboard mode, upload by drag only, and generic `variant="atmospheric"`.

## Examples And Anti-Patterns

- **Do:** show “Maximum 10 MB. PDF or DOCX.” before file selection and retain failed files with “Retry upload.”
- **Do:** use a field error such as “Enter a date on or after 30 July 2026.”
- **Do:** let a user type a date or open the picker.
- **Avoid:** glowing border-only validation, red/orange-only errors, disappearing labels, or live validation that scolds partial input.
- **Avoid:** custom selects for five simple options, silent asynchronous checks, blocked paste, or disabled submit with no explanation.
- **Avoid:** textured fields laid over identity imagery, fixed-height error rows, or truncated translated labels.

## Related Patterns

- Actions and triggers.
- Feedback, status, progress, and recovery.
- Dialogs, popovers, and disclosure.
- Keyboard/focus behavioral patterns.
- Platform-native form patterns.
