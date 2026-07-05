# SupportBot v2 - System Description

## System Overview

SupportBot v2 is an LLM-powered customer support assistant deployed by Meridian Financial, a fictional retail banking and fintech company. It handles tier-1 customer support queries through a web-based chat interface, reducing load on human support agents while giving customers 24/7 self-service access to account information.

## Components

- **Frontend:** React web portal, customer-facing, embedded in Meridian's online banking site
- **API Gateway:** AWS API Gateway — authenticates user sessions (JWT-based), rate-limits requests, routes traffic to backend services
- **LLM Backend:** Third-party LLM API (GPT-4-class model, external vendor — e.g., OpenAI or Anthropic), accessed over HTTPS with an API key held in a secrets manager
- **RAG Pipeline:** LangChain-based retriever that queries an internal PostgreSQL customer database and injects retrieved context into the LLM prompt
- **Admin Panel:** Internal web tool used by support staff to review conversations, override bot responses, and escalate tickets
- **Logging:** Centralised log aggregation (AWS CloudWatch) capturing prompts, responses, and system events

## Data Processed

- Customer PII (name, account number, last 4 digits of card, address on file)
- Transaction summaries (dates, amounts, merchant categories — not full card numbers)
- Support ticket history and prior conversation transcripts
- Session/authentication metadata (JWT claims, session IDs)

## Users

- **Authenticated retail banking customers** — access via the web portal, scoped to their own account data only
- **Internal support staff** — access via the admin panel, with broader read access across customer records for ticket handling

## Data Flow (Summary)

1. Customer authenticates via the web portal and submits a query.
2. API Gateway validates the session token and forwards the request.
3. RAG Retriever queries the customer database, scoped (in theory) to the authenticated customer's account.
4. Retrieved context + user query are sent to the external LLM API.
5. LLM response is returned, logged, and displayed to the customer.
6. All prompts, retrieved context, and responses are written to centralised logs.

## Deployment Environment

- AWS cloud-hosted (multi-AZ, single region)
- External-facing (internet accessible via the customer web portal)
- Admin panel is accessible over a VPN-restricted internal network

## Regulatory Context

- Subject to **GDPR** (EU/UK customer PII)
- **PCI-DSS adjacent** — the system handles card-data-adjacent fields (last 4 digits, transaction metadata) though full PANs are not processed
- Subject to Meridian's internal Third-Party Vendor Risk Policy due to reliance on an external LLM provider

## Out of Scope for This Assessment

- The underlying LLM vendor's internal model training, alignment, or infrastructure security (treated as a third-party dependency, assessed at the integration boundary only)
- Physical security of Meridian's offices
- General corporate IT security (endpoint security, email security) not directly tied to SupportBot
