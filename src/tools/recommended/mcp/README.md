# Recommended MCP services

`ospo-db` is the 26-tool persistent investigation database. Its source lives
under [`src/database/ospo-db`](../../../database/ospo-db).

## Deploy ospo-db

The database Worker has no unauthenticated one-click deployment. From
`src/database/ospo-db`, authenticate Wrangler and run `./setup.sh`.
The script creates or selects the exact D1 database, applies its schema,
installs a generated bearer secret, deploys, and writes a private connector
configuration. See the
[`ospo-db` README](../../../database/ospo-db/README.md) for migration, backup,
authentication, and rollback details.

---

## Tools (26)

| Domain | Tools |
|---|---|
| Investigation | \`create_investigation\`, \`list_investigations\`, \`load_investigation\`, \`close_investigation\`, \`update_investigation\`, \`delete_investigation\` |
| Entities | \`add_entity\`, \`search_entities\`, \`update_entity\`, \`delete_entity\` |
| Relationships | \`add_relationship\`, \`get_relationships\`, \`update_relationship\`, \`delete_relationship\`, \`search_relationships\`, \`get_neighbors\` |
| Source Grading | \`record_grade\` |
| Timeline | \`add_timeline_event\`, \`get_timeline\` |
| Progress | \`save_progress\`, \`load_progress\` |
| Notebook | \`save_notebook\`, \`load_notebook\` |
| Evidence | \`register_evidence\` |
| Geo | \`add_location\` |
| Statistics | \`get_statistics\` |



## ospo-pigeon-profile

**Psychological Profiling Toolkit** — a 16-framework cognitive surrogate construction system, deployed as a Cloudflare Workers MCP server.


## What it does

Provides structured psychological profiling through 16 peer-reviewed frameworks, accessible as MCP tools. Claude loads the relevant framework on demand, constructs a cognitive surrogate of the subject, and uses it to inform analysis, communication strategy, or investigative reasoning.

## Tools

| Tool | Purpose |
|------|---------|
| `list_frameworks` | List all 16 frameworks with descriptions and trigger conditions |
| `get_framework` | Load the full methodology for a specific framework by ID |
| `get_profiling_toolkit` | Load the master orchestration router that maps profile questions to frameworks |
| `assess` | Submit evidence for assessment against the current profile state |

## Stack

- Cloudflare Workers (runtime)
- `@modelcontextprotocol/sdk` (MCP protocol)
- TypeScript
- Wrangler (deployment)

## Development

```bash
npm install
npm run dev      # local dev server
npm run deploy   # deploy to Cloudflare
```



# Thinking Toolkit

*Twelve structured techniques for diagnosing and resolving stuck-ness. code, strategy, narrative, life.*

Every discipline has its version of the same silence. The developer stares at a function that passes every test and breaks every deployment. The strategist holds two market reports that contradict each other with equal authority. The writer sits with a draft that is competent, coherent, and completely dead on the page. The founder refreshes the same three browser tabs, toggling between options that feel identical in weight and consequence.

The block is never the absence of thought. It is the wrong *shape* of thought applied to the problem at hand. A sequencing failure diagnosed as a creativity failure. A contradiction mistaken for a decision. A feedback loop treated as a one-time incident.

This toolkit does not think for you, human or model, it makes no difference. It thinks *about* your thinking. It identifies the structural failure in how you are approaching the problem, hands you the precise instrument for that species of stuck-ness, and steps back. The rest is yours.

---

### The Instruments

| Tool | What It Does |
|------|-------------|
| `diagnose` | Describe the shape of what has you pinned — the frustration, the circularity, the thing that will not yield. The toolkit reads the wound, identifies the type, and returns the full methodology for the technique most likely to break the impasse. |
| `get_technique` | You already know the name of what ails you. Load the complete methodology by ID — constraints, phases, examples, output format — and get to work. |
| `list_techniques` | Survey the full armoury. Twelve techniques, each with the trigger feeling that tells you when to reach for it. |
| `get_thinking_toolkit` | Load the master diagnostic router — the decision tree, the combination matrix, the contraindications. The architecture behind the armoury. |

---

### The Twelve Techniques

| Technique | The Feeling That Calls It |
|-----------|--------------------------|
| **Cause-Effect Confusion** | *"Am I solving the right problem?"* — The fix keeps failing because the diagnosis is wrong. You are treating symptoms while the disease sits undisturbed beneath them. |
| **Temporal Blindness** | *"Does the order matter?"* — Sequence is load-bearing and nobody has tested it. A before B produces a different world than B before A, and the difference is not academic. |
| **Collision-Zone Thinking** | *"I've tried everything obvious"* — The conventional approaches lie exhausted on the floor. Time to force two unrelated domains together and see what ignites at the point of contact. |
| **Inversion Exercise** | *"It has to be done this way"* — An assumption has gone unquestioned so long it feels like gravity. Flip it. Watch what collapses. Watch what stands. |
| **Meta-Pattern Recognition** | *"I keep seeing this pattern"* — The same dynamic surfaces across three separate domains. That is not coincidence. That is a principle wearing different coats, and it has something to tell you. |
| **Scale Game** | *"Will this hold at the edges?"* — Test it at a thousand times the size. Test it at one-thousandth. The extremes expose what normal operation conceals, every time. |
| **Simplification Cascades** | *"It keeps getting more complex"* — Somewhere in the tangle is a single insight that, if true, eliminates three moving parts at once. Find it, and the complexity confesses. |
| **Perspective Mapping** | *"Why don't they understand?"* — They do understand. They understand *differently*. Model their mind instead of projecting yours onto it. |
| **Contradiction Holding** | *"Both of these seem true"* — They are. The premature urge to collapse to one side destroys the insight that only lives in the tension between them. Hold both. See what emerges. |
| **Feedback Loop Mapping** | *"Why does this keep happening?"* — Because the solution is feeding the problem. Map the circle. Find the point where the output re-enters the input and starts the whole disaster again. |
| **Priority Paralysis** | *"Everything feels equally important"* — It is not. But the ranking function has flatlined, and every task exerts the same gravitational pull. Restart the hierarchy. |
| **Decision Paralysis** | *"I can't cross the threshold"* — The cost of not deciding has already exceeded the cost of deciding wrong. You do not need more information. You need architecture for action. |

---
