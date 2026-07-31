## DOMAIN 1: People Investigation & Entity Research

### Investigation Methodology

People investigation and entity research represents one of the most ethically sensitive OSINT domains, yet exhibits **EMERGING** evidence quality with limited institutional standardisation. The Berkeley Protocol on Digital Open Source Investigations provides the most comprehensive ethical and methodological framework, establishing principles of safety, accuracy, dignity, responsibility, and proportionality. However, this framework addresses human rights investigations specifically and may not fully translate to commercial or law enforcement contexts.

The OSINT intelligence cycle applies universally: Direction (defining research objectives and scope), Collection (gathering information from prioritised sources), Processing (organising and structuring data), Analysis (evaluating reliability and synthesising findings), and Dissemination (producing reports tailored to stakeholder needs). Within people investigation, this cycle must incorporate additional ethical review at each stage to ensure proportionality, purpose limitation, and data minimisation consistent with privacy law.

Professional practice varies significantly by sector. Law enforcement people investigation prioritises evidentiary admissibility, chain of custody documentation, and compliance with investigative powers legislation. Journalistic background research emphasises verification through multiple independent sources, protection of subject dignity, and public interest justification. Corporate due diligence focuses on risk assessment, regulatory compliance (particularly sanctions screening and politically exposed persons identification), and commercial relevance. Academic research requires ethical review board approval, informed consent considerations, and methodology documentation for reproducibility.

### Source Hierarchy

People investigation source hierarchies exhibit professional community variation, but consensus emerges around core tiers:

**Tier 1 - Official Government Records** (highest reliability): Electoral registers, company director registrations, land registry records, professional licensing databases, court judgments, bankruptcy registers. These sources provide legally verified identity information with auditability.

**Tier 2 - Verified Commercial Databases**: Credit reference agency data, corporate registry aggregators (Companies House, OpenCorporates), professional networking platforms with verified credentials (LinkedIn with identity confirmation), news archives from established outlets. Reliability depends on verification protocols and update frequency.

**Tier 3 - Social Media and Self-Published Content**: Personal social media profiles, blogs, forum participation, online reviews. Requires cross-verification as content may be misleading, outdated, or deliberately false. Authentication crucial.

**Tier 4 - Secondary Commentary**: News aggregation sites, gossip columns, unverified user-generated content, anonymous forums. Lowest reliability; useful for hypothesis generation but requires corroboration before inclusion in findings.

**Tier 5 - Data Breach and Leaked Information**: Credential leaks, hacked databases, document dumps. Legal and ethical constraints apply; many jurisdictions prohibit use of unlawfully obtained information regardless of public availability. Commercial OSINT providers explicitly exclude such sources to maintain compliance.

Jurisdictional coverage varies significantly. UK investigators access comprehensive electoral registers and Companies House director information. US investigators utilise extensive court records and property registries but face more limited beneficial ownership transparency. EU investigators must navigate GDPR restrictions on personal data processing.

### Standard Report Structure

No universally adopted standard exists for people investigation reports, representing a **critical gap**. However, analysis of practitioner outputs and professional body guidance reveals common structural elements:

**Executive Summary** (1-2 paragraphs): Subject identity confirmation, investigation scope, key findings summary, significant risk indicators.

**Subject Profile**: Full name and known aliases, date and place of birth (if ascertainable), current and historical addresses, nationality and residency status, family relationships (where relevant to investigation purpose).

**Professional Background**: Employment history from verified sources, professional qualifications and licenses, company directorships and shareholdings, industry affiliations and memberships.

**Financial Indicators**: Property ownership, company ownership structures, known business interests, bankruptcy or insolvency history, sanctions screening results, politically exposed person status.

**Legal History**: Civil litigation (as claimant or defendant), criminal convictions (where legally accessible), regulatory enforcement actions, professional disciplinary proceedings.

**Digital Footprint**: Social media presence analysis, website ownership, domain registrations, online business activities, digital reputation assessment.

