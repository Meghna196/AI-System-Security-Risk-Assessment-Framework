# AI System Security Risk Assessment

## SupportBot v2 - Meridian Financial

**Assessment Date:** July 5, 2026
**Prepared by:** Meghna Suresh
**Framework:** NIST AI RMF 1.0 | OWASP LLM Top 10

---

## 1. Executive Summary

SupportBot v2 is Meridian Financial's LLM-powered customer support chatbot, retrieving customer account data through a RAG pipeline and calling a third-party LLM API to answer tier-1 support queries. This assessment applied the NIST AI RMF (MAP, MEASURE, MANAGE) and a STRIDE threat model cross-referenced to the OWASP LLM Top 10, producing 16 distinct risks across five components. Four risks scored Critical: direct prompt injection against the LLM, two variants of broken retrieval scoping that let one customer's session pull another customer's PII, and an admin panel that auto-executes LLM-recommended account actions without human review. The headline finding is that SupportBot's largest exposures sit at the boundary between the RAG pipeline and the LLM — where untrusted input (customer prompts, retrieved documents) is not yet clearly separated from trusted instructions and identity context. The top recommendation is to enforce per-session retrieval scoping and treat all retrieved/user-supplied content as untrusted data before it reaches the LLM, alongside a human-in-the-loop gate on any account-impacting action the bot recommends.

## 2. Scope and Methodology

- **System assessed:** SupportBot v2 (see `docs/system-description.md` for full scope)
- **Assessment type:** Threat model and risk register, based on architecture review; no live/dynamic testing was performed
- **Frameworks applied:** NIST AI RMF 1.0 (MAP, MEASURE, MANAGE — see `docs/nist-ai-rmf-mapping.md`), STRIDE threat modeling (see `docs/threat-model.md`), OWASP LLM Top 10
- **Artefacts produced:** Data flow diagram (`diagrams/supportbot-dfd.svg`), STRIDE threat model (`docs/threat-model.md`), scored risk register (`register/SupportBot-Risk-Register.xlsx`, `register/risk-register.csv`), automated risk summary script (`scripts/risk_summary.py`)
- **Limitations:** This assessment is based on the architecture as described in `docs/system-description.md`. No penetration testing, red-teaming, or live prompt-injection testing was conducted against a running instance of SupportBot. Likelihood and Impact scores reflect the as-described architecture with no compensating controls assumed beyond what is explicitly documented. Findings should be validated against the actual deployed configuration before controls are prioritised for implementation.

## 3. System Architecture Summary

SupportBot v2 is deployed on AWS and exposed to authenticated retail banking customers through a React web portal (see `diagrams/supportbot-dfd.svg`). Customer requests pass through an AWS API Gateway that authenticates the session, then to a LangChain-based RAG Retriever that queries an internal PostgreSQL customer database for account context. That context, along with the user's prompt, is sent to a third-party, GPT-4-class LLM API outside Meridian's direct control. The LLM's response is returned to the customer and logged, along with the originating prompt and retrieved context, to a centralised CloudWatch log aggregator. A separate internal Admin Panel gives support staff broader read access to customer records and the ability to review or override bot responses and escalate tickets. Two trust boundaries matter most for this assessment: the boundary where untrusted customer input enters the system, and the boundary where Meridian's data crosses out to the third-party LLM vendor.

## 4. Key Findings

### 4.1 Critical Risks

**AI-001 — Direct prompt injection bypasses system prompt guardrails (LLM API).** A customer-supplied prompt can override or subvert the system prompt that constrains SupportBot's behaviour, potentially causing it to ignore its instructions, produce unauthorised content, or take actions outside its intended scope. This is the foundational LLM attack class (OWASP LLM01) and, left unaddressed, undermines every other control built on top of "the model will behave as instructed." *Recommended control:* an input validation layer ahead of the LLM API, output filtering on responses, and periodic adversarial/red-team testing of prompts.

**AI-005 — PII over-retrieval exposes other customers' data in the active context window (RAG Pipeline).** If the RAG retriever is not strictly scoped to the authenticated customer's own records, a normal or lightly manipulated query can pull other customers' account details into the context sent to the LLM — and potentially into the response shown to the wrong customer. Given SupportBot's GDPR and PCI-DSS-adjacent data, this is a direct regulatory exposure, not just a technical bug. *Recommended control:* retrieval scoping by authenticated session/user ID, enforced with row-level security in PostgreSQL rather than relying on the retriever's query logic alone.

**AI-006 — Crafted queries retrieve data for accounts other than the authenticated user (RAG Pipeline).** Related to but distinct from AI-005: this is a broken-access-control issue at the retrieval layer itself, where query parameters can be manipulated to target another account rather than the over-retrieval happening incidentally. *Recommended control:* server-side validation of every retrieval query against the authenticated session identity, independent of client-supplied parameters.

