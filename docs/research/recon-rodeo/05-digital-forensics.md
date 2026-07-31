## DOMAIN 5: Digital Forensics & Technical Intelligence

### Investigation Methodology

Digital forensics and technical infrastructure investigation using OSINT exhibits **MODERATE** evidence quality with strong technical practitioner methodologies but limited institutional standardisation outside specialised cybersecurity frameworks.

The MITRE ATT&CK framework provides the most comprehensive methodological structure, particularly for reconnaissance tactics (T1590-T1599 in Enterprise matrix). Reconnaissance tactics include: Active Scanning (T1595), Search Open Websites/Domains (T1593), Search Open Technical Databases (T1596), Phishing for Information (T1598 — but outside pure OSINT scope), and Search Victim-Owned Websites (T1594).

Technical OSINT investigation types include: **domain analysis** (investigating domain ownership, history, relationships), **infrastructure mapping** (identifying servers, networks, services, relationships), **certificate analysis** (using certificate transparency logs to find related domains), **attribution** (linking infrastructure to threat actors or organisations), **reconnaissance analysis** (understanding adversary information gathering), and **exposure assessment** (identifying vulnerable or misconfigured systems).

The intelligence cycle applies with technical-specific adaptations. **Direction** defines whether investigation focuses on threat actor attribution, security posture assessment, digital supply chain analysis, or infrastructure mapping. **Collection** uses passive DNS, certificate transparency logs, WHOIS records, port scanning engines (Shodan, Censys), BGP data, and web archives. **Processing** structures data into infrastructure graphs, timeline reconstructions, and change detection. **Analysis** applies clustering (related infrastructure), anomaly detection (unusual configurations), and pattern recognition (infrastructure reuse revealing attribution). **Dissemination** produces technical reports, indicator lists, or threat intelligence feeds.

Professional community variation appears less pronounced than in other domains. Cybersecurity researchers, threat intelligence analysts, law enforcement digital investigators, and penetration testers share substantially overlapping methodologies. Divergence appears mainly in operational constraints (active vs passive techniques, legal authority) rather than fundamental methodology.

### Source Hierarchy

Technical OSINT source hierarchies prioritise technical authoritative sources:

**Tier 1 - DNS and Network Infrastructure Registries**: Authoritative DNS records (queried directly from name servers), WHOIS data from registry operators (not third-party aggregators), Regional Internet Registries (RIPE, ARIN, APNIC, LACNIC, AFRINIC) for IP allocation data, BGP routing data from RouteViews or RIPE RIS. Highest technical reliability.

**Tier 2 - Certificate Transparency Logs**: Public logs of all SSL/TLS certificates (crt.sh, Censys, Certificate Transparency project). Cryptographically authenticated, cannot be retroactively removed. Reveals domain relationships through Subject Alternative Names (SANs).

**Tier 3 - Passive DNS and Historical Data**: SecurityTrails, PassiveTotal, RiskIQ. Aggregates historical DNS resolutions revealing infrastructure changes over time. Reliability depends on data collection coverage and temporal granularity.

**Tier 4 - Internet-Wide Scanning Services**: Shodan (internet-connected device search), Censys (certificate and host data), BinaryEdge (attack surface monitoring), ZoomEye (cyberspace search). Active scanning of public IP space. Reliability high for current state but requires ongoing updates to track changes.

**Tier 5 - Web Archives**: Wayback Machine (Internet Archive), Archive.today. Historical website content, structure, and linked resources. Reliability for content accurate but may miss dynamically loaded content or ephemeral resources.

**Tier 6 - Code Repositories and Paste Sites**: GitHub, GitLab, Bitbucket for code, configuration files, exposed credentials. Pastebin and similar for leaked credentials or configurations. Requires verification — may contain false information or honeypots.

