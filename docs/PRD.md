# CreditBridge Product Requirements Document

**Status:** Working product brief  
**Audience:** Product, design, engineering, and coding assistants  
**Source of truth:** This brief describes the product direction and the current repository. A feature listed as present in code is not thereby verified as production-ready.

## 1. Product summary

CreditBridge is a business operations and credit intelligence platform for Indian MSMEs. It combines ERP capabilities for recording day-to-day business activity with a credit layer that turns financial evidence into an understandable profile for lenders.

The platform serves two connected groups:

- **MSME teams** that need to manage business records and present their financial position clearly.
- **Lenders** that need a consistent way to review, filter, and monitor MSME credit opportunities.

## 2. Problem

Many small businesses have useful operating and financial records spread across invoices, bank activity, tax filings, and operational systems. Those records can be hard for a lender to collect and assess consistently. The result can be slow underwriting and limited access to credit for businesses that lack conventional collateral or credit histories.

CreditBridge aims to organize relevant business data, calculate explainable risk indicators, and make that information easier for lenders to review.

## 3. Product goals

1. Give MSMEs a structured place to manage core business operations and financial records.
2. Collect or import relevant financial evidence with clear consent and source tracking.
3. Produce a credit profile with a score, grade, recommended credit limit, supporting factors, and risk flags.
4. Let authorized lenders find and review suitable businesses and track portfolio signals.
5. Keep decisions understandable: show the financial signals behind a score rather than presenting a number alone.

## 4. Users and needs

### MSME owner or finance operator

- Maintain customer, supplier, invoice, payment, inventory, and financial records.
- Share bank or tax data with consent or upload available records.
- Understand the business's credit profile and what could improve it.
- Prepare a useful financial package when seeking credit.

### Lender or underwriting analyst

- Find businesses that fit lending thresholds and segments.
- Review a business's score, financial signals, recommended limit, and risk flags.
- Record review outcomes and monitor portfolio risk.

### CreditBridge operator

- Configure data providers and platform settings.
- Monitor ingestion, scoring, and service health.
- Investigate audit history and data quality issues.

## 5. Core user journeys

### Business operations

1. An MSME user signs in and records or imports business activity.
2. The user manages sales, purchasing, accounting, stock, or manufacturing records as relevant.
3. Those records are available for the user's operational workflows and, where explicitly integrated, financial analysis.

### Credit profile

1. A business supplies bank and GST evidence through an available provider flow or import.
2. The backend analyzes available evidence and computes a risk score.
3. The business or authorized lender can review the score, grade, recommended limit, positive factors, and flags.
4. The business can use the financial outputs and documents to support a loan discussion.

### Lender review

1. A lender registers and authenticates with its API key.
2. The lender filters the scored business pool and opens a business detail or explanation.
3. The lender records a review or rejection and inspects portfolio information.

## 6. Functional requirements

| ID | Requirement | Repository evidence / status |
|---|---|---|
| FR-01 | MSME account registration, login, and current-user endpoint | Implemented route code in `backend/app/api/v1/auth.py`; runtime verification not established here. |
| FR-02 | Business profile, invoice, and payment workflows | API routes and services exist under `backend/app/api/v1/`; provider configuration and complete workflows need environment-level verification. |
| FR-03 | Bank data import and Account Aggregator consent flow | Upload and consent routes exist. Provider service includes mock/fallback behavior. |
| FR-04 | PAN/GSTIN/MSME/DigiLocker verification flows | KYC routes and service code exist; live provider behavior depends on credentials and configuration. |
| FR-05 | Compute and retrieve a credit score from bank and GST signals | `intelligence.py` invokes the pipeline in `agents/pipeline.py`; the current main pipeline uses bank analysis, GST analysis, and rule-based scoring. |
| FR-06 | Provide a filtered lender business pool and risk segments | Lender route code exists in `backend/app/api/v1/lender.py`; it requires a lender API key. |
| FR-07 | Explain lender-facing business risk and record review actions | Detail, explanation, rejection, review, portfolio, and audit-related route code exists. |
| FR-08 | Create loan offers/applications and financial document outputs | Loan and document routes/services exist; end-to-end provider and UI verification remains open. |
| FR-09 | Support ERP operations across accounting, buying, selling, stock, manufacturing, and CRM | Domain models, services, and routers exist in `backend/app/`; the completion level of each end-to-end workflow needs a separate audit. |
| FR-10 | Connect ERP activity automatically to credit scoring | Product opportunity; do not assume this is implemented without tracing the data flow. |

## 7. Non-functional requirements

- **Security:** Authenticate users and lenders; scope business data to authorized identities; protect API keys and provider credentials.
- **Privacy and consent:** Track consent for external financial data access and respect its status and scope.
- **Auditability:** Record important lender and administrative actions.
- **Explainability:** Persist score components, flags, positive factors, data coverage, and computation time.
- **Reliability:** Make ingestion, scoring, and provider failures visible and recoverable.
- **Data quality:** Preserve source, date range, and completeness information so missing evidence is not mistaken for healthy evidence.
- **Accessibility and usability:** Follow the design principles and system guidance in `doc/engineering/design/`.

## 8. Product boundaries and assumptions

- CreditBridge is a platform for business operations and credit intelligence; the repository does not by itself establish that CreditBridge directly originates or funds loans.
- The README describes a live, event-driven and predictive product direction. The currently inspected main scoring pipeline is narrower and rule-based; treat broader AI and real-time claims as roadmap until verified in the running system.
- The ERP domain modules and credit-intelligence modules coexist in this repository. Their automatic integration is not assumed.
- A code route or integration service does not prove a production provider connection, deployment, or complete user journey.

## 9. Success measures to define

Set baselines and targets before launch. Candidate measures:

- Time from complete data submission to a reviewable credit profile.
- Share of profiles with adequate and recent source data.
- Lender review time per business.
- Share of lender reviews with a recorded reason and outcome.
- Data ingestion and scoring failure rates.
- MSME completion rate for onboarding and consent.

## 10. Release acceptance checklist

- A business can complete the intended onboarding and submit or connect financial data.
- Missing, stale, or incomplete data is visible in the profile.
- Score components and recommendations have documented definitions and reviewed edge cases.
- A lender can authenticate, filter the pool, inspect a profile, and record a review.
- Business and lender access boundaries are verified.
- Provider credentials, error handling, migrations, deployment, and recovery procedures are documented.
- User-facing claims match the behavior that has been verified in the release environment.
