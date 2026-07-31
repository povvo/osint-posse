# Content And Data Display

Output path: `components/content-data-display.md`

## Display Covered

- Cards, content/product/event items, list rows, selectable tiles, thumbnails, panels, and widgets.
- Tables, charts, graphs, badges, chips, tags, avatars, dense grids, and structured data fields.
- Editorial identity imagery beside clean informational surfaces.

## User Or Maker Problem

This family helps people scan, compare, inspect, select, and understand content or data without turning every item into a cinematic plate. Makers receive clear boundaries between a Card, list row, Table, chart, status badge, filter chip, avatar, and editorial scene so atmosphere supports hierarchy rather than reducing information density or accuracy.

## Anatomy And Boundaries

| Component or module | Anatomy | Boundary | Related component |
| --- | --- | --- | --- |
| Content Card | Optional media, eyebrow/category, title, summary, metadata, optional action | Summarizes one item; not a generic container for arbitrary nested UI | Link, scene thumbnail |
| List item | Primary label, secondary metadata, optional leading media/icon, trailing status/action | Supports fast vertical scanning; not a mini Card wall | Navigation item, checkbox |
| Selectable tile | Selection control/state, content summary, clear target | Represents a choice; selection is not navigation unless explicitly combined | Choice, Card |
| Panel/widget | Heading, content region, optional contextual actions/status | Groups related information or controls; not every section needs a raised panel | Status, chart |
| Data Table | Caption/title, column headers, rows/cells, sorting/filtering, selection, pagination | Compares structured records; not reproduced as unrelated mobile Cards without preserving relationships | Pagination, filter |
| Chart | Title, visual plot, axes/scales/legend or direct labels, annotation, summary/data access | Shows pattern or relationship; does not replace exact values when exact inspection matters | Table, tooltip |
| Badge/status label | Text, optional icon, semantic state | Communicates concise status/count; not an interactive filter by default | Status message |
| Chip/tag | Text, optional icon/remove action, selected state when interactive | Represents filter, attribute, or compact input; not a decorative category bubble | Filter, choice |
| Avatar | Person/entity image, initials/fallback, accessible name in context | Represents a real entity; does not use anonymous scene silhouettes | Profile, list item |
| Media thumbnail | Licensed/generated image, crop metadata, alt/label relationship | Previews content; not a text background | Scene plate, Card |

## Variants

| Variant | Purpose | Visual difference | Behavioral difference |
| --- | --- | --- | --- |
| Editorial Card | Narrative entry with identity image | Portrait or derived crop plus clean text region | Usually one clear destination |
| Utility Card | Compact summary/action | Little or no image, lifted clean surface | May contain a small action set |
| List row | High scanning efficiency | Minimal containment, stable columns | Row link or explicit controls, not both ambiguously |
| Compact Table | Dense expert comparison | Tighter spacing, fixed headers where useful | Keyboard sorting/filtering and horizontal strategy |
| Comfortable Table | General comparison | More row height and whitespace | Same semantics |
| Analytical chart | Data relationship | Clean plot with restrained brand emphasis | Hover/focus/tooltips plus table/summary |
| Status badge | Read-only state | Icon/text/shape; compact | Not focusable unless it opens details |
| Filter chip | Active filter/input | Selected/remove state | Keyboard/touch interactive and announced |

Variants express content/task purpose. Warm, cool, glowing, grainy, immersive, and “Western” are treatment choices, not component variants.

## States

| State | Visual behavior | Interaction behavior | Content behavior |
| --- | --- | --- | --- |
| Default | Clean surface, readable hierarchy, restrained boundary | Static or clearly interactive | Complete title/label and key metadata |
| Hover | One boundary/value change on interactive item | Pointer only | No hidden essential information |
| Focus-visible | Crisp focus on the actionable target | Keyboard access | Accessible name describes destination/action |
| Active/pressed | Brief stable response | Activates once | Content does not jump |
| Selected | Marker/check plus selected surface and programmatic state | Toggle/select according to contract | Selection count/status updates |
| Disabled/unavailable | Readable state and reason where useful | No action | Do not hide critical historical data |
| Loading | Stable layout or labelled progress | Preserve current sort/filter/selection | No fake records or indefinite shimmer |
| Empty | Valid absence with explanation/action | Next path available | Distinguish empty from filtered-zero and failed |
| Error/stale | Message and affected region retained | Retry/refresh/inspect previous data | Timestamp/source/state explicit |

## Density Profile

| Density | Use | Spacing behavior | Prohibited compromise |
| --- | --- | --- | --- |
| Editorial | Hero/story collections | Large scene gap, few Cards, strong negative space | Do not stretch task controls or hide metadata |
| Comfortable | Default product content | Standard 8px cadence and 44/48-unit targets | Do not add atmosphere to every item |
| Compact | Tables, market/operational data, expert grids | Reduced row padding and grouped columns | Never reduce text, focus, touch/keyboard access, or row distinction below requirements |

Density is task-dependent. The identity language’s emptiness applies to hero hierarchy, not to every Table or data dashboard.

## Card And List Rules

