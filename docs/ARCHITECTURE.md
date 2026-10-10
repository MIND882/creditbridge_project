# CreditBridge Architecture

**Status:** Repository-oriented architecture map  
**Last reviewed:** 2026-10-06

This document describes the main systems present in the repository and the intended product flow. It does not claim that every listed component is deployed or connected end to end.

## 1. System overview

CreditBridge contains three broad areas:

1. **MSME credit-intelligence backend** — business onboarding, data intake, scoring, loan-related outputs, and lender APIs.
2. **ERP domain backend** — accounting, stock, buying, selling, manufacturing, and CRM APIs.
3. **Web applications** — an MSME-facing application and a separate lender portal.

The repository also includes engineering and design-system documentation under `doc/engineering/`.

## 2. Credit-intelligence data flow

```text
MSME profile / bank and GST evidence
                 ↓
         FastAPI v1 endpoints
                 ↓
        SQLAlchemy data models
                 ↓
     Bank analyzer → GST analyzer
                 ↓
       Rule-based risk scorer
                 ↓
       Persisted risk profile
                 ↓
 Lender pool, detail, explanation,
 review, and portfolio endpoints
```

The current pipeline in `backend/app/agents/pipeline.py` runs bank analysis, GST analysis, and risk scoring, then stores a risk score. Other code includes buyer scoring, cash-flow forecasting, event processing, and a Redis event consumer. Their presence should not be interpreted as proof that every component participates in the main scoring path.

## 3. Backend structure

### CreditBridge core

- `backend/app/api/v1/` — auth, business, consent, data, documents, intelligence, invoices, KYC, lender, loans, payments, and uploads.
- `backend/app/agents/` — bank/GST analysis, score calculation, forecasting, buyer scoring, event handling, and orchestration.
- `backend/app/services/` — provider adapters and application services such as KYC, bank-data, payment, financial-statement, PDF, and notification handling.
- `backend/app/models/` — SQLAlchemy models for businesses, bank and GST data, invoices, scores, loans, consent, and audit records.

### ERP domains

ERP domains are grouped by business area. The common pattern is a domain folder with API, schema, model, repository, and service code. Examples include:

- `backend/app/accounts/`
- `backend/app/buying/`
- `backend/app/selling/`
- `backend/app/stock/`
- `backend/app/manufacturing/` (check the exact directory name in the working tree; route tags use `MANUFACTURING`)
- `backend/app/crm/`

`backend/app/main.py` registers routers and is the place to inspect active URL prefixes and tags. Do not infer automatic cross-domain data flow from co-location in this repository.

## 4. Web applications

- `frontend/` — MSME-facing application.
- `frontend-lender/` — lender portal with pool, business detail, portfolio, alerts, and risk-intelligence screens.

The engineering context doc and app READMEs may describe intended structures that have changed. Check the actual source tree and package configuration before implementing UI changes.

## 5. Data and infrastructure

The documented stack includes Python/FastAPI, SQLAlchemy, PostgreSQL, Redis, and React/TypeScript web apps. The exact active configuration is defined by the backend settings, requirements, Docker files, and each frontend package. Verify these files before changing versions or deployment assumptions.

Primary persistent records include business profiles, bank transactions/accounts, GST filings, invoices, consent records, risk scores, loan offers, and audit events. ERP models hold operational records for their respective domains.

## 6. External services

The code and README refer to integrations for bank Account Aggregator data, GST data, KYC, payments, and notifications. Treat these as provider adapters whose live status depends on credentials, environment configuration, and provider responses. Some paths have mock or fallback behavior.

## 7. Important boundaries

- API routes handle HTTP concerns; services and domain logic own application behavior.
- A feature should use the owning domain's models/services rather than duplicating its business rules in a router or UI.
- The lender portal consumes lender endpoints and must send the configured lender credential as required by the API.
- ERP operations should only feed credit scoring through an explicit, documented integration path with consent, provenance, and tests.
- Score calculation, credit policy, and provider transformations need explicit versioning and clear explanations.

## 8. How to verify a proposed architecture change

1. Trace the request from router to service, repository/model, and response schema.
2. Check router registration in `backend/app/main.py` and migrations for any schema changes.
3. Check authentication, business scoping, consent, audit behavior, and error handling.
4. Identify whether the change affects the MSME UI, lender UI, or both.
5. Update the relevant API and design documentation along with the implementation.
