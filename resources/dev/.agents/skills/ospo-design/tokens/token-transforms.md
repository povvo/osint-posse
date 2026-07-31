# Token Transforms

Output path: `tokens/token-transforms.md`

The canonical token graph is platform-neutral and reference-based. Transforms validate and expand that graph into deterministic platform artifacts; they do not invent values or semantic names.

## Canonical Shape

Use a W3C Design Tokens-style object where practical:

```json
{
  "semantic": {
    "surface": {
      "canvas": {
        "$type": "color",
        "$value": "{alias.palette.field.deep}",
        "$description": "Primary application field"
      }
    }
  }
}
```

Permitted metadata includes description, deprecation, usage, mode applicability, platform exception, and accessibility constraint. Proof labels, source identifiers, file paths, and provenance do not belong in the design-use token graph.

## Transform Pipeline

| Input | Transform | Output | Consumer | Constraint |
| --- | --- | --- | --- | --- |
| Canonical JSON | Schema and type validation | Validated token graph | All builds | Reject unknown `$type`, missing `$value`, malformed colours, and invalid units |
| Token references | Dependency-graph resolution | Acyclic reference graph | All builds | Primitive → global → alias → semantic → component only |
| Base semantic graph | Light/dark mode expansion | Mode-specific semantic graph | Theme runtime | Dark remains default identity; light is explicit translation |
| Colour-mode graph | High-contrast override | System-colour graph | Accessibility mode | High contrast wins over ordinary light/dark values |
| Motion graph | Reduced-motion override | Reduced-motion graph | Accessibility mode | Replace travel/ambient motion with cuts, short fades, and state cues |
| Semantic colour token | OKLCH validation plus sRGB fallback serialization | CSS variable and platform colour resource | Web/native/RN | Flag out-of-gamut conversion and excessive rounding |
| `dimension` in rem/px | Unit transform by platform role | CSS rem/px, iOS pt, Android dp/sp, Windows epx, RN number | Platform artifact | Typography maps through native roles; do not mechanically convert body rem to fixed points |
| `duration` in ms | Unit serialization | CSS ms, Swift seconds, Android ms, XAML timespan, RN number | Motion implementation | Preserve purpose and user-setting override |
| `cubicBezier` | Curve serialization/approximation | CSS curve, native timing curve, spline/key-spline | Motion implementation | Record approximation error; never substitute a spring |
| Dot-separated token path | Naming normalization | kebab CSS, lower_snake resources, Pascal/camel typed names | Platform artifact | Maintain a reversible name map |
| Semantic token | Component-binding generation | `component.*` defaults | Design/code/AI consumers | Component bindings may reference semantics only |
| Media ratio/focal token | Crop-metadata transform | JSON sidecar or asset-catalog metadata | Image pipeline | Preserve recognition core and safe-text zone |
| Normalized texture value | Resolution-aware media transform | Grain amplitude and scale parameters | Offline image renderer | Scale by delivered resolution; mask functional content |
| Platform-independent target | Platform design-target transform | 44 CSS px/pt, 48dp Android, native Windows/RN equivalent | Control implementation | Apply stricter current platform requirement when present |
| Fully expanded graph | Contrast, reference, and drift validation | Build report and artifact manifest | CI/review | Fail on unresolved references, invalid pairs, or hard-coded component values |

## Required Output Artifacts

| Platform | Output artifact | Naming transform | Value transform |
| --- | --- | --- | --- |
| Canonical | `tokens.canonical.json` | Preserve dot paths | References unresolved; W3C-style types |
| Web | `tokens.css` and optional `tokens.json` | `semantic.surface.canvas` → `--ef-surface-canvas` | CSS colours, rem/px, ms, cubic-bezier; mode selectors/media queries |
| iOS | `EFTokens.generated.swift` plus colour assets | Path → Swift nested/static camel case | Colour objects, points, seconds, native type-role mapping |
| Android | `ef_tokens.xml` and/or `EFTokens.generated.kt` | Path → `ef_lower_snake` or Compose camel case | ARGB/resources, dp/sp, ms, Compose easing |
| Windows | `EFTokens.generated.xaml` plus typed helpers | Path → `EF.Pascal.Path` | Brushes, effective pixels, timespans, theme dictionaries |
| React Native | `tokens.generated.ts` | Path → typed camel-case object | Colour strings, density-independent numbers, ms, platform selectors |
| Media | `media-recipes.generated.json` | Preserve semantic media names | Ratios, focal vectors, area constraints, grain/blur formulas |
| Manifest | `token-build-manifest.json` | Stable artifact names | Input hash, transform version, mode/platform, warnings, output hash |