**Association Mapping**: Network visualisation showing relationships to other individuals, companies, and organisations. Link analysis showing nature of relationships (familial, commercial, professional).

**Source Registry**: Complete list of sources consulted with URLs, access dates, and reliability ratings. Critical for auditability and verification.

**Caveats and Limitations**: Explicit statement of information not found, sources not accessible, assumptions made, and confidence levels for key findings.

Report tone varies by professional context. Law enforcement reports emphasise factual, neutral language with careful distinction between established facts and inferences. Journalistic reports may incorporate narrative elements whilst maintaining verification standards. Corporate due diligence reports focus on risk assessment and may include recommendation sections.

### Analytical Framework

People investigation analysis centres on **relationship mapping**, **timeline construction**, and **risk assessment**. The lack of standardised analytical frameworks represents another gap, though practitioners converge on common approaches.

**Link Analysis**: Mapping connections between individuals, organisations, and events using network visualisation tools (Maltego, i2 Analyst's Notebook). Analysis identifies direct relationships (family, employment, partnership) and indirect relationships (shared addresses, common associates, overlapping company networks). Clustering techniques reveal hidden networks and potential collusion.

**Timeline Analysis**: Constructing chronological sequences of events, appointments, transactions, and movements. Temporal analysis identifies patterns, contradictions, and critical periods requiring deeper investigation. Cross-referencing timelines from multiple sources reveals inconsistencies requiring resolution.

**Source Triangulation**: Applying the three-source rule where possible — independent corroboration of key facts from three distinct sources before treating as established. When corroboration unavailable, explicit confidence qualifiers applied (e.g., "single source, unverified", "corroborated by two independent sources").

**Contradiction Resolution**: When sources disagree, investigators assess source reliability, recency, and position relative to the fact in question. Primary sources (direct observation) outweigh secondary sources (reportage). Recent sources generally outweigh historical sources unless documenting past states. Explicit notation of unresolved contradictions required rather than arbitrary selection.

**Risk Scoring**: Corporate due diligence commonly applies risk rating frameworks assessing reputational risk, regulatory risk, sanctions risk, and association risk. Scoring remains largely proprietary with limited published methodology. Academic research into risk scoring sparse.

### Key Databases & Tools

**People Search Platforms**: Pipl, Spokeo, PeopleFinders (US-focused), 192.com (UK). Aggregate public records, social media, and commercial data. Reliability variable; verification essential.

**Social Media Intelligence Tools**: Social-Searcher, Hootsuite, Brand24 for monitoring and archival. Maltego Social Transforms for relationship mapping. Platform-native search (Twitter/X Advanced Search, Facebook Graph Search where available).

**Company Registry Services**: OpenCorporates (global aggregator, 200+ million companies), Companies House (UK), SEC EDGAR (US), national registries (variable access).

**Court Records**: PACER (US federal courts), National Archives (historical records), Courtlistener (US case law), BAILII (British and Irish case law), national court websites.

**Professional Licensing Databases**: General Medical Council (UK doctors), Solicitors Regulation Authority (UK solicitors), state bar associations (US lawyers), professional body membership directories.

**Property and Land Registries**: Land Registry (England/Wales), Registers of Scotland, various US county registries, Zoopla/Rightmove for UK property transaction history.

**Sanctions and PEP Screening**: OpenSanctions (consolidates 245 global sources), OFAC SDN List, EU Sanctions List, UN Security Council Sanctions List, World-Check (commercial).

**Archival Tools**: Wayback Machine (Internet Archive), Archive.today, Hunchly (browser extension for evidence collection and chain of custody).

### Quality Criteria & Verification

Quality standards for people investigation remain largely practitioner-driven rather than institutionally codified. The Berkeley Protocol provides the most authoritative framework, establishing six core principles:

**Safety**: Investigations must not place subjects, investigators, or sources at risk of harm. Operational security (OPSEC) protocols protect investigator identity when researching hostile actors. Source protection protocols prevent exposure of confidential informants.

**Accuracy**: Claims require evidential support. Distinguish between established facts, reasonable inferences, and speculation. Apply appropriate confidence qualifiers (confirmed, probable, possible, unconfirmed).

**Dignity**: Subjects retain human rights regardless of alleged wrongdoing. Avoid unnecessary intrusion into private life unrelated to legitimate investigation purpose. Proportionality assessment required: information gathering must be proportionate to investigation objective.

**Responsibility**: Investigators accountable for methodology, findings, and potential harms. Document decision-making process. Maintain audit trail enabling independent verification.

**Transparency**: Methodology must be documentable and reproducible. Sources must be citeable (whilst protecting confidential informants). Limitations and gaps explicitly stated.

**Purpose Limitation**: Data collection limited to information relevant to defined investigation purpose. Function creep (expanding investigation beyond original scope) requires explicit justification.

**Source Reliability Assessment** employs various frameworks. The NATO Admiralty Code rates sources (A = completely reliable to F = unreliable) and information (1 = confirmed to 6 = cannot be judged). The similar 5x5 matrix appears in law enforcement contexts. However, application remains inconsistent across practitioners.

**Verification Protocols** vary by claim type. Identity verification requires government-issued identification cross-referenced with electoral register or similar. Employment claims verified through company confirmation, LinkedIn verification, or professional body membership. Property ownership verified through land registry. Association claims require multiple independent confirmations or documentary evidence (company filings showing shared directorships).

### Failure Modes & Mitigations

**Common Failure Modes**:

1. **Identity Confusion**: Confusing subjects with similar names. **Mitigation**: Require multiple confirming identifiers (date of birth, address, unique reference numbers).

2. **Outdated Information**: Presenting historical information as current. **Mitigation**: Date-stamp all information, explicitly note currency, prioritise recent sources.

3. **Circular Reporting**: Multiple sources reporting the same underlying original source, creating false corroboration. **Mitigation**: Trace claims to primary sources, identify unique sources vs echoes.

4. **Confirmation Bias**: Seeking information confirming pre-existing hypothesis whilst ignoring contradictory evidence. **Mitigation**: Actively seek disconfirming evidence, document contradictions, apply devil's advocate analysis.

5. **Scope Creep**: Investigating beyond proportionate necessity. **Mitigation**: Maintain clear purpose limitation statement, require justification for scope expansion, periodic relevance review.

6. **Privacy Violations**: Collecting personal data without lawful basis. **Mitigation**: GDPR compliance review, purpose limitation enforcement, data minimisation, legal basis documentation.

7. **Source Reliability Failures**: Treating unreliable sources as authoritative. **Mitigation**: Mandatory source rating, three-source rule for critical claims, explicit reliability qualifiers.

8. **Inadequate Documentation**: Insufficient audit trail preventing verification. **Mitigation**: Real-time evidence collection (Hunchly), source registry maintenance, screenshot archival with metadata.

### Template Design Notes

People investigation templates must incorporate:

- **Mandatory ethical review checkpoint** before investigation commencement assessing proportionality, purpose limitation, and legal basis under privacy law.
- **Source hierarchy hardcoded** with Tier 1-5 structure and reliability ratings.
- **Verification protocols** specifying minimum corroboration requirements for different claim types (identity, employment, associations, property).
- **Output structure** with mandatory sections: Subject Profile, Professional Background, Financial Indicators, Legal History, Association Mapping, Source Registry, Caveats.
- **Quality checklist** ensuring Berkeley Protocol principles addressed: safety, accuracy, dignity, responsibility, transparency, purpose limitation.
- **Customisable elements**: Investigation scope (personal vs professional focus), depth of association mapping (1-degree vs 2-degree connections), jurisdiction (determines accessible records).

### Evidence Quality Assessment

**EMERGING** — Limited institutional standardisation. Berkeley Protocol provides ethical framework but lacks detailed methodological specification. UK College of Policing guidance needed but not found. ACFE standards focus on fraud investigation specifically. Gap in comprehensive people investigation methodology guidance. Practitioner-driven approaches dominant but lack formal validation.
***