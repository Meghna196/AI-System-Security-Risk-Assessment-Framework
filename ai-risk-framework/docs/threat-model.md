# Threat Model - SupportBot v2

## Methodology: STRIDE + OWASP LLM Top 10 cross-reference

## DFD Reference: `diagrams/supportbot-dfd.svg`

Each component from the data flow diagram is analysed against the six STRIDE categories (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege). Every threat is cross-referenced to the OWASP LLM Top 10 where an LLM-specific mapping applies; where a threat is a conventional application-security issue rather than an LLM-specific one, it is mapped to the relevant standard OWASP category instead and noted as such. Risk IDs correspond 1:1 to rows in `register/SupportBot-Risk-Register.xlsx`.

---

## Component: LLM API Integration

| STRIDE Category | Threat | OWASP Ref | Risk ID |
|---|---|---|---|
| Tampering | Direct prompt injection via user input bypasses the system prompt / guardrails, causing the model to ignore its instructions | LLM01: Prompt Injection | AI-001 |
| Elevation of Privilege | Indirect prompt injection: instructions embedded in retrieved documents or transaction records cause the model to take unintended actions (e.g., recommend a refund) | LLM01: Prompt Injection, LLM08: Excessive Agency | AI-002 |
| Information Disclosure | Model is manipulated into revealing its system prompt, internal instructions, or memorised fragments of training data | LLM06: Sensitive Information Disclosure | AI-003 |
| Denial of Service | Adversarial long-form or repetitive inputs ("token flooding") exhaust API rate limits and blow through the monthly cost ceiling | LLM04: Model Denial of Service | AI-004 |

---

## Component: RAG Pipeline / Customer Database

| STRIDE Category | Threat | OWASP Ref | Risk ID |
|---|---|---|---|
| Information Disclosure | Over-retrieval pulls more records than intended into the active context window, exposing other customers' PII in the response | LLM06: Sensitive Information Disclosure | AI-005 |
| Spoofing | Crafted queries or manipulated session parameters retrieve records for accounts other than the authenticated customer (broken retrieval scoping) | LLM02: Insecure Output Handling / Broken Access Control at retrieval layer | AI-006 |
| Tampering | Attacker-controlled content (e.g., a support ticket comment, an uploaded document) is ingested into the knowledge base and poisons future retrieval results | LLM03: Training Data / Supply Chain Poisoning | AI-007 |
| Information Disclosure | Vector store or embedding index misconfiguration allows direct/raw document retrieval outside the intended RAG query flow | LLM06: Sensitive Information Disclosure | AI-008 |

---

## Component: API Gateway

| STRIDE Category | Threat | OWASP Ref | Risk ID |
|---|---|---|---|
| Spoofing | JWT forgery or session-token replay allows an attacker to impersonate an authenticated customer session | OWASP API2:2023 Broken Authentication (no direct LLM Top 10 mapping — conventional API security issue) | AI-009 |
| Denial of Service | Absence of per-user/per-IP rate limiting allows a single account to exhaust shared gateway and backend capacity | LLM04: Model Denial of Service | AI-010 |
| Elevation of Privilege | Insufficient server-side authorization checks allow a customer-tier token to reach admin-only endpoints | OWASP API5:2023 Broken Function Level Authorization (no direct LLM Top 10 mapping) | AI-011 |

---

## Component: Audit Logs (CloudWatch)

| STRIDE Category | Threat | OWASP Ref | Risk ID |
|---|---|---|---|
| Information Disclosure | Logs capture full prompts and responses, including customer PII, in plaintext and are readable by a broad internal audience | LLM06: Sensitive Information Disclosure | AI-012 |
| Repudiation | Logs are not tamper-evident, so actions taken by the bot, staff, or an attacker cannot be reliably attributed after the fact | OWASP A09:2021 Security Logging and Monitoring Failures (no direct LLM Top 10 mapping) | AI-013 |
| Tampering | The log pipeline lacks write-once / immutable storage, allowing an attacker with log-write access to delete or alter evidence post-incident | OWASP A09:2021 Security Logging and Monitoring Failures (no direct LLM Top 10 mapping) | AI-014 |

---

## Component: Admin Panel

| STRIDE Category | Threat | OWASP Ref | Risk ID |
|---|---|---|---|
| Elevation of Privilege | LLM-recommended actions (ticket escalation, refund initiation) are auto-executed by the admin panel without a human confirmation step | LLM08: Excessive Agency | AI-015 |
| Spoofing | Admin panel authentication lacks MFA, increasing the likelihood of account takeover for high-privilege internal users | OWASP A07:2021 Identification and Authentication Failures (no direct LLM Top 10 mapping) | AI-016 |

---

## Summary

- **16 distinct threats** identified across 5 components.
- **11 of 16** threats map directly to an OWASP LLM Top 10 category — reflecting that most of SupportBot's novel risk surface is LLM-specific (prompt injection, excessive agency, sensitive information disclosure via retrieval).
- **5 of 16** threats are conventional application-security issues (broken authentication, broken authorization, logging/monitoring failures) that exist independently of the LLM component but still materially affect SupportBot's overall risk posture. These are noted against standard OWASP Top 10 / OWASP API Security Top 10 categories per the verification guidance for this exercise.
- Scoring and prioritisation of each threat is carried out in `register/SupportBot-Risk-Register.xlsx` (see also `register/risk-register.csv`).
