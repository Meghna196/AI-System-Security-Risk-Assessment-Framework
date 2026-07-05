# AI System Security Risk Assessment Framework

A reusable security risk assessment framework for AI systems, built against the target system **SupportBot v2** — a fictional LLM-powered customer support chatbot deployed by fintech company Meridian Financial.

This repo maps a concrete AI system through the **NIST AI Risk Management Framework (AI RMF 1.0)** and the **OWASP LLM Top 10**, producing a threat model, a scored risk register, and a written assessment report — the same deliverables an AI Security Risk Analyst would produce during the first weeks of a real engagement.

## Target System

**SupportBot v2** (Meridian Financial) — a customer-facing LLM chatbot that answers account queries, explains transaction history, and opens support tickets. It runs on a third-party LLM API, retrieves customer data via a RAG pipeline against an internal PostgreSQL database, and is exposed to authenticated customers through a web portal.

## Repo Structure

```
ai-risk-framework/
├── docs/
│   ├── system-description.md      # Scope document: what the system is, who uses it, what data it touches
│   ├── nist-ai-rmf-mapping.md      # GOVERN / MAP / MEASURE / MANAGE mapping
│   └── threat-model.md             # STRIDE threat model cross-referenced to OWASP LLM Top 10
├── diagrams/
│   └── supportbot-dfd.svg          # Data flow diagram
├── register/
│   ├── SupportBot-Risk-Register.xlsx
│   └── risk-register.csv           # CSV export used by scripts/risk_summary.py
├── scripts/
│   └── risk_summary.py             # Reads the CSV register, prints a priority-ordered summary
└── report/
    └── SupportBot-Security-Risk-Assessment.md   # Final written assessment
```

## Frameworks Applied

- NIST AI RMF 1.0 (GOVERN, MAP, MEASURE, MANAGE)
- STRIDE threat modeling methodology
- OWASP LLM Top 10 (2025)

## How to Reproduce the Risk Summary

```bash
python3 scripts/risk_summary.py register/risk-register.csv
```