**Tier 7 - Threat Intelligence Sharing Platforms**: VirusTotal (malware and URL scanning), AlienVault OTX (open threat exchange), MISP (malware information sharing), Hybrid Analysis (malware sandbox). Community-contributed intelligence with variable quality. Higher-reputation contributors more reliable.

**Tier 8 - Public Vulnerability Databases**: CVE (Common Vulnerabilities and Exposures), NVD (National Vulnerability Database), vendor security advisories. Authoritative for vulnerability information but identification in wild infrastructure requires scanning or passive observation.

Data recency critical in technical OSINT. Infrastructure changes rapidly (domain reassignment, service reconfigurations, certificate renewals). Date-stamping essential. Historical data valuable for attribution (infrastructure reuse patterns) but current state requires fresh collection.

### Standard Report Structure

Technical OSINT report structures vary by investigation type:

**Domain Analysis Report**:
- Executive Summary: Domain identity, investigation scope, key findings, attribution confidence, risk assessment
- Domain Profile: Domain name, registrar, registration date, expiration date, update history, WHOIS data (registrant if accessible, privacy service if used), name servers, DNS records (A, AAAA, MX, TXT, NS, CNAME)
- Infrastructure: IP addresses (current and historical), hosting provider, ASN, geolocation, reverse DNS, shared hosting neighbours (other domains on same IP)
- Certificate Analysis: Current SSL/TLS certificate, issuer, validity period, Subject Alternative Names (related domains), historical certificates, self-signed vs CA-issued
- Website Analysis: Technology stack (web server, CMS, frameworks, JavaScript libraries identified via Wappalyzer or BuiltWith), content analysis, external resources (CDNs, analytics, third-party scripts), historical changes (Wayback Machine)
- Email Infrastructure: MX records, SPF/DKIM/DMARC policies, email security posture
- Related Infrastructure: Domains sharing IP, certificates, name servers, or registrant, infrastructure clusters suggesting common ownership
- Risk Assessment: Malicious indicators (malware hosting, phishing, C2 infrastructure), vulnerability exposure, misconfiguration detection
- Timeline: Key infrastructure changes, registration events, content modifications
- Attribution Assessment: Infrastructure patterns consistent with known actors, unique identifiers, confidence level
- Source Documentation: Tools used, query timestamps, methodology

**Infrastructure Attribution Report**:
- Executive Summary: Infrastructure summary, attributed actor/organisation, confidence assessment, supporting evidence summary
- Infrastructure Inventory: Domains, IP addresses, certificates, ASNs, hosting providers
- Attribution Evidence: Infrastructure reuse (domains/IPs previously attributed to same actor), unique fingerprints (unusual configurations, custom certificates, distinctive web server responses), temporal patterns (operational times, update schedules), resource overlap (shared name servers, registrars, hosting), linguistic/cultural indicators (language in code comments, time zone patterns)
- Alternative Hypotheses: Other potential attributions considered, evidence for/against each
- Confidence Assessment: High (multiple unique indicators, no contradictory evidence), Moderate (pattern consistent but not unique, some ambiguity), Low (limited evidence, significant ambiguity)
- Recommendations: Monitoring strategy, indicator list for detection
- Source Documentation

**Exposure Assessment Report** (security posture):
- Executive Summary: Organisation assessed, exposure summary, critical findings, risk rating
- Methodology: Tools used, scope (domains/IP ranges assessed), date of assessment
- Domain Inventory: Legitimate domains, subdomain enumeration results, abandoned/forgotten subdomains
- Service Exposure: Open ports and services identified (via Shodan/Censys), service versions, known vulnerabilities
- Certificate Issues: Expired certificates, self-signed certificates on production, weak cryptography
- DNS Misconfigurations: Missing SPF/DMARC, wildcard DNS, dangling DNS (domains pointing to uncontrolled infrastructure)
- Leaked Credentials: Findings from breach databases, paste site monitoring
- Cloud Exposure: Misconfigured S3 buckets, exposed cloud databases, cloud infrastructure enumeration
- Risk Prioritisation: Critical (immediate exploitation risk), High (significant risk, needs patching), Medium (moderate risk), Low (minor issues)
- Recommendations: Remediation priorities, monitoring suggestions

