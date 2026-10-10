# CreditBridge Engineering Rules

This file is the concise project entry point for implementation rules. Detailed standards remain in `doc/engineering/` and must be consulted when working in the corresponding area.

## 1. Before changing code

- Read the relevant source files and existing docs; verify paths instead of relying on old examples.
- Keep product requirements, implemented behavior, and roadmap clearly distinguished.
- For API changes, inspect the router, service, model, schema, migrations, and callers.
- For UI changes, read `frontend/AGENTS.md` and the relevant current framework documentation before editing.

## 2. Architecture boundaries

- Keep responsibilities in their existing layers: HTTP/API, domain/service, persistence, and presentation.
- Follow the dependency direction and feature boundaries in `doc/engineering/04_ARCHITECTURE_RULES.md`.
- Keep shared UI and design-system code free of product-specific business logic.
- Do not make one business domain import another domain's UI or internal implementation. Use a clear API or domain contract.
- Keep provider-specific behavior behind service/adaptor boundaries.

## 3. API and data rules

- Validate request and response contracts with the project's schema conventions.
- Enforce authentication and business/lender authorization at the API boundary.
- Never assume a UUID or business identifier supplied by a caller grants access to that record.
- Handle missing and incomplete data explicitly; do not silently convert absence into a healthy score.
- Preserve financial data provenance, consent state, relevant timestamps, and audit history.
- Do not log secrets, credentials, or unnecessary personal or financial data.
- Keep database schema changes in migrations and make the deployment order clear.

## 4. Frontend rules

- Follow `doc/engineering/03_CODE_STYLE_GUIDE.md` and the design-system implementation guide.
- Use design tokens and shared components; avoid one-off styling where an existing token or component applies.
- Keep fetching and business behavior out of presentational components according to the project's frontend conventions.
- Preserve accessibility, responsive behavior, loading states, empty states, and actionable errors.
- Follow `frontend/AGENTS.md` for the frontend framework's local rules.

## 5. Product and credit rules

- Scores and recommendations must be explainable and traceable to documented inputs and calculation versions.
- Label mock data and simulated provider responses. Never present them as live customer data.
- Do not describe a route, service, or README diagram as production capability until its end-to-end behavior is verified.
- Do not connect ERP records to underwriting implicitly; define consent, data mapping, provenance, and access controls first.

## 6. Change completion

- Keep a change focused and update docs when contracts, flows, or behavior change.
- Report what changed and what was verified. Do not claim verification that was not performed.
- Follow `doc/engineering/05_AI_REVIEW_CHECKLIST.md` for review-oriented changes.

## Detailed references

- [Architecture rules](doc/engineering/04_ARCHITECTURE_RULES.md)
- [Code style](doc/engineering/03_CODE_STYLE_GUIDE.md)
- [Design-system implementation](doc/engineering/01_DESIGN_SYSTEM_IMPLEMENTATION_GUIDE.md)
- [AI engineering prompt](doc/engineering/02_AI_ENGINEERING_PROMPT.md)
- [AI review checklist](doc/engineering/05_AI_REVIEW_CHECKLIST.md)
