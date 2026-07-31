# Platform Tokens

Output path: `tokens/platform-tokens.md`

Platform artifacts preserve semantic intent while adopting native naming, units, typography, focus, motion, and control behavior. The examples below define an equivalence contract, not a requirement to force identical rendering.

## Platform Output Matrix

| Token | Artifact | Web/CSS | iOS | Android | Windows | React Native | Transform |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `semantic.surface.canvas` | Colour | `--ef-surface-canvas` | `EFColor.surfaceCanvas` | `EFTheme.colors.surfaceCanvas` | `EFBrush.SurfaceCanvas` | `tokens.color.surfaceCanvas` | Emit sRGB fallback; allow system forced-colour override |
| `semantic.surface.raised` | Colour | `--ef-surface-raised` | `EFColor.surfaceRaised` | `EFTheme.colors.surfaceRaised` | `EFBrush.SurfaceRaised` | `tokens.color.surfaceRaised` | Preserve functional plane separation, not identical elevation |
| `semantic.text.primary` | Colour | `--ef-text-primary` | `EFColor.textPrimary` | `EFTheme.colors.onSurface` | `EFBrush.TextPrimary` | `tokens.color.textPrimary` | Validate contrast after platform compositing |
| `semantic.text.secondary` | Colour | `--ef-text-secondary` | `EFColor.textSecondary` | `EFTheme.colors.onSurfaceVariant` | `EFBrush.TextSecondary` | `tokens.color.textSecondary` | Do not implement by opacity alone |
| `semantic.action.primary.surface` | Colour | `--ef-action-primary-bg` | `EFColor.actionPrimary` | `EFTheme.colors.primary` | `EFBrush.ActionPrimary` | `tokens.color.actionPrimary` | Platform theme may remap status; retain intent |
| `semantic.action.primary.foreground` | Colour | `--ef-action-primary-fg` | `EFColor.onActionPrimary` | `EFTheme.colors.onPrimary` | `EFBrush.OnActionPrimary` | `tokens.color.onActionPrimary` | Pair generated and contrast-test together |
| `semantic.border.focus` | Focus colour | `--ef-focus-ring` | `EFColor.focusRing` | `EFTheme.colors.focusIndicator` | `SystemControlFocusVisualPrimaryBrush` or `EFBrush.Focus` | `tokens.color.focusRing` | Prefer native focus API; do not draw a glow |
| `semantic.status.error.accent` | Status colour | `--ef-status-error` | `EFColor.statusError` | `EFTheme.colors.error` | System error brush or `EFBrush.StatusError` | `tokens.color.statusError` | Conventional platform error colour may override; icon/copy contract remains |
| `semantic.type.body.family` | Font family | `--ef-font-body` | `EFFont.body` | `EFTypography.bodyLarge.fontFamily` | `EFFontFamily.Body` | `tokens.font.bodyFamily` | Use platform-approved open-aperture family and script fallback |
| `semantic.type.body.size` | Type size | `1rem` baseline | Dynamic Type body metric | `sp`, mapped to body style | Effective-pixel type style with text scaling | Numeric dp-like size with `allowFontScaling` | Never convert rem mechanically into fixed native points |
| `semantic.type.body.weight` | Font weight | `400` | `.regular` | `FontWeight.Normal` | `FontWeights.Normal` | `"400"` | Prevent synthetic weights where possible |
| `semantic.type.body.line` | Line height | Unitless `1.6` | Font-metric-relative line spacing | `lineHeight` in `sp` | Style line-height/effective px | Numeric scaled line height | Validate clipping for fallback scripts and large text |
| `semantic.type.display.size` | Responsive type | CSS `clamp()` | Dynamic Type custom metric with maximum reviewed optically | Compose responsive type style | Adaptive resource/style | Window-width/type-scale mapping | Preserve hierarchy; do not force the web formula |
| `semantic.layout.inline-gap` | Dimension | `0.5rem` or generated px | `8pt` baseline | `8dp` | `8 epx` | `8` | Map 1 design pixel to one platform-independent unit, then review |
| `semantic.layout.control-padding` | Dimension | `12px` baseline | `12pt` baseline | `12dp` baseline | `12 epx` baseline | `12` | Native control defaults may exceed; do not reduce below platform norm |
| `semantic.layout.content-inset` | Dimension | `32px`, responsive | `32pt`, adaptive margins | `32dp`, adaptive window size class | `32 epx`, adaptive layout | `32`, responsive helper | Compact mode may step down; large text may step up |
| `semantic.focus.offset` | Dimension | `4px` outline offset | Native focus treatment or `4pt` custom spacing | Native focus treatment or `4dp` | Native focus visual | Per-platform wrapper | Preserve visible separation from adjacent colours |
| `global.radius.control` | Radius | `4px` | `4pt` | `4dp` | `4 epx` | `4` | Optical equality may require small per-platform correction |
| `global.target.touch` | Target size | Design target `44×44 CSS px`; never below applicable WCAG/platform rules | At least `44×44pt` | At least `48×48dp` | Use native control target and at least the shared 44-unit design target where touch is expected | Branch: `44` iOS, `48` Android | Visible icon can remain 20–24 units; target grows independently |
| `semantic.motion.feedback.duration` | Duration | `120ms` | `0.12s` | `120ms` | `0:0:0.12` | `120` | Respect platform animation-scale and reduced-motion settings |
| `semantic.motion.reveal.duration` | Duration | `240ms` | `0.24s` | `240ms` | `0:0:0.24` | `240` | Native standard may replace if purpose is equivalent |
| `semantic.motion.response.easing` | Easing | `cubic-bezier(0.2,0,0,1)` | `UnitCurve`/timing parameters | `CubicBezierEasing` | `CubicEase` approximation | Easing function | Document curve approximation; do not add spring |
| `semantic.motion.axis.easing` | Easing | `cubic-bezier(0.2,0.75,0.2,1)` | Custom timing curve | Compose cubic bezier | Spline/key-spline approximation | Easing function | Preserve deceleration and directional continuity |
| `semantic.texture.functional` | Media transform | `none` | No texture layer | No texture modifier | No texture brush | No texture overlay | Functional content always clean |
| `semantic.texture.identity.min` | Media transform | Generated raster/CSS overlay outside text | Pre-rendered asset preferred | Pre-rendered asset preferred | Pre-rendered asset preferred | Pre-rendered asset preferred | Generate texture at asset resolution; avoid runtime full-screen noise |
| `semantic.imagery.ratio.master` | Aspect ratio | `aspect-ratio: 3 / 4` | `3:4` media container | `aspectRatio(0.75f)` | `AspectRatio` helper | `aspectRatio: 0.75` | Derived crops use stored focal/recognition metadata |

## Output Artifact Contract

| Platform | Required artifact | Naming | Mode mechanism | Accessibility transform |
| --- | --- | --- | --- | --- |
| Web | CSS custom properties plus typed token JSON | `--ef-{intent}` | `prefers-color-scheme`, explicit theme attribute, forced-colours media query | `prefers-reduced-motion`, `:focus-visible`, zoom/reflow, semantic HTML |
| iOS/iPadOS | Swift colour/font/spacing namespace and asset catalogue colours | `EFColor`, `EFFont`, `EFSpace` | Trait collections and named colour assets | Dynamic Type, Increase Contrast, Reduce Motion, VoiceOver, external keyboard focus |
| Android | Compose theme or XML resources generated from the same graph | `EFTheme`, `ef_*` resources | Night resources or theme state | Font scaling, high contrast where exposed, animation duration scale, TalkBack, keyboard/D-pad focus |
| Windows | WinUI/XAML resource dictionaries and typed helpers | `EFBrush.*`, `EFFont*`, `EFSpace*` | Theme dictionaries and system colours | Text scale, high contrast resource dictionaries, system animation setting, Narrator, visible focus |
| React Native | Typed TypeScript token module with platform selectors only where necessary | `tokens.{family}.{intent}` | Context/provider plus `Appearance` | `AccessibilityInfo`, `allowFontScaling`, per-platform target sizes, visible focus on desktop/web targets |

## Unit And Colour Transform Rules

- **Colour:** keep one canonical perceptual or sRGB value in the token graph and emit platform colour objects. Do not round-trip through platform screenshots. Identity colours may opt into wide gamut only with tested sRGB fallbacks.
- **Typography:** map roles to native text styles before mapping numbers. Preserve user scaling, script fallback, weight, and line-height behavior; a fixed web pixel size is not a native type contract.
- **Space:** CSS px, Apple points, Android dp, Windows effective pixels, and React Native density-independent numbers are related design units, not identical physical measurements.
- **Motion:** convert milliseconds to native duration units and approximate cubic curves explicitly. Native standard motion wins when it communicates the same purpose and respects user settings.
- **Focus:** use native focus visuals where they meet the semantic contract. Custom focus requires a crisp, persistent, high-contrast indicator and must survive forced/high-contrast modes.
- **Media:** pre-render grain, bloom, and chromatic edge effects for performance and deterministic quality. Store focal point, recognition core, and safe-text metadata alongside each asset.

## Platform Rules

- Preserve semantic intent across platform naming differences; identical purpose does not require identical chrome.
- Use native navigation, controls, gestures, dialogs, menus, feedback, permission flows, and back behavior.
- Keep platform-specific exceptions explicit in the transform configuration, not hidden in component code.
- Treat target-size numbers as design targets and verify current platform and accessibility requirements at implementation time.
- Verify font rendering, colour management, image decoding, high contrast, dark/light modes, large text, localization, keyboard order, and reduced motion on real devices.

## Anti-Patterns

- A web-first component rendered unchanged on every platform.
- Fixed px values copied into iOS/Android/Windows typography without native scaling.
- Runtime grain or blur effects that drain battery, destabilize contrast, or render differently by GPU.
- Platform branches that hard-code raw colours instead of repointing semantic resources.
- Custom dialogs, back gestures, focus, or permission screens that discard native expectations to preserve atmosphere.