All technical reports must clearly distinguish between current state and historical observations, explicitly date all findings, and note limitations (tools used, scope, access constraints).

### Analytical Framework

Technical OSINT analysis employs several frameworks:

**Infrastructure Clustering**: Grouping related infrastructure through shared characteristics: **IP clustering** (domains resolving to same IP or IP range), **certificate clustering** (domains sharing certificates or appearing in SANs together), **name server clustering** (domains sharing authoritative name servers), **registrar/registrant clustering** (domains registered through same service or entity), **ASN clustering** (resources within same autonomous system), **hosting provider clustering** (domains/IPs with same hosting provider). Clustering reveals infrastructure under common control even when ownership obscured.

**Temporal Analysis**: Examining infrastructure changes over time: **registration patterns** (bulk domain registrations suggesting campaigns), **DNS changes** (infrastructure rotation, failover configurations), **certificate lifecycle** (renewal patterns, expiration suggesting abandonment), **content modifications** (website changes tracked via Wayback Machine), **operational time patterns** (update times suggesting operator time zones). Temporal patterns aid attribution and campaign tracking.

**Technology Fingerprinting**: Identifying software, versions, and configurations: **web server identification** (Apache, nginx, IIS) and version, **CMS detection** (WordPress, Joomla, Drupal), **framework identification** (React, Angular, Django), **analytical and tracking services** (Google Analytics, Facebook Pixel), **CDN usage** (Cloudflare, Akamai), **hosting provider indicators**. Technology stack reveals operational capabilities, potential vulnerabilities, and sometimes attribution clues.

**Attribution Analysis** (from MITRE ATT&CK and threat intelligence practice): Building attribution through: **infrastructure reuse** (threat actors reusing domains/IPs across campaigns), **operational security failures** (exposed emails, usernames, real names in certificates or WHOIS), **timing patterns** (operational hours suggesting geography), **linguistic indicators** (language in error messages, code comments), **victimology** (target selection patterns), **TTP consistency** (techniques, tactics, procedures matching known actors), **resource overlap** (shared infrastructure with previously attributed operations). Attribution confidence must be explicit and qualified.

**Adversary Reconnaissance Reconstruction**: Analysing attacker information gathering through logs, honeypots, and passive observation. MITRE ATT&CK reconnaissance tactics framework: Active Scanning (port scans, vulnerability scans), Search Open Websites/Domains (target website reconnaissance), Search Open Technical Databases (DNS, WHOIS, certificate databases), Gather Victim Identity Information (employee names, email formats). Understanding adversary reconnaissance informs defensive priorities.

**Certificate Transparency Analysis**: Leveraging CT logs for: **subdomain discovery** (finding all subdomains for a target domain through historical and current certificates), **infrastructure mapping** (identifying related domains through SAN analysis), **phishing detection** (domains mimicking legitimate brands with similar names), **timeline reconstruction** (certificate issuance dates revealing infrastructure provisioning).

### Key Databases & Tools

**DNS and WHOIS**:
- dig, nslookup (command-line DNS queries)
- WhoisXML API, who.is (WHOIS lookups)
- SecurityTrails (historical DNS and WHOIS)
- PassiveTotal, RiskIQ (passive DNS)
- DNSDumpster (domain reconnaissance)
- Reverse WHOIS (finding related domains)

**Internet Scanning Platforms**:
- Shodan (internet-connected device search, 400+ ports)
- Censys (certificate and host database, research-focused)
- BinaryEdge (attack surface monitoring)
- ZoomEye (cyberspace search engine)
- Criminal IP (infrastructure scanner)

**Certificate Transparency**:
- crt.sh (certificate search, comprehensive CT log coverage)
- Censys Certificates
- SSLMate (CT monitoring and alerting)
- Facebook CT monitoring

