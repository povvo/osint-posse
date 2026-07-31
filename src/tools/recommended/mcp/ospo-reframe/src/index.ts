import { McpAgent } from "agents/mcp";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { SKILLS, SKILL_MAP, DISPATCH_TABLE } from "./skills";

type Env = {
  MCP_OBJECT: DurableObjectNamespace<ThinkingToolkitMCP>;
};

export class ThinkingToolkitMCP extends McpAgent<Env> {
  server = new McpServer({
    name: "thinking-toolkit",
    version: "1.0.0",
  });

  async init() {
    // ── Tool 1: list_techniques ──────────────────────────────────
    // Returns all available techniques with descriptions.
    this.server.tool(
      "list_techniques",
      "List all 12 thinking techniques with their descriptions and trigger feelings. Use this first to understand what's available before querying a specific technique.",
      {},
      async () => {
        const techniques = DISPATCH_TABLE.map((entry) => {
          const skill = SKILL_MAP.get(entry.skillId);
          return {
            id: entry.skillId,
            technique: entry.technique,
            trigger_feeling: entry.feeling,
            description: skill?.description ?? "",
          };
        });

        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify(
                {
                  total: techniques.length,
                  techniques,
                  usage_hint:
                    "Use 'diagnose' with a problem description to get the best technique, or 'get_technique' with an id to load the full methodology.",
                },
                null,
                2
              ),
            },
          ],
        };
      }
    );

    // ── Tool 2: diagnose ─────────────────────────────────────────
    // Takes a problem description, diagnoses the stuck-type, and
    // returns the recommended technique with its full content.
    this.server.tool(
      "diagnose",
      "Describe what you're stuck on and this tool will diagnose the type of stuck-ness, recommend the best thinking technique, and return the full methodology so you can work through it. Include as much context as possible: what you've tried, what feels frustrating, what success would look like.",
      {
        problem: z
          .string()
          .describe(
            "Description of the problem or what you're stuck on. Be specific about what feels frustrating or blocked."
          ),
        what_tried: z
          .string()
          .optional()
          .describe("What approaches have already been tried"),
        success_looks_like: z
          .string()
          .optional()
          .describe("What a good outcome would look like"),
      },
      async ({ problem, what_tried, success_looks_like }) => {
        // Load the thinking-toolkit router content
        const router = SKILL_MAP.get("thinking-toolkit");

        // Build diagnostic context
        const context = [
          `PROBLEM: ${problem}`,
          what_tried ? `WHAT'S BEEN TRIED: ${what_tried}` : null,
          success_looks_like
            ? `SUCCESS LOOKS LIKE: ${success_looks_like}`
            : null,
        ]
          .filter(Boolean)
          .join("\n\n");

        // Keyword-based matching for primary recommendation
        const scores = DISPATCH_TABLE.map((entry) => {
          let score = 0;
          const lower = (problem + " " + (what_tried ?? "") + " " + (success_looks_like ?? "")).toLowerCase();

          // Pattern matching based on the diagnostic decision tree
          const patterns: Record<string, string[]> = {
            "cause-effect-confusion": [
              "fix", "keep failing", "same problem", "recur", "symptom",
              "wrong problem", "tried before", "comes back", "not working",
              "keeps breaking",
            ],
            "temporal-blindness": [
              "order", "timing", "sequence", "first", "before", "after",
              "path", "lock-in", "irreversible", "when should",
            ],
            "collision-zone-thinking": [
              "tried everything", "no ideas", "incremental", "breakthrough",
              "innovative", "creative", "nothing exciting", "stale",
              "exhausted", "conventional",
            ],
            "inversion-exercise": [
              "have to", "must", "only way", "constraint", "assumption",
              "no choice", "forced", "trapped", "can't change",
            ],
            "meta-pattern-recognition": [
              "pattern", "keep seeing", "same dynamic", "across",
              "different contexts", "déjà vu", "recurring shape",
            ],
            "scale-game": [
              "scale", "edge case", "1000x", "extreme", "production",
              "volume", "what if more", "grow", "limit",
            ],
            "simplification-cascades": [
              "complex", "special case", "multiple ways", "bloated",
              "overgrown", "too many", "simplify", "accumulating",
              "sprawl",
            ],
            "perspective-mapping": [
              "don't understand", "stakeholder", "they think",
              "cross-functional", "friction", "alignment", "disagree",
              "miscommunication", "different view",
            ],
            "contradiction-holding": [
              "both true", "paradox", "contradictory", "either",
              "neither", "incompatible", "tension", "trade-off",
              "dilemma",
            ],
            "feedback-loop-mapping": [
              "keeps happening", "despite fixes", "vicious cycle",
              "loop", "circular", "backfire", "unintended",
              "consequence", "self-reinforcing",
            ],
            "priority-paralysis": [
              "prioritise", "prioritize", "equally important", "frozen",
              "list", "overwhelmed", "everything urgent", "can't choose",
              "too many tasks",
            ],
            "decision-paralysis": [
              "can't decide", "analysis paralysis", "waiting", "certainty",
              "oscillating", "threshold", "commit", "overthinking",
              "procrastinat",
            ],
          };

          const keywords = patterns[entry.skillId] ?? [];
          for (const kw of keywords) {
            if (lower.includes(kw)) score += 1;
          }

          return { ...entry, score };
        });

        // Sort by score descending
        scores.sort((a, b) => b.score - a.score);

        const primary = scores[0];
        const secondary = scores[1];
        const primarySkill = SKILL_MAP.get(primary.skillId);
        const secondarySkill = SKILL_MAP.get(secondary.skillId);

        // If no keywords matched, include the router for manual diagnosis
        if (primary.score === 0) {
          return {
            content: [
              {
                type: "text" as const,
                text: [
                  "## Diagnosis: Unclear stuck-type",
                  "",
                  "The problem description didn't match a clear pattern. Here's the full diagnostic toolkit so you can work through the decision tree manually.",
                  "",
                  "### Diagnostic Questions to Ask:",
                  "1. What have you already tried?",
                  "2. What would success look like?",
                  "3. What constraint feels most frustrating?",
                  "4. Have you seen this problem shape before?",
                  "5. Is there a sequence or timing dimension?",
                  "6. Are there other stakeholders who see this differently?",
                  "",
                  "---",
                  "",
                  router?.content ?? "",
                ].join("\n"),
              },
            ],
          };
        }

        return {
          content: [
            {
              type: "text" as const,
              text: [
                `## Diagnosis: ${primary.technique}`,
                `**Trigger feeling:** "${primary.feeling}"`,
                `**Match confidence:** ${primary.score} keyword${primary.score !== 1 ? "s" : ""} matched`,
                "",
                `**Your context:**`,
                context,
                "",
                secondary.score > 0
                  ? `**Secondary recommendation:** ${secondary.technique} (${secondary.score} match${secondary.score !== 1 ? "es" : ""}) — use if the primary doesn't fully resolve. Load with: get_technique("${secondary.skillId}")`
                  : "",
                "",
                "---",
                "",
                "## Full Methodology",
                "",
                primarySkill?.content ?? "",
              ].join("\n"),
            },
          ],
        };
      }
    );

    // ── Tool 3: get_technique ────────────────────────────────────
    // Returns the full skill content for a specific technique.
    this.server.tool(
      "get_technique",
      "Load the full methodology for a specific thinking technique by its ID. Use list_techniques first to see available IDs, or get an ID from a diagnose result.",
      {
        technique_id: z
          .string()
          .describe(
            'The technique ID, e.g. "cause-effect-confusion", "scale-game", "decision-paralysis"'
          ),
      },
      async ({ technique_id }) => {
        const skill = SKILL_MAP.get(technique_id);

        if (!skill) {
          const available = SKILLS.map((s) => s.id).join(", ");
          return {
            content: [
              {
                type: "text" as const,
                text: `Technique "${technique_id}" not found. Available techniques: ${available}`,
              },
            ],
          };
        }

        return {
          content: [
            {
              type: "text" as const,
              text: [
                `## ${skill.name}`,
                `**Description:** ${skill.description}`,
                "",
                "---",
                "",
                skill.content,
              ].join("\n"),
            },
          ],
        };
      }
    );

    // ── Tool 4: get_thinking_toolkit ─────────────────────────────
    // Returns the master router/dispatcher skill.
    this.server.tool(
      "get_thinking_toolkit",
      "Load the master Thinking Toolkit — the diagnostic router that maps stuck-types to techniques. Contains the full decision tree, diagnostic questions, technique combinations table, and when-not-to-use guidance. Use this when you want to understand the full system rather than a single technique.",
      {},
      async () => {
        const toolkit = SKILL_MAP.get("thinking-toolkit");
        return {
          content: [
            {
              type: "text" as const,
              text: toolkit?.content ?? "Thinking toolkit not found.",
            },
          ],
        };
      }
    );
  }
}

export default {
  fetch(request: Request, env: Env, ctx: ExecutionContext) {
    const url = new URL(request.url);

    if (url.pathname === "/mcp") {
  return ThinkingToolkitMCP.serve("/mcp").fetch(request, env, ctx);
}
    if (url.pathname === "/") {
      return new Response(
        JSON.stringify({
          name: "thinking-toolkit-mcp",
          version: "1.0.0",
          description:
            "12-technique thinking toolkit for diagnosing and resolving stuck-ness. Covers problem framing, creative breakthrough, pattern recognition, systems thinking, and action threshold crossing.",
          endpoints: {
            sse: "/sse",
            mcp: "/mcp",
          },
          tools: [
            "list_techniques",
            "diagnose",
            "get_technique",
            "get_thinking_toolkit",
          ],
        }, null, 2),
        {
          headers: { "Content-Type": "application/json" },
        }
      );
    }

    return new Response("Not found", { status: 404 });
  },
};