These names describe the required build outputs; generated files are downstream artifacts and are not handwritten.

## Transform Order And Precedence

1. Parse canonical values and metadata.
2. Validate type, name, and layer ownership.
3. Build the reference graph and reject cycles.
4. Resolve global and alias materials into semantic intent.
5. Apply colour mode.
6. Apply contrast preference, which overrides colour mode where necessary.
7. Apply motion preference independently.
8. Bind component tokens to the effective semantic graph.
9. Perform platform naming and unit transforms.
10. Serialize artifacts, run contrast/reference/drift checks, and write a manifest.

Runtime user preference chooses among prevalidated artifacts or theme branches; runtime code must not calculate brand colours ad hoc.

## Colour Transform

- Preserve OKLCH as the canonical perceptual description when the target supports it and emit an sRGB hex fallback.
- Gamut-map by reducing chroma before changing lightness or hue. Record the mapped value in the build report.
- Do not derive opacity-based text colours from opaque primitives; create or map a semantic foreground and validate the composited result.
- Round sRGB channels only at final serialization and ensure two distinct semantic roles do not collapse into the same output accidentally.
- Generate contrast test pairs from actual component bindings, not from all possible colours.

## Unit Transform

- Spacing and radius: one design unit maps to CSS px, Apple pt, Android dp, Windows effective px, and React Native density-independent number, subject to optical review.
- Type: CSS uses rem and user zoom; native uses semantic text roles and user scaling. The token value is a target relationship, not an instruction to disable scaling.
- Media blur at runtime size:

  `scaled_blur = clamp(1px, reference_blur × short_edge / 736, 96px)`

  Use this only in an offline or deterministic media pipeline. Review at 1× and 2× output.
- Grain amplitude remains a luminance fraction; spatial frequency scales with output resolution. Do not scale opacity and frequency by the same factor.
- Touch targets map to the platform design target and may grow with input modality or accessibility preference.

## Naming Transform

| Canonical | CSS | Swift/Compose/RN | Android XML | Windows |
| --- | --- | --- | --- | --- |
| `semantic.text.primary` | `--ef-text-primary` | `textPrimary` | `ef_text_primary` | `EF.Text.Primary` |
| `component.button.primary.background` | `--ef-button-primary-background` | `buttonPrimaryBackground` | `ef_button_primary_background` | `EF.Button.Primary.Background` |

Every artifact ships a reversible name map so diagnostics can report the canonical token.

## Validation Requirements

- No unresolved references, cycles, type mismatches, or layer inversions.
- No component token may resolve directly from a primitive, global, or alias path.
- All light/dark/high-contrast/reduced-motion branches generate successfully.
- Required text, focus, icon, and boundary pairs meet their declared contrast behavior after compositing.
- Generated platform artifacts resolve to the same canonical graph hash and transform version.
- Media recipes keep the dark majority, scarce convergence peak, resolution-aware texture, and clean information mask.

## Anti-Patterns

- Editing generated platform artifacts by hand.
- Using different canonical JSON per platform or theme.
- Resolving aliases at design time and copying raw values into components.
- Runtime colour arithmetic, opacity-based disabled text, or unrecorded native exceptions.
- Mechanical rem-to-point conversion, cubic-curve-to-spring substitution, or fixed blur at every resolution.
- A build that succeeds with warnings for missing references, mode branches, or contrast-critical pairs.
