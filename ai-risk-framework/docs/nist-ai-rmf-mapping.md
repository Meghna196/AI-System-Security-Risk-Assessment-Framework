# NIST AI RMF Mapping - SupportBot v2

## GOVERN

- **Risk ownership:** CISO (overall accountability), Data Protection Officer (PII/privacy risk), Engineering Lead (model behaviour and integration risk), Head of Vendor Management (third-party LLM risk)
- **Policies in scope:** Acceptable Use Policy, Data Retention Policy, Third-Party Vendor Risk Policy, Incident Response Plan
- **Current gaps observed:** No dedicated AI risk owner distinct from general application security; no documented policy specifically addressing LLM prompt/output handling; vendor risk policy predates LLM-specific procurement and has not been updated to address model-specific risks (e.g., training-data use of customer prompts, model version changes)

## MAP

| AI Risk Category | Relevance to SupportBot |
|---|---|
| Bias / Fairness | Medium — responses must be consistent across demographics; no current evaluation of response consistency across customer segments |
| Privacy | High — PII retrieved via RAG pipeline and passed to a third-party LLM API outside Meridian's direct control |
| Security | High — external attack surface, LLM API dependency, prompt-based attack surface not present in traditional web apps |
| Explainability | Medium — customers may query why an action was taken (e.g., a declined transaction) and the bot must not fabricate a rationale |
| Third-party dependency | High — LLM vendor availability, pricing, and policy changes are outside Meridian's control; vendor outage directly degrades SupportBot |
| Robustness | Medium — no adversarial testing has been performed against prompt manipulation or malformed inputs |
| Reliability | Medium — model updates/version changes by the vendor are not currently tracked or regression-tested against SupportBot's expected behaviour |

## MEASURE

See `register/SupportBot-Risk-Register.xlsx` and `register/risk-register.csv` for the scored risk inventory (Likelihood × Impact) derived from the STRIDE threat model in `docs/threat-model.md`. Measurement approach:

- Each threat identified in the threat model was scored for **Likelihood** (1–5) and **Impact** (1–5) based on the current (as-described) architecture, with no compensating controls assumed beyond what is explicitly documented in `docs/system-description.md`.
- Risk Score = Likelihood × Impact; Risk Level bands: 1–8 Low, 9–14 Medium, 15–19 High, 20–25 Critical.
- 4 risks scored Critical, 4 scored High, out of 16 total risks registered — see `report/SupportBot-Security-Risk-Assessment.md` Section 4 for the narrative breakdown.
- No dynamic/live testing (e.g., red-teaming, penetration testing) was performed as part of this measurement pass — scores reflect architectural review only, which is itself flagged as a governance gap below.

## MANAGE

Prioritised treatment plan (full detail in `report/SupportBot-Security-Risk-Assessment.md`, Section 6):

1. Deploy a prompt injection detection/input validation layer in front of the LLM API, and treat retrieved content as untrusted data rather than instructions (addresses AI-001, AI-002 — Critical/High).
2. Implement per-session retrieval scoping in the RAG pipeline so queries cannot return other customers' records (addresses AI-005, AI-006 — both Critical).
3. Require human-in-the-loop confirmation before any account-impacting action recommended by the LLM is executed by the admin panel (addresses AI-015 — Critical).
4. Establish a quarterly red-team cadence specifically targeting LLM-specific attack classes (prompt injection, data exfiltration via retrieval, indirect injection via ingested documents).
5. Update the Third-Party Vendor Risk Policy to require SLA and change-notification terms from the LLM vendor, and define a fallback/degraded-mode behaviour for vendor outages.
6. Assign explicit AI risk ownership in GOVERN (currently diffused across CISO/DPO/Engineering with no single accountable owner for LLM-specific risk).

This MANAGE section, together with MEASURE, is intentionally a living record — it should be revisited each time the threat model or risk register is updated.
