"""
ospo :: shared configuration

Single source of truth for phase metadata, step-to-template mappings,
script dependency declarations, and MCP tool assignments.

Imported by task_runner.py and template_builder.py to eliminate duplication.
"""

# ---------------------------------------------------------------------------
# Phase metadata
# ---------------------------------------------------------------------------
PHASES = {
    "oppstrat": {
        "number": 1,
        "title": "Operational Direction & Strategic Foundation",
        "cycle_stage": "Direction",
    },
    "intelepi": {
        "number": 2,
        "title": "Intelligence Collection & Epistemic Filtering",
        "cycle_stage": "Collection",
    },
    "colent": {
        "number": 3,
        "title": "Collation & Entity Resolution",
        "cycle_stage": "Processing",
    },
    "chronrel": {
        "number": 4,
        "title": "Chronological & Relational Processing",
        "cycle_stage": "Processing",
    },
    "hypcog": {
        "number": 5,
        "title": "Hypothesis Reasoning & Cognitive De-biasing",
        "cycle_stage": "Analysis",
    },
    "findis": {
        "number": 6,
        "title": "Final Reporting & Dissemination",
        "cycle_stage": "Dissemination",
    },
}

# ---------------------------------------------------------------------------
# Phase folder names (phase number -> folder)
# ---------------------------------------------------------------------------
PHASE_FOLDERS = {
    1: "oppstrat",
    2: "intelepi",
    3: "colent",
    4: "chronrel",
    5: "hypcog",
    6: "findis",
}

# ---------------------------------------------------------------------------
# Step -> Phase mapping
# ---------------------------------------------------------------------------
STEP_TO_PHASE = {
    1: 1, 2: 1,
    3: 2, 4: 2, 5: 2,
    6: 3, 7: 3, 8: 3,
    9: 4, 10: 4, 11: 4,
    12: 5,
    13: 6, 14: 6, 15: 6,
}

# ---------------------------------------------------------------------------
# Step -> Template mappings (canonical, used by both task_runner and template_builder)
# ---------------------------------------------------------------------------
STEP_TEMPLATES = {
    1: ["research/case-decision-log.md"],
    2: ["research/investigation-strategy.md"],
    3: ["research/source-grading.md"],
    4: ["database/task-log.md"],
    5: ["database/evidence-register.md"],
    6: ["analysis/pole.md"],
    7: ["database/entity-register.md"],
    8: ["database/subject-profiles.md", "research/family-network-research.md", "research/cultural-context.md"],
    9: ["analysis/chronological-matrix.md"],
    10: ["analysis/network-architecture.md"],
    11: ["analysis/verification.md", "analysis/morphological.md"],
    12: ["analysis/ach.md"],
    13: ["working/briefing.md"],
    14: ["working/case-summary.md"],
    15: ["working/findings-memo.md", "working/nim.md", "working/report.md"],
}

# ---------------------------------------------------------------------------
# Step -> Script mappings
# ---------------------------------------------------------------------------
STEP_SCRIPTS = {
    1: [],
    2: [],
    3: ["source_grader.py"],
    4: [],
    5: ["evidence_preservation.py", "content_archiver.py"],
    6: ["entity_resolver.py"],
    7: ["entity_resolver.py"],
    8: ["corporate_intel.py", "domain_intel.py", "username_enum.py", "sanctions_screen.py"],
    9: ["chronological_matrix.py"],
    10: ["network_graph.py"],
    11: ["geolocation.py", "content_archiver.py"],
    12: [],
    13: ["report_generator.py"],
    14: ["report_generator.py"],
    15: ["report_generator.py", "financial_analysis.py"],
}

# ---------------------------------------------------------------------------
# Step -> MCP/Tool mappings
# Thinking Toolkit (TT): use at reasoning impasses, competing framings, strategy decisions
# PSS profiling is optional and deliberately absent from mandatory task gates.
# ---------------------------------------------------------------------------
STEP_MCP_TOOLS = {
    1: [
        "web_search",
        "OSDb (create_investigation, add_entity, save_notebook)",
        "Thinking Toolkit (diagnose - scope framing, competing objectives)",
    ],
    2: [
        "web_search",
        "OSDb (record_grade, register_evidence, save_progress)",
    ],
    3: [
        "web_search",
        "OSDb (record_grade, register_evidence, save_progress)",
    ],
    4: [
        "OSDb (save_progress)",
    ],
    5: [
        "web_search",
        "OSDb (register_evidence, save_progress)",
    ],
    6: [
        "OSDb (add_entity, add_relationship, save_progress)",
    ],
    7: [
        "OSDb (add_entity, search_entities, add_relationship, get_relationships, save_progress)",
    ],
    8: [
        "web_search",
        "web_fetch",
        "OSDb (add_entity, update_entity, add_relationship, save_progress)",
        "Thinking Toolkit (diagnose - use at any reasoning impasse during collection)",
    ],
    9: [
        "OSDb (add_timeline_event, get_timeline, save_progress)",
        "Thinking Toolkit (diagnose - structural implications of timeline gaps and conflicts)",
    ],
    10: [
        "OSDb (get_relationships, add_relationship, save_progress)",
        "Thinking Toolkit (diagnose - interpret centrality patterns and community structure)",
    ],
    11: [
        "web_search",
        "web_fetch",
        "OSDb (add_location, register_evidence, save_progress)",
    ],
    12: [
        "Thinking Toolkit (diagnose - ACH reasoning; call when stuck on hypothesis ranking)",
        "OSDb (save_notebook, save_progress)",
    ],
    13: [
        "OSDb (get_statistics, load_notebook, save_progress)",
    ],
    14: [
        "OSDb (get_statistics, save_progress)",
    ],
    15: [
        "OSDb (get_statistics, close_investigation, save_progress)",
    ],
}

# ---------------------------------------------------------------------------
# Script -> module dependencies (for auto-install)
# ---------------------------------------------------------------------------
SCRIPT_MODULES = {
    "source_grader.py":          ["core"],
    "evidence_preservation.py":  ["archiving"],
    "content_archiver.py":       ["archiving", "social"],
    "entity_resolver.py":        ["sanctions"],
    "corporate_intel.py":        ["corporate"],
    "domain_intel.py":           ["network"],
    "username_enum.py":          ["identity"],
    "sanctions_screen.py":       ["sanctions"],
    "chronological_matrix.py":   ["core"],
    "network_graph.py":          ["graph"],
    "geolocation.py":            ["geo"],
    "report_generator.py":       ["reporting"],
    "financial_analysis.py":     ["core"],
}