**IP and ASN Analysis**:
- bgp.he.net (BGP routing and ASN lookup)
- IPinfo.io, ip-api (IP geolocation and ASN)
- RIPE Stat (RIPE region IP/ASN analysis)
- GreyNoise (identifying internet scanners)

**Web Analysis**:
- Wayback Machine (Internet Archive, historical websites)
- BuiltWith, Wappalyzer (technology identification)
- Netcraft (web server analysis, site reports)
- URLscan.io (URL analysis and screenshots)
- PhishTank (phishing URL database)

**Subdomain Enumeration**:
- Sublist3r (subdomain discovery)
- Amass (OWASP, comprehensive subdomain enumeration)
- Certificate transparency logs (via crt.sh)
- DNS brute-forcing (dnsenum, fierce)

**Threat Intelligence Platforms**:
- VirusTotal (malware and URL scanning)
- AlienVault OTX (open threat exchange)
- Hybrid Analysis (malware sandbox)
- AbuseIPDB (IP reputation)
- URLhaus (malware URL database)

**Network Analysis**:
- Maltego (relationship mapping, extensive transforms)
- SpiderFoot (automated OSINT collection)
- Recon-ng (reconnaissance framework)
- theHarvester (email, subdomain, name gathering)

### Quality Criteria & Verification

Quality standards for technical OSINT derive primarily from cybersecurity research practices and threat intelligence frameworks:

**Data Currency**: Technical infrastructure changes frequently. All findings must be date-stamped. Historical data valuable for attribution but current state requires fresh queries. Currency requirements vary by data type: DNS records (query within 24 hours for current state), WHOIS (changes infrequent but note registration/update dates), certificates (note validity period), web content (archive historical, note access date).

**Source Authentication**: Verify queries return data from authoritative sources: DNS queries from authoritative name servers (not cached/recursive), WHOIS from registry operators (not third-party aggregators where possible), certificate data from CT logs (cryptographically verifiable), BGP data from RouteViews/RIPE RIS (authoritative routing data).

**Passive vs Active Techniques**: Distinguish between passive (querying existing databases, CT logs, passive DNS) and active techniques (port scanning, web requests to target). Passive techniques leave no traces on target infrastructure. Active techniques potentially detectable and may constitute unauthorised access in some jurisdictions. Legal and ethical implications require explicit consideration. Threat intelligence and security research commonly use passive techniques exclusively.

**Attribution Confidence Framework** (adapted from threat intelligence practice):
- **High Confidence**: Multiple unique technical fingerprints, infrastructure reuse with previously confirmed attribution, operational security failure exposing actor identity, multiple independent indicators consistent with single actor
- **Moderate Confidence**: Technical patterns consistent with known actor but not unique, timing patterns consistent with suspected actor, some infrastructure overlap with previous operations, plausible alternative explanations exist
- **Low Confidence**: Limited technical indicators, patterns common across multiple actors, significant ambiguity, insufficient evidence for firm conclusion
- **No Assessment**: Insufficient evidence to attribute

**Indicator Quality Ratings** (for threat intelligence):
- **High Quality**: Indicator directly linked to malicious activity, low false positive rate, specific to particular threat actor/campaign
- **Medium Quality**: Indicator associated with malicious activity but may appear in legitimate contexts, moderate false positive rate, distinguishes between limited set of actors
- **Low Quality**: Indicator appears in both malicious and legitimate contexts, high false positive rate, generic infrastructure used by many actors

**Documentation Standards**: Reproducible methodology essential. Document: exact queries used, tools and versions, query timestamps, source databases accessed, any API keys or access methods. Enable peer verification. Screenshot evidence for ephemeral resources. Wayback Machine or archive.today for web content preservation.

### Failure Modes & Mitigations

**Common Failure Modes**:

