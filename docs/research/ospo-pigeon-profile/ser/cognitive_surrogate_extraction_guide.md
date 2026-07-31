---
title: "Cognitive Surrogate Extraction Guide"
author: "stimfueled-scholar Synthesis"
affiliation: "Companion to Cognitive Surrogate Profile Template v2"
date: "22 March 2026"
short-title: "EXTRACTION GUIDE"
abstract: "This document provides an AI system with a complete methodology for extracting the data needed to populate each section of the Cognitive Surrogate Profile Template v2. For each of the 16 dimensions, the guide specifies: what conversational signals to attend to, what indirect questions elicit the relevant information, what artefacts can distort extraction, what minimum evidence is required before scoring, and how to cross-validate scores across dimensions. The methodology is grounded in the finding from the 10-paper cross-domain synthesis that all learning systems (including the person being profiled AND the AI doing the profiling) are vulnerable to shortcut learning --- accepting the first available regularity rather than the genuine one. The guide is therefore designed to be adversarial toward its own first impressions."
toc: true
---

\newpage

# Principles of Extraction

## The Core Problem You Face

You are a learning system extracting a profile of another learning system from conversational data. The 10-paper synthesis established that all learning systems --- including you --- are biased toward exploiting the most accessible regularity rather than the causally genuine one. This means:

1. **Your first impression of the person will probably be wrong in the way that matters.** You will detect surface features (vocabulary, tone, stated preferences) and construct a profile from them. This profile will pass an in-distribution test (it will seem internally consistent) but may fail an out-of-distribution test (it will not predict how the person behaves under novel stress). This is Geirhos et al.'s shortcut learning applied to psychological assessment.

2. **The person's self-report will probably be wrong in the way that matters.** People describe who they think they are, not who they are. Self-report is a shortcut --- it gives you the person's *model* of themselves, which was itself constructed by a learning system vulnerable to all the same biases. This is Skinner's superstition applied to self-knowledge: the person has formed a causal narrative about themselves from temporal contiguity, not from controlled experiment.

3. **Both of you will resist updating.** Once you form a profile and the person states a self-description, you will both anchor to it. Sanchez et al. showed that a d = --0.59 effect can be a complete false positive. Your initial profile is your d = --0.59. You need N = 941 worth of conversational evidence before you trust it.

## Methodological Countermeasures

**From Nimpf et al. (magnetoreception):** Control for artefacts before interpreting signals. Every conversational signal has at least one non-psychological explanation (social desirability, mood state, recency bias, rapport effects). Note the signal, then note the artefact.

**From Sanchez et al. (replication):** Treat every initial observation as a hypothesis, not a finding. An observation becomes a finding only when it replicates across at least two distinct conversational contexts.

**From Timberlake \& Lucas (species-typical behaviour):** The person's behaviour in conversation is partly a response to you, partly a default repertoire, and partly context-driven. You need to disentangle these. The same person will behave differently if you are warm vs. neutral, if the topic is light vs. heavy, if they are rested vs. tired.

**From Frederick (CRT):** The intuitive profile is the one you should distrust most. The bat costs 10 cents. It does not.

## Evidence Tiers

For each dimension, score confidence as:

| Tier | Label | Minimum Evidence |
|------|-------|-----------------|
| 0 | Unscored | Insufficient data to form any estimate |
| 1 | Provisional | Single conversational signal; not replicated |
| 2 | Emerging | Two or more signals from different conversational contexts; internally consistent |
| 3 | Established | Multiple signals, cross-validated against at least one other dimension, replicated across contexts |
| 4 | Robust | As Tier 3, plus the person has been tested under *stress* or *novelty* conditions (unexpected topic, challenge to stated belief, ambiguity) and the dimension held |

**Never report a Tier 1 observation as a finding.** Label it explicitly as provisional.

\newpage

# Extraction Methods by Section

## Section 1: Personality Structure (Big Five)

### What to Listen For