- A Card has one clear subject and destination or a small related action set. If it contains independent sections, it is a panel or layout region.
- Do not make the entire Card clickable when it also contains nested controls unless event/focus semantics are unambiguous.
- Place identity imagery in a dedicated media region and text on a clean surface. Never rely on crop-dependent contrast.
- Preserve a consistent title/metadata order across a collection. Use content-driven height unless alignment materially improves comparison.
- Prefer lists for repetitive scanning and Cards for richer heterogeneous summaries. Avoid endless card grids because they look “designed.”

## Table And Chart Rules

- Tables use real headers, captions/descriptions, correct row/column relationships, and locale-aware numeric alignment.
- Sorting controls announce column and direction. Filtering, selection, pagination, loading, and stale state remain explicit.
- On narrow screens, prioritize, pin, scroll with context, or offer a purposeful record-detail layout. Do not silently transpose every row into a Card and lose comparison.
- Charts choose form from the data question. The brand palette is not a categorical data palette.
- Direct-label important series, use redundant shape/pattern, expose exact values, and provide a text summary or data Table where needed.
- Warm/cool may distinguish one emphasis or binary relationship only after CVD and meaning review; never encode many series with grainy tonal variants.
- Plot areas, axes, data marks, labels, and tooltips remain crisp and texture-free.

## Content And Naming Rules

- Titles name the item; metadata follows a stable order and uses explicit labels when values are ambiguous.
- Badges state status in text. Chips use nouns for attributes and clear selected/remove semantics.
- Empty copy distinguishes “No items yet,” “No results for these filters,” and “Couldn’t load items.”
- Dates, times, currency, units, decimal separators, abbreviations, and pluralization follow locale/domain rules.
- Truncation never removes the only distinguishing term; offer full content on focus/expansion where appropriate.
- Avatars do not infer gender or use anonymous fictional silhouettes for real people.

## Token Dependencies

| Part | Required token | Override boundary |
| --- | --- | --- |
| Panel/Card surface | `component.panel.background` | Clean functional surface |
| Panel/Card boundary | `component.panel.border` | May omit if separation is otherwise clear |
| Content padding | `component.panel.padding` | Density may step on semantic scale |
| Primary copy | `semantic.text.primary` | No texture/opacity shortcut |
| Secondary/metadata copy | `semantic.text.secondary`, `semantic.text.muted` | Must meet declared contrast |
| Selection | `component.choice.selected.*` | Check/marker and semantics required |
| Focus | `semantic.focus.ring` | Native equivalent accepted |
| Status | `component.status.*` | Meaning and recovery contracts apply |
| Scene thumbnail | `component.scene.*`, `component.scene-support.*` | Text remains on support surface |
| Chart emphasis | Appropriate semantic/data token defined by domain | Do not use raw brand colours as a data scale |

## Accessibility And Localization

- Use semantic headings, lists, Tables, captions, headers, row/column scopes, links, buttons, and selection controls.
- Interactive Cards expose one clear focus target or explicit internal targets; avoid nested interactive elements.
- Table users can reach sort/filter/select/pagination by keyboard and understand current state without visual position alone.
- Charts provide a meaningful accessible name, summary, exact-value access, keyboard-operable interactions where interactive, and a nonvisual alternative.
- Colour, shape, pattern, label, and programmatic state redundantly encode series/status/selection.
- Support zoom, large text, RTL, window resize, translated labels, local formats, and high contrast without clipping or losing relationships.
- Loading placeholders are hidden or labelled appropriately for assistive technology; avoid high-frequency shimmer and respect reduced motion.
- Media has purpose-based alt text; decorative texture is hidden. Avatars have context-appropriate names outside the image.

## Code And API Contract

```text
ContentItem {
  id: stable item id
  title: required localized string
  hrefOrAction?: exactly one primary behavior
  summary?: localized string
  metadata: ordered labelled values
  media?: licensed asset plus focal/alt metadata
  status?: semantic status
  selected?: boolean
  actions?: small explicit action set
}

DataTable {
  caption: required
  columns: ordered typed column definitions
  rows: keyed records
  sort?: controlled sort state
  selection?: none | single | multiple
  loadingState: idle | loading | refreshing | failed | stale
  pagination?: page or cursor contract
}
```

- Chart APIs require title, question/intent, data, scale/units, series labels, accessible summary, exact-value route, and empty/error states.
- Unsupported: arbitrary `cardStyle`, raw palette array for data, clickable container with hidden nested controls, unlabelled badge, and image-as-text-background.

## Examples And Anti-Patterns

- **Do:** use one atmospheric thumbnail for an editorial Card and place title/metadata on opaque carbon.
- **Do:** keep an expert Table compact while preserving 16px-equivalent text, focus, headers, and keyboard sorting.
- **Do:** pair a highlighted data series with direct label, distinct line style, and a text summary.
- **Avoid:** grainy charts, glowing table rows, orange/cyan-only categories, or every dashboard module as a floating Card.
- **Avoid:** anonymous scene figures as user avatars, status conveyed only by a coloured dot, or skeleton records that look like real data.
- **Avoid:** converting a comparison Table into unrelated Cards on mobile without an alternative comparison path.

## Related Patterns

- Navigation, filtering, pagination, and selection.
- Feedback, empty, loading, stale, and error states.
- Imagery art direction and scene components.
- Perceptual hierarchy and density.
- Domain-specific data patterns.