1. **Stale Data**: Treating historical infrastructure data as current state. **Mitigation**: Fresh queries for current state, explicit date stamping, comparison of historical and current data to detect changes.

2. **Shared Infrastructure Misattribution**: Attributing all domains on shared hosting (shared IP, shared certificate) to single actor when multiple unrelated entities share infrastructure. **Mitigation**: Additional clustering signals beyond IP/certificate sharing, verification of shared ownership through WHOIS or content analysis, explicit confidence qualifiers.

3. **CDN/Proxy Masking**: Identifying CDN edge server (Cloudflare, Akamai) as origin server, missing actual origin infrastructure. **Mitigation**: Historical DNS data from before CDN adoption, certificate analysis revealing origin server, scanning non-HTTP ports, subdomain enumeration finding non-CDN-protected resources.

4. **Privacy Service Opacity**: WHOIS privacy services (Domains by Proxy, WhoisGuard) obscuring registrant information. **Mitigation**: Historical WHOIS before privacy adoption, related domain analysis revealing registrant patterns, certificate email addresses (sometimes), leak databases for registrant information.

5. **Certificate Misinterpretation**: Misunderstanding certificate meaning, particularly treating "example.com" in certificate as confirming legitimacy when certificate may be self-signed, expired, or obtained fraudulently. **Mitigation**: Certificate validation (issuer trustworthiness, validity period, chain verification), comparison with legitimate certificates for same organisation, CT log analysis for anomalous certificates.

6. **Attribution Overconfidence**: Treating circumstantial evidence as definitive attribution. **Mitigation**: Explicit confidence framework, consideration of alternative hypotheses, peer review for attribution claims, avoiding attribution based on single indicator.

7. **Legal Boundary Violations**: Active scanning crossing into unauthorised access, particularly when scanning systems without clear public exposure. **Mitigation**: Limit to passive techniques or use scanning services (Shodan, Censys) aggregating legally obtained data, legal review for grey areas, explicit scope limitations.

8. **Tool Over-Reliance**: Treating automated tool output as complete without manual verification. **Mitigation**: Manual verification of critical findings, understanding tool methodologies and limitations, cross-tool verification for material claims.

### Template Design Notes

Technical OSINT templates must incorporate:

- **Investigation type selection** (domain analysis vs infrastructure attribution vs exposure assessment vs threat actor reconnaissance reconstruction) determining scope and tools.
- **Passive-first requirement** defaulting to passive techniques (CT logs, passive DNS, WHOIS, Shodan/Censys) unless active scanning explicitly justified and legally authorised.
- **Clustering methodology** hardcoding infrastructure relationship analysis (IP, certificate, name server, ASN, registrar clustering).
- **Attribution framework** with explicit confidence levels (high/moderate/low/no assessment) and alternative hypothesis consideration.
- **Currency protocols** specifying maximum data age for different resource types (DNS, WHOIS, certificates, content).
- **Output structure** varying by type: domain analysis emphasises comprehensive domain profile, attribution reports emphasise evidence synthesis and confidence assessment, exposure assessments emphasise risk prioritisation.
- **Quality checklist**: data currency verified, source authenticity confirmed, passive/active techniques distinguished, attribution confidence explicit, alternative hypotheses considered, legal constraints respected, methodology documented.
- **MITRE ATT&CK mapping** for reconnaissance techniques observed or employed.

### Evidence Quality Assessment

**MODERATE** — Strong technical practitioner methodologies from cybersecurity research community. MITRE ATT&CK provides comprehensive framework for reconnaissance tactics. SANS training materials (SEC487, SEC497, SEC587) codify practitioner knowledge. However, limited formal institutional standards outside specialised cybersecurity frameworks. Academic literature on OSINT infrastructure investigation less developed than technical security research. Professional certifications (GIAC GOSI) emerging but not yet universal. Gap between sophisticated practice and published standards. Technical community knowledge sharing strong but informal.
***