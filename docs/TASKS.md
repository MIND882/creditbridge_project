# CreditBridge Project Tasks

This is a short, evidence-aware project queue. A checked item means relevant code or documentation is present; it does not mean production deployment or acceptance testing has been completed.

## Present in the repository

- [x] MSME authentication, business, KYC, consent, data, invoice, payment, loan, intelligence, and document API modules.
- [x] Bank/GST/risk scoring pipeline and persisted risk-score model.
- [x] Lender APIs for pool, segments, business detail/explanation, review/rejection, and portfolio-related flows.
- [x] ERP API domains for accounting, buying, selling, stock, manufacturing, and CRM.
- [x] MSME-facing and lender-facing frontend projects.
- [x] Engineering and design-system documentation under `doc/`.

## Product and integration work to define or verify

- [ ] Choose and document the first release scope across credit intelligence and ERP; define what is in and out.
- [ ] Verify one complete MSME journey from account creation through bank/GST data submission to an explainable score.
- [ ] Verify one complete lender journey from authentication through pool filtering, business review, and recorded outcome.
- [ ] Audit which external providers are live, sandboxed, mocked, or unavailable in each environment.
- [ ] Trace whether ERP accounting, invoice, and payment records feed the credit profile; document the actual mappings or mark the integration as future work.
- [ ] Review scoring inputs, weights, missing-data behavior, versioning, confidence, and recommended-limit calculations with product and credit stakeholders.
- [ ] Compare lender frontend API paths and authentication headers with the registered backend route prefixes and requirements.
- [ ] Document deployment, secrets, migrations, background workers, event-stream operations, backups, and recovery.
- [ ] Audit access control and business-data isolation across core APIs and ERP modules.
- [ ] Reconcile the README's product and architecture claims with verified behavior in the target environment.

## Feature task template

Copy this template for each planned feature:

```markdown
### [ ] Feature title
- **Problem:** Who has what problem?
- **Outcome:** What should become possible?
- **Scope:** What is included and excluded?
- **Acceptance criteria:** Observable behavior that proves completion.
- **Dependencies:** APIs, data, providers, migrations, or design decisions.
- **Verification:** How the behavior will be checked.
- **Status:** Planned / In progress / Implemented / Verified / Released.
```