**AI-015 — LLM-recommended actions auto-executed without human confirmation (Admin Panel).** SupportBot can recommend account-impacting actions (ticket escalation, refund initiation) that the admin panel currently executes without a human checking them first. This is "excessive agency" (OWASP LLM08): a successful prompt injection or a model error doesn't just produce a bad chat message, it can trigger a real financial action. *Recommended control:* require explicit human confirmation before any such action is executed, regardless of how confident the model's recommendation appears.

### 4.2 High Risks

Four risks scored High (15–16): **AI-002** (indirect prompt injection via retrieved/ingested documents causing unintended actions — treat all retrieved content as untrusted data, never as instructions), **AI-009** (JWT forgery/replay enabling session impersonation — short-lived tokens, key rotation, replay detection), **AI-011** (customer-tier tokens reaching admin-only endpoints due to missing server-side authorization checks), and **AI-012** (full prompts/responses containing PII logged in plaintext with broad internal access — redact before persistence and restrict via RBAC). None of these are unique to SupportBot's use of an LLM in isolation, but each compounds the Critical risks above: AI-002 is a second path into the same prompt-injection problem as AI-001, and AI-009/AI-011 would, if exploited, give an attacker exactly the kind of account access that AI-005/AI-006 show is already under-scoped.

### 4.3 Medium and Low Risks

| Risk ID | Level | Summary |
|---|---|---|
| AI-016 | Medium (12) | Admin panel lacks MFA, raising account takeover risk for high-privilege users |
| AI-003 | Medium (9) | Model can be induced to leak system prompt or memorised training data |
| AI-004 | Medium (9) | Token flooding can exhaust API quota / cost ceiling |
| AI-010 | Medium (9) | No per-user rate limiting at the API Gateway |
| AI-007 | Low (8) | Knowledge base can be poisoned via attacker-controlled ingested content |
| AI-008 | Low (8) | Vector store misconfiguration could allow raw document retrieval outside the RAG flow |
| AI-013 | Low (6) | Logs aren't tamper-evident, limiting attribution after an incident |
| AI-014 | Low (6) | Log pipeline lacks immutable storage |

## 5. NIST AI RMF Maturity Observations

Mapping SupportBot against NIST AI RMF's four core functions (full detail in `docs/nist-ai-rmf-mapping.md`) surfaces a consistent pattern: Meridian has reasonably mature conventional application-security practices (the API Gateway, standard logging) but has not yet adapted its **GOVERN** function to account for LLM-specific risk. Risk ownership for AI-specific issues is currently diffused across the CISO, DPO, and Engineering Lead with no single accountable owner for LLM behaviour risk, and the Third-Party Vendor Risk Policy predates LLM procurement — it does not require SLA or change-notification terms from the LLM vendor, nor does it define a fallback behaviour if the vendor has an outage or unilaterally changes model behaviour. On **MAP**, the organisation has not yet formally catalogued LLM-specific risk categories (prompt injection, excessive agency, training-data leakage) as distinct from generic IT risk — this assessment is, in effect, the first MAP pass. On **MEASURE**, no dynamic testing (red-teaming, adversarial prompt testing) has been performed; all scores in this assessment are architecture-review estimates and should be treated as a floor, not a validated ceiling, on actual risk. **MANAGE** is the most concrete function today only because this assessment has just populated it — before this engagement, there was no risk register or prioritised control list specific to SupportBot.

## 6. Prioritised Recommendations

| Priority | Recommendation | Effort | Owner |
|---|---|---|---|
| 1 | Implement per-session retrieval scoping in the RAG pipeline (row-level security in Postgres, server-side query validation against session identity) | High | Data Engineering |
| 2 | Deploy a prompt injection input validation/output filtering layer in front of the LLM API and treat all retrieved/ingested content as untrusted data | Medium | Engineering |
| 3 | Require human-in-the-loop confirmation before the admin panel executes any LLM-recommended account-impacting action | Medium | Product / Engineering |
| 4 | Enforce function-level authorization checks server-side for all admin endpoints; add MFA to admin panel accounts | Medium | Engineering / IT Security |
| 5 | Redact/mask PII in logs before persistence and restrict log access via RBAC; move to immutable (write-once) log storage | Medium | Security Engineering |
| 6 | Conduct quarterly red-team exercises specifically targeting LLM attack classes (prompt injection, retrieval-scoping bypass, indirect injection via ingested documents) | Medium | Security |
| 7 | Update the Third-Party Vendor Risk Policy to require SLA/change-notification terms from the LLM vendor and define a fallback/degraded-mode behaviour for vendor outages | Low | Vendor Management |

## 7. Conclusion

SupportBot v2's overall risk posture is elevated primarily by four Critical findings clustered around insufficient separation between untrusted input and trusted instructions/identity — prompt injection into the LLM and broken retrieval scoping in the RAG pipeline are two expressions of the same underlying gap, compounded by an admin panel that acts on LLM output without human review. None of these are exotic: all four have well-understood, implementable controls (input validation, retrieval scoping, human-in-the-loop confirmation) rather than requiring a redesign of the system. The recommended next step is to treat retrieval scoping and prompt-injection defences as a single Priority-1 workstream, since fixing one without the other leaves the same class of exposure open through the other path.
