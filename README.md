# AI System Security Risk Assessment Framework

> A structured, documentation-driven framework for assessing security risks in AI/LLM systems, mapping threats to NIST AI RMF and OWASP LLM Top 10 controls, and producing an actionable risk register.

## Overview

AI systems introduce security risks that traditional application security frameworks were not designed to address. Prompt injection, training data poisoning, and model supply chain attacks require a dedicated assessment methodology, and most organisations lack a repeatable process for identifying and prioritising these threats.

This project delivers a complete, reusable risk assessment framework for AI and large language model deployments. It structures the assessment process around two industry-standard references: the NIST AI Risk Management Framework (AI RMF 1.0) and the OWASP LLM Top 10. The output is a populated risk register with threat scenarios, likelihood and impact ratings, control mappings, and recommended mitigations.

I built this to demonstrate the core workflow of an AI Security Risk Analyst: identifying what can go wrong in an AI system, framing it in terms of established frameworks, and communicating risk clearly to both technical and non-technical stakeholders. The framework is designed to be adapted to real deployment contexts with minimal rework.

## What I Built / Key Features

- **Threat Model Templates:** Structured threat modelling worksheets for LLM-based systems, covering assets, trust boundaries, attack surfaces, and adversary objectives using a STRIDE-inspired approach adapted for AI.
- **OWASP LLM Top 10 Assessment Checklist:** A per-category checklist that maps each of the 10 vulnerability classes to concrete test questions, observable indicators, and relevant system components.
- **NIST AI RMF Control Mapping:** A crosswalk document aligning identified risks to the Govern, Map, Measure, and Manage functions of the NIST AI RMF, including suggested organisational roles and review cadences.
- **Risk Register (Populated Example):** A fully worked example risk register covering a representative LLM-powered application, with likelihood and impact scores, composite risk ratings, and prioritised remediation actions.
- **Scoring Rubric:** A documented, repeatable methodology for rating likelihood and impact that accounts for AI-specific factors such as adversarial accessibility of the model interface and sensitivity of training data.
- **Reporting Template:** A concise executive summary template for communicating risk findings to stakeholders who are not expected to read the full register.

## Skills & Tools Demonstrated

**Frameworks and Standards**
- NIST AI RMF 1.0 (Govern, Map, Measure, Manage)
- OWASP LLM Top 10 (2023)
- STRIDE threat modelling methodology

**Security Practice**
- AI/LLM-specific threat modelling
- Risk register construction and scoring
- Control gap analysis and remediation planning
- Technical writing for mixed audiences

**Tooling**
- `draw.io` for architecture and data flow diagrams
- `Markdown` and `YAML` for structured, version-controlled documentation
- `Python` for lightweight risk scoring calculations and report generation scripts
- `Git` for version control and review history of assessment artefacts

**Reference Sources**
- NIST AI 100-1 (Artificial Intelligence Risk Management Framework)
- OWASP LLM Top 10 project documentation
- MITRE ATLAS tactics and techniques for adversarial ML

## Architecture & Approach

The framework follows a four-phase assessment lifecycle that mirrors the structure of the NIST AI RMF.

```text
[1. SCOPE]          [2. IDENTIFY]         [3. ANALYSE]          [4. REPORT]
Define system  -->  Threat model      -->  Score & map       -->  Risk register
boundary            OWASP LLM Top 10      to NIST AI RMF         + exec summary
assets, roles       STRIDE workshop       controls, gaps
trust boundaries    MITRE ATLAS ref       remediation plan
```

The assessment starts by scoping the target system, capturing data flows, model interfaces, and trust boundaries in a diagram. From there, threat scenarios are generated using the OWASP LLM Top 10 as a prompt list and refined through a STRIDE pass. Each scenario is scored using the rubric, mapped to the relevant NIST AI RMF function, and entered into the risk register. A Python script aggregates scores and generates a summary report in Markdown.

Key design decisions: keeping all artefacts in plain text formats so they are diff-able and auditable in Git, separating the scoring rubric from the register itself so the methodology can be updated independently, and providing a worked example so the framework is immediately usable as a reference.

## Suggested Repository Structure

```text
ai-security-risk-framework/
├── README.md
├── docs/
│   ├── methodology.md          # Scoring rubric and assessment lifecycle
│   ├── nist-airgmf-mapping.md  # NIST AI RMF control crosswalk
│   └── owasp-llm-checklist.md  # Per-category assessment checklist
├── templates/
│   ├── threat-model-template.md
│   ├── risk-register-template.csv
│   └── executive-summary-template.md
├── examples/
│   ├── threat-model-llm-chatbot.md
│   ├── risk-register-llm-chatbot.csv
│   └── executive-summary-llm-chatbot.md
├── diagrams/
│   └── system-boundary-llm-chatbot.drawio
└── scripts/
    ├── score_risks.py          # Aggregates register scores
    └── generate_report.py      # Renders Markdown summary from CSV
```

## What This Demonstrates to Employers

- **Shows ability to apply NIST AI RMF in practice**, not just cite it, by producing concrete control mappings and governance artefacts for a realistic system.
- **Demonstrates familiarity with OWASP LLM Top 10** as an operational tool, translating vulnerability categories into assessable, evidence-backed findings.
- **Illustrates structured risk communication**, producing outputs appropriate for both engineering teams (detailed register) and leadership (executive summary).
- **Shows repeatable, auditable process thinking**, using version-controlled plain-text artefacts and a documented scoring rubric that a team could adopt and extend.
- **Demonstrates cross-framework literacy**, connecting OWASP findings to NIST AI RMF functions and referencing MITRE ATLAS for adversarial ML context.
- **Reflects awareness of the AI threat landscape**, covering prompt injection, data poisoning, model supply chain risks, and insecure output handling as first-class concerns.

## Getting Started

**Prerequisites:** Python 3.10+, `pip`, a Markdown viewer or editor (VS Code recommended).

```bash
git clone https://github.com/your-username/ai-security-risk-framework.git
cd ai-security-risk-framework
pip install -r requirements.txt
```

To score an existing risk register and generate a summary report:

```bash
python scripts/score_risks.py --input examples/risk-register-llm-chatbot.csv
python scripts/generate_report.py --input examples/risk-register-llm-chatbot.csv --output report.md
```

Start with `docs/methodology.md` for a full explanation of the scoring rubric, then open the `examples/` directory to see a completed assessment you can use as a reference.