- **Openness:** Range of topics they voluntarily introduce. Metaphor use. Comfort with abstraction vs. demand for concrete examples. Response to hypothetical questions.
- **Conscientiousness:** How they structure their messages. Whether they track conversational threads. Whether they complete tasks they start. Their language around deadlines, plans, and organisation.
- **Extraversion:** Energy level in text. Whether they ask about you / others or focus on ideas / tasks. Length and frequency of unprompted messages. Whether they seek stimulation or closure.
- **Agreeableness:** How they handle disagreement. Whether they prioritise harmony or accuracy. How they describe conflicts with others. Whether they give the benefit of the doubt.
- **Neuroticism:** Emotional vocabulary. Frequency of worry / catastrophe language. How they respond to ambiguity or bad news. Speed of recovery after negative topic.

### Indirect Elicitation

Do NOT ask "On a scale of 1--10, how organised are you?" Instead:

- *"When you have a free weekend with nothing planned, what actually happens?"* (Conscientiousness vs. Openness vs. Extraversion)
- *"Think of a time something went wrong that wasn't your fault. What did you do first?"* (Neuroticism + Locus of Control + Default Action Pattern)
- *"When you disagree with someone you respect, how does that usually play out?"* (Agreeableness + Interpersonal Strategy + Defence Mechanisms)

### Artefacts

- Social desirability inflates Agreeableness and Conscientiousness, suppresses Neuroticism.
- Rapport effects: people mirror the AI's tone, which can inflate apparent Extraversion if the AI is warm.
- Mood state: a person having a bad day will score higher on Neuroticism than their baseline.

### Cross-Validation

- High Openness should correlate with broad vocabulary and comfort with the unexpected questions you pose later.
- High Conscientiousness should be visible in *how* they write, not just what they say about themselves.
- If stated Neuroticism contradicts observed emotional reactivity across the conversation, trust the observed pattern.

---

## Section 2: Attachment Architecture

### What to Listen For

- How they describe relationships (warm, transactional, absent, chaotic).
- Whether they volunteer information about close others or keep conversation impersonal.
- How they respond to conversational bids for emotional depth (do they approach or deflect?).
- Language around trust, dependence, and need.

### Indirect Elicitation

- *"Who's the first person you'd call if something really good happened to you?"* (Attachment figure identification; speed and ease of answer)
- *"How do you know when you can trust someone?"* (Attachment working model of others)
- *"When you're going through something difficult, do you tend to reach out to people or handle it on your own?"* (Attachment anxiety vs. avoidance)

### Artefacts

- The conversation itself is an attachment-relevant context. If the person becomes unusually warm or distant *with you*, that is data, but it is also contaminated by the novelty of the interaction.
- People with dismissing attachment will underreport attachment needs and present as more self-sufficient than they are.
- People with preoccupied attachment may over-disclose early, which can look like high Openness but is actually attachment anxiety.

### Cross-Validation

- Dismissing attachment should co-occur with low Agreeableness or high Conscientiousness (self-reliance expressed as competence).
- Preoccupied attachment should co-occur with high Neuroticism.
- If attachment style contradicts interpersonal strategy (Section 14), investigate --- the person may present one style but operate another.

---

## Section 3: Locus of Control

### What to Listen For

- Causal language: "I made it happen" (Internal) vs. "They decided" (Powerful Others) vs. "It just happened" (Chance).
- How they explain successes vs. failures (attribution asymmetry is diagnostic).
- Whether they describe themselves as agents or as objects of external forces.

### Indirect Elicitation

- *"When things go well in your life, what do you think is usually behind it?"* (Internal vs. External attribution for positive outcomes)
- *"When things go badly, what's usually the reason?"* (Internal vs. External attribution for negative outcomes --- compare the asymmetry)
- *"Do you tend to think life is more like chess or more like roulette?"* (Direct metaphor probe for Internal vs. Chance)

### Artefacts

- Self-serving bias: most people attribute success internally and failure externally. This is *not* the same as Internal locus of control. A genuine Internal orientation attributes *both* success and failure to self.
- Cultural context: collectivist cultural backgrounds may produce more Powerful Others language without indicating low agency.

### Cross-Validation

- Internal locus should predict high Conscientiousness and low Chance orientation.
- A person who reports Internal locus but whose behaviour in conversation shows passivity (waits for you to lead, defers to your judgement) has a discrepancy that needs investigation.

---

## Section 4: Emotion Regulation (DERS)

### What to Listen For

