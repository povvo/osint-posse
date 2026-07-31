# Voice, Tone, And Microcopy

Output path: `foundations/voice-tone-microcopy.md`

## Voice Identity

- **Personality:** spare, observant, grounded, and humane. The voice notices what matters and leaves decorative atmosphere to the image.
- **Authority level:** calm competence. It states facts, limits, consequences, and next steps without swagger or institutional distance.
- **Warmth level:** restrained but present through respect, acknowledgement, and useful recovery—not through exclamation marks or forced friendliness.
- **Formality:** plain professional language, contractions allowed, technical terms defined at first use.
- **Humour boundary:** no humour in errors, consent, permissions, safety, identity, accessibility, loss, payment, or destructive actions. Elsewhere, wit may be dry and rare, never a genre impersonation.
- **Task versus atmosphere:** task copy is explicit. Editorial headlines may be more evocative, but they cannot replace labels, instructions, or status.

## Tone By Context

- **Default:** concise and concrete. Name the object and action: “Open project,” not “Venture onward.”
- **Onboarding:** orient, show one meaningful first step, and explain unfamiliar terms. Avoid mythic language that makes the product harder to understand.
- **Error:** neutral, specific, and recovery-led. Say what failed, what was preserved, and what the user can do.
- **Success:** quiet and factual. Confirm the completed object or state and offer the next useful action.
- **Warning:** direct about risk, scope, and reversibility. Do not dramatize or soften material consequences.
- **Empty state:** explain why the area is empty and give a primary action; avoid loneliness, abandonment, or danger metaphors.
- **High-stakes flow:** maximum clarity, complete consequences, visible alternatives, and no stylistic ambiguity.
- **Editorial moment:** short, sensory, and unresolved may be appropriate in a title or caption, provided context follows in plain language.

## Microcopy Grammar

- **Verb style:** active, concrete, and transitive when possible: “Save draft,” “Share report,” “Remove access.”
- **Sentence length:** aim for `8–18` words in controls and feedback; split instructions above roughly `25` words.
- **Label style:** sentence case, familiar noun or verb, no terminal punctuation for short labels, no unexplained abbreviations.
- **Help text style:** answer the likely question at the point of need. State constraints before submission, not only after an error.
- **CTA construction:** verb plus object. Distinguish actions precisely: “Delete file” and “Remove from folder” are not interchangeable.
- **Pronouns:** use “you” for actions and choices, “we” only when the organisation is actually acting, and “I” only when quoting a user-controlled statement.
- **Numbers and dates:** use locale-aware formats, explicit units, and unambiguous time zones where consequences depend on them.

## Feedback Copy

| Situation | Required content | Example pattern |
| --- | --- | --- |
| Loading | Task name and, when useful, progress or duration | “Uploading 3 files… 42%” |
| Delayed | What continues, whether the user can leave, and a cancel/background option | “This is taking longer than usual. You can leave this page; we’ll keep working.” |
| Recovery | Problem, preserved state, and specific remedy | “We couldn’t save the title. Your other changes are safe. Try again.” |
| Retry | Name the exact action being repeated | “Retry upload” |
| Confirmation | Resulting state and affected object | “Report saved as a draft.” |
| Undo | Reversible result, scope, and available window where relevant | “Access removed. Undo” |
| Warning | Risk, scope, reversibility, and safer alternative | “Deleting this folder removes 18 items. This can’t be undone.” |
| Escalation | What support needs, what data will be shared, and next expectation | “Contact support and include error code E104. We won’t attach your document.” |

Never display invented certainty. If the system does not know whether an operation completed, say so and provide a verification path.

## Sound And Haptic Language

- **Sound role:** off by default and functional only—time-sensitive alert, media control, or explicit confirmation when visual attention may be elsewhere. No ambient wind, fire, hoofbeat, weapon, or “frontier” sound effects.
- **Haptic role:** platform-standard light selection, medium consequential confirmation, and error patterns. Do not invent continuous or atmospheric vibration.
- **Silence rule:** routine navigation, hover, reading, scrolling, loading imagery, and decorative scene transitions remain silent.
- **Accessibility alternative:** every sound and haptic event has a simultaneous visual and semantic state. Caption spoken content, expose volume/mute controls, respect device settings, and never require hearing or vibration to complete a task.

## Localization

- **Idioms to avoid:** frontier metaphors, dialect spelling, “shoot,” “pull the trigger,” “circle the wagons,” “wild west,” “spirit animal,” “tribe,” “powwow,” journey clichés, and location-specific humour.
- **Text expansion:** allow at least 35% expansion for labels, flexible height for messages, and responsive reflow for scripts with different metrics.
- **Cultural tone risks:** anonymous figures, weapons, land, migration, Indigenous-coded forms, and colonial narratives can carry real histories. Do not turn them into casual copy metaphors.
- **Plain-language rule:** use the most familiar accurate word, define necessary jargon, and target a general reading level appropriate to the audience and legal context.
- **Grammar:** avoid concatenating sentence fragments or relying on word order that fails in other languages. Use complete localizable strings with variables described.
- **Names and identity:** preserve diacritics, chosen names, and user-provided capitalization. Do not infer gender from name, image, or role.

## Accessibility Obligations

- Web copy and interaction should meet WCAG 2.2 at the claimed conformance level; target platform guidance may be stricter.
- Error messages identify the field or scope in text and are programmatically associated with the relevant control.
- Status messages are announced without unexpectedly moving focus unless immediate action is required.
- Link text makes sense out of context; avoid repeated “Learn more” when destinations differ.
- Instructions do not depend only on colour, shape, sound, location, or gesture.
- User-facing time limits explain duration, warning, extension, and preservation behavior.

## Translation Rules

1. Write the literal task message first.
2. Remove redundant adjectives, idioms, bravado, and faux-poetic genre language.
3. Add the object, scope, state, or consequence the user needs.
4. Add recovery or next action when the state is not final.
5. Check accessible name, programmatic association, localization, and reading order.
6. Use atmospheric language only in optional editorial copy after the functional meaning is complete.

## Anti-Patterns

- Faux-Western dialogue, cowboy slang, “wanted” language, weapon metaphors, or historical role-play in functional copy.
- Cryptic one-word labels, poetic errors, vague confirmations, passive blame, or cheerful failure.
- Exclamation-heavy success messages, forced humour, gender assumptions, or anthropomorphising the system to hide uncertainty.
- “Something went wrong” without scope or recovery; “Are you sure?” without consequence.
- Sound or haptics as atmosphere, repeated vibration, uncaptioned audio, or inaccessible transient feedback.
- Protecting a terse voice by omitting consent, safety, privacy, billing, or recovery information.