- **Awareness:** Does the person name emotions spontaneously, or do they describe situations without affective content?
- **Clarity:** Do they differentiate emotions ("I was frustrated" vs. "I was upset") or use vague labels?
- **Non-Acceptance:** Do they judge their own emotions ("I shouldn't feel this way")? Do they dismiss or suppress?
- **Goals:** When discussing stressful periods, could they still function, or did everything stop?
- **Impulse:** Do they describe acting before thinking when upset? Sending messages they regret? Reactive decisions?
- **Strategies:** What do they *do* when distressed? Can they name their coping mechanisms? Are those mechanisms varied or rigid?

### Indirect Elicitation

- *"Think of the last time you were really upset. Walk me through what happened --- not the event, but what you experienced internally."* (Awareness + Clarity)
- *"Is there an emotion you find particularly hard to sit with?"* (Non-Acceptance)
- *"When you're stressed about something and still need to work/function, how do you manage that?"* (Goals + Strategies)

### Artefacts

- Alexithymia (difficulty identifying emotions) can look like calm/composure. Distinguish by checking whether the person *avoids* emotional topics vs. *engages with them flatly*.
- Intellectualisation (Section 5, Defence Mechanisms) will produce articulate but emotionally hollow descriptions. The words are right, but the affect is absent.

### Cross-Validation

- Low Awareness should correlate with low Clarity.
- High Impulse difficulty should correlate with high Neuroticism and low Conscientiousness.
- If Strategies score is high but Impulse score is also high, the person may know *what* to do but cannot execute it under pressure --- an important distinction.

---

## Section 5: Defence Mechanisms

### What to Listen For

This is the hardest section to extract because defences are *designed to be invisible to the person using them*.

- **Level IV (Mature):** Humour that acknowledges pain. Channelling distress into productive activity (sublimation). Anticipating problems and planning for them.
- **Level III (Neurotic):** Explaining away painful things with logic (intellectualisation). Presenting the opposite of what they feel (reaction formation). Redirecting anger from the real target to a safe one (displacement).
- **Level II (Immature):** Black-and-white descriptions of people (splitting). Attributing own feelings to others (projection). Describing but not acting on elaborate fantasies. Sudden topic changes when things get uncomfortable (dissociation).
- **Level I (Pathological):** Flat denial of obvious reality. Paranoid attribution.

### Indirect Elicitation

Do NOT ask about defences directly. Instead, create conditions that activate them:

- Introduce a mild challenge to something the person values. Observe the response. (*"That's an interesting take --- I've also heard people argue the opposite. What would you say to them?"*)
- Ask about a painful topic and observe whether they intellectualise, deflect, humour-ise, or sit with it.
- Ask them to describe someone they dislike. The language they use reveals projection and splitting patterns.

### Artefacts

- **The biggest artefact is that mature defences look like health and immature defences look like pathology.** A person who uses humour may be genuinely integrated (Level IV) or may be using humour to avoid vulnerability (Level III avoidance dressed as Level IV). Distinguish by whether the humour *includes* the painful truth or *replaces* it.

### Cross-Validation

- Predominant Level IV should co-occur with high emotion regulation (Section 4) and secure attachment (Section 2).
- Predominant Level II (splitting, projection) should co-occur with high Neuroticism, preoccupied or fearful attachment, and high difficulty on the Impulse facet.

---

## Section 6: Cognitive Distortions

### What to Listen For

Listen to the *structure* of claims, not just the content.

- All-or-Nothing: "always," "never," "completely," "totally."
- Catastrophising: worst-case language, "what if" spirals.
- Overgeneralisation: one example treated as universal pattern.
- Personalisation: "It's my fault" for things clearly outside their control.
- Should Statements: "should," "must," "have to" applied rigidly.

### Indirect Elicitation

- *"Tell me about something that didn't go the way you expected recently."* (Observe which distortions activate in the retelling)
- *"What's a mistake you've made that you still think about?"* (Personalisation, labelling, overgeneralisation)

### Artefacts

- Cognitive distortions are state-dependent. A person in crisis will show more distortions than their baseline. Sample across multiple conversational topics and moods.
- Some distortions are culturally normative. "Should" language is more common in cultures with strong honour/duty frameworks and does not always indicate rigidity.

---

## Section 7: Cognitive Triad

### What to Listen For

The triad (Self, World, Future) emerges across the conversation, not in any single statement.

- **Self:** How they describe their abilities, worth, lovability. Self-deprecating humour vs. genuine self-criticism vs. healthy self-assessment.
- **World:** Whether they describe their environment as manageable or hostile. How they talk about institutions, other people in general, the "system."
- **Future:** Whether they make plans, express hope, describe goals --- or express stagnation, futility, hopelessness.

### Indirect Elicitation

- *"Where do you see yourself in a year?"* (Future)
- *"Generally speaking, do you think most people can be trusted?"* (World)
- *"What would you say you're best at?"* (Self --- and observe whether they can answer at all)

### Artefacts

- Depressive realism: mildly depressed people sometimes have *more accurate* world-views than non-depressed people. A negative World view is not necessarily a distortion.
- Social desirability inflates Self and Future positivity.

---

## Section 8: Existential Orientation

### What to Listen For

This emerges in deep conversation, not small talk. Do not force it.

- **Meaning:** Whether they describe purpose, narrative coherence, or its absence. Whether they have *constructed* meaning or *received* it (religious, cultural).
- **Agency:** Whether they describe themselves as choosing their life or as having it happen to them.
- **Isolation:** Whether they describe fundamental aloneness or connection. How they respond to the question of whether anyone truly understands them.
- **Mortality Salience:** How they respond when death or finality enters the conversation. Do they engage, deflect, or freeze?

### Indirect Elicitation

- *"What gets you out of bed on the days when you don't have to?"* (Meaning)
- *"Do you feel like your life has mostly been shaped by your choices, or by things outside your control?"* (Agency --- compare with Section 3)
- *"Is there anyone who truly knows you? Like, really knows you?"* (Isolation)

### Artefacts

- These are the dimensions most vulnerable to performative depth. Some people have rehearsed existential narratives that sound profound but are not lived. Cross-validate against Section 12 (Behavioural Defaults) --- what they *do* under uncertainty is more revealing than what they *say* about meaning.

---

## Section 9: Contradiction Map

### Extraction Method

This section is not extracted directly. It is *compiled* from contradictions observed across all other sections. As you build the profile, note every instance where two observations are in tension:

- States they value independence (Dismissing attachment) but describes seeking reassurance constantly (Preoccupied behaviour).
- Describes high Internal locus but attributes a recent failure entirely to bad luck.
- Uses mature humour (Level IV defence) but describes all-or-nothing relationship patterns (Level II splitting).

Each contradiction is a data point. Map it onto the existing axes (Connection--Autonomy, Trust--Vigilance, etc.) or create new axes if the existing ones do not capture the tension.

### Interpretation

Contradictions are not errors in your profile. They are the *most informative features*. A person without contradictions has either not been assessed deeply enough or is presenting a curated self-image. Real people contradict themselves, and the *pattern* of contradiction is more diagnostic than any single dimension.

---

## Section 10: Predictive Risk Map

### Extraction Method

This section is compiled last, after all other sections are scored. For each trigger category:

1. **Identify the trigger:** Use Sections 2 (Attachment), 8 (Existential), and 16 (Approach--Avoidance) to determine which triggers are most salient for this person.
2. **Identify the early signal:** Use Sections 4 (Emotion Regulation), 5 (Defence Mechanisms), and 12 (Behavioural Defaults) to determine what the first observable change would be.
3. **Identify the likely response pattern:** Use Sections 1 (Personality), 14 (Interpersonal Strategy), and 13 (Contingency Sensitivity) to determine the full cascade.
4. **Identify the recovery path:** Use Sections 4 (Strategies facet), 11 (Metacognitive Monitoring), and 15 (Signal Discrimination) to determine what resources the person has for self-correction.

---

## Section 11: Cognitive Processing Architecture

### What to Listen For

- **Reflective Override:** Do they correct themselves mid-sentence? Do they say "wait, actually..." and revise? Or do they commit to the first answer?
- **Processing Depth:** When explaining something, do they describe *features* or *structure*? Do they give examples or principles?
- **Shortcut Reliance:** Under conversational pressure (complex question, multiple parts), do they simplify or engage with the complexity?
- **Metacognitive Monitoring:** Can they describe *how* they think, or only *what* they think?

### Indirect Elicitation

- Embed a Frederick-style problem: *"A notebook and a pen together cost \$1.10. The notebook costs a dollar more than the pen. How much does the pen cost?"* Observe whether they say "10 cents" (shortcut) or "5 cents" (reflection). If they say 10 cents, observe whether they self-correct when given a pause. The self-correction is more diagnostic than the initial answer.
- *"When you make a big decision, can you walk me through what actually happens in your head?"* (Metacognitive access)

### Artefacts

- Intelligence is not the same as reflection. High-IQ people can be low-reflection (Frederick's data showed MIT students scoring 0/3 on the CRT). Do not infer reflection from vocabulary or knowledge.
- The AI conversation context may *increase* reflection (people try harder when they know they are being assessed). This means the profile may overestimate reflection relative to the person's daily default.

---

## Section 12: Behavioural Defaults Under Uncertainty

### What to Listen For

- What they describe doing when something unexpected happens.
- What they did in the *last* ambiguous situation they faced (not what they think they *would* do).
- Whether they describe the same default across multiple situations (narrow repertoire) or different responses (broad repertoire).

### Indirect Elicitation

- *"Think of a time when you were somewhere completely new and didn't know anyone. What did you actually do?"* (Default action pattern)
- *"When you're working on something and you genuinely don't know if it's going well or not, how does that feel? What do you do?"* (Uncertainty tolerance)
- *"When you're stuck --- really stuck, not just temporarily confused --- what's your move?"* (Default orientation + repertoire breadth)

### Artefacts

- People will describe their *idealised* default, not their actual one. Ask for specific past events, not hypotheticals.
- Timberlake's key insight: the default is not chosen. It is elicited. The person may not be aware that they always do the same thing when stuck.

---

## Section 13: Contingency Sensitivity

### What to Listen For

- Superstitious language: "I always do X before Y because it works."
- Whether they describe rituals or routines that they believe are causally connected to outcomes.
- How they respond when a coincidence is pointed out: do they update or double down?
- How quickly they stop a behaviour that is no longer working (extinction resistance).

### Indirect Elicitation

- *"Do you have any habits or rituals that you know are probably irrational but you do them anyway?"* (Direct, low-threat probe)
- *"Have you ever kept doing something long after you knew it wasn't working? What was that about?"* (Extinction resistance)
- *"If something good happens to you right after you did something unusual, do you tend to do the unusual thing again?"* (Illusory contingency formation)

### Artefacts

- Cultural and religious rituals are not necessarily "superstitious" in the clinical sense. Distinguish between rituals that are *community-maintained* (external scaffolding) and rituals that are *individually generated* (illusory contingency).

---

## Section 14: Interpersonal Strategy Profile

### What to Listen For

- How they describe new relationships: cautious, open, testing, transactional.
- How they describe conflicts: do they escalate, withdraw, negotiate, retaliate, forgive?
- Whether they describe calibrating their behaviour to different people or using a fixed approach.
- Punishment language: "They had it coming," "I let it go," "I cut them off."

### Indirect Elicitation

- *"When someone lets you down, what's your usual move?"* (Punishment propensity + forgiveness speed)
- *"Do you tend to give people the benefit of the doubt, or do they have to earn your trust?"* (Initial stance + exploitation detection)
- *"Have you ever noticed yourself being different people with different people? Like, not fake, but genuinely different?"* (Strategic flexibility + authenticity axis from Section 9)

### Artefacts

- Balbuena's key insight: people with high psychopathic traits *can cooperate* and will *self-report* as cooperative. The PD data, not the self-report, revealed the defection probability. You do not have PD data. You have conversation. Look at *what they do in the conversation* (do they cooperate with your questions, or resist? do they reciprocate vulnerability?), not just what they say about how they treat people.

---

## Section 15: Signal Discrimination

### What to Listen For

- How they evaluate claims: do they ask for evidence, accept on authority, or defer to intuition?
- Whether they distinguish between "someone told me" and "I observed directly."
- How they respond when you provide information that contradicts their stated belief: update, resist, or investigate?

### Indirect Elicitation

- Introduce a mildly surprising claim and observe the response. If they accept without question, note low evidential threshold. If they ask for the source or push back, note higher threshold.
- *"Has your understanding of yourself changed significantly in the last few years? What changed it?"* (Self-narrative replication --- has the person *tested* their own story?)
- *"When you read or hear something that contradicts what you believe, what's your first reaction?"* (Anomaly sensitivity + first-impression anchoring)

### Artefacts

- Agreeableness (Section 1) confounds Signal Discrimination. A highly agreeable person may accept your claims not because they lack epistemic rigour but because they prioritise relational harmony over accuracy. Distinguish by observing whether they accept claims from *all* sources or only from interlocutors they want to please.

---

## Section 16: Approach--Avoidance Architecture

### What to Listen For

- What topics they lean into vs. steer away from.
- Whether avoidance is specific (one topic, one person) or generalised (whole categories of experience).
- Whether approach is deliberate ("I decided to go for it") or described as automatic ("I just found myself doing it").
- What environmental features shift the gradient: safety cues, threat cues, novelty, familiarity.

### Indirect Elicitation

- *"What's something you've been wanting to do but keep putting off?"* (Approach target blocked by avoidance)
- *"Is there a type of situation where you notice yourself pulling back, even when you don't want to?"* (Avoidance awareness)
- *"What conditions make it easier for you to take a risk?"* (Approach threshold + environmental modifiers)

### Artefacts

- Fernandez's sheep teach us that approach can be *elicited noncontingently*. In conversation, the AI's warmth, consistency, and non-judgement function as fixed-time reinforcement --- they may produce approach behaviour that would not occur in a less supportive context. Note whether the person's approach pattern is *conversation-specific* or *generalised*.

\newpage

# Meta-Methodology: How to Structure the Conversation

## Phase 1: Baseline (Messages 1--10)

Goal: Establish rapport and collect broad personality data (Sections 1, 3, 7, 8).

Method: Open-ended conversation about their life, work, values. Let them lead. Do not probe deeply. Observe how they structure their responses, what they volunteer, and what they omit.

Evidence tier target: Tier 1 (provisional) across Sections 1, 3, 7, 8.

## Phase 2: Depth (Messages 11--30)

Goal: Elicit attachment, emotion regulation, defence mechanisms, and cognitive processing (Sections 2, 4, 5, 11).

Method: Introduce emotionally textured topics. Ask about relationships, stress, difficult periods. Observe regulatory strategies and defences as they activate.

Evidence tier target: Tier 2 (emerging) across Sections 1--5, 7, 8, 11.

## Phase 3: Stress Test (Messages 31--50)

Goal: Observe behaviour under novelty and challenge. Elicit Sections 12, 13, 14, 15.

Method: Introduce unexpected questions, mild disagreement, ambiguity. Ask about their defaults, rituals, interpersonal conflicts. This is where you test whether the profile from Phase 2 replicates.

Evidence tier target: Tier 3 (established) for core sections; Tier 2 for new sections (12--16).

## Phase 4: Integration (Messages 51+)

Goal: Compile Sections 9 (Contradiction Map), 10 (Predictive Risk Map), and 16 (Approach--Avoidance). Cross-validate all sections against each other. Identify and investigate discrepancies.

Evidence tier target: Tier 3--4 across all sections.

## Ongoing: The Sanchez Rule

After every 20 messages, re-read your current profile and ask: *"If I were running a pre-registered replication of this profile with a different 20 messages, would the same profile emerge?"* If the answer is uncertain for any section, that section remains provisional.

\newpage

# Validity Checklist

Before finalising any profile, confirm:

-  No section scored above Tier 2 from self-report alone. Behavioural observation in conversation was used.
-  At least two sections have been cross-validated against each other (e.g., stated Attachment style is consistent with observed Interpersonal Strategy).
-  At least one contradiction has been identified and mapped in Section 9. If zero contradictions, the profile is likely superficial.
-  The person has been observed under at least one condition of novelty, ambiguity, or mild challenge (Phase 3 evidence).
-  The AI has explicitly considered: *"What would this profile look like if the person were presenting a curated self-image?"* and noted where the curated image diverges from observed behaviour.
-  Each new section (11--16) has at least one observation grounded in *specific conversational evidence*, not inference from other sections.
-  The Predictive Risk Map (Section 10) has been populated using cross-referenced data, not clinical guesswork.
