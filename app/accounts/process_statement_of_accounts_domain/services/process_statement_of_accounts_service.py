# HAND-WRITTEN

"""

Business logic for Process Statement Of Accounts -- port of

``erpnext/accounts/doctype/process_statement_of_accounts/process_statement_of_accounts.py``.







Upstream hooks:

    validate

    validate_account

    validate_company_for_table



The account and cost-centre tenant checks, the customer requirement, the text

defaults and the auto-email window are ported. The Project check, the three

Print Format checks and the Jinja template validation are not; see

:meth:`_validate`.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



import datetime as dt



from app.accounts.account_domain.models.account import Account

from app.accounts.cost_center_domain.models.cost_center import CostCenter

from app.accounts.process_statement_of_accounts_domain.models.process_statement_of_accounts import ProcessStatementOfAccounts

from app.accounts.psoa_cost_center_domain.models.psoa_cost_center import PsoaCostCenter

from app.accounts.psoa_project_domain.models.psoa_project import PsoaProject

from app.accounts.process_statement_of_accounts_cc_domain.models.process_statement_of_accounts_cc import ProcessStatementOfAccountsCc

from app.accounts.process_statement_of_accounts_customer_domain.models.process_statement_of_accounts_customer import ProcessStatementOfAccountsCustomer

from app.accounts.process_statement_of_accounts_domain.repositories.process_statement_of_accounts_repository import (

    ProcessStatementOfAccountsRepository,

)

from app.accounts.process_statement_of_accounts_domain.schemas.process_statement_of_accounts import (

    ProcessStatementOfAccountsCreate,

    ProcessStatementOfAccountsUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ProcessStatementOfAccountsService"]





def _add_months(day: dt.date, months: int) -> dt.date:

    """Add whole months, clamping the day to the target month's length."""

    total = day.year * 12 + (day.month - 1) + months

    year, month = divmod(total, 12)

    month += 1

    nxt = dt.date(year + (month == 12), 1 if month == 12 else month + 1, 1)

    return dt.date(year, month, min(day.day, (nxt - dt.timedelta(days=1)).day))





class ProcessStatementOfAccountsService:

    def __init__(self, repository: Optional[ProcessStatementOfAccountsRepository] = None) -> None:

        self.repository = repository or ProcessStatementOfAccountsRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProcessStatementOfAccounts:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Process Statement Of Accounts", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    # ══════════════════════════════════════════════════════════════════════

    # ported validators

    # ══════════════════════════════════════════════════════════════════════

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: ProcessStatementOfAccounts

    ) -> None:

        """

        Port of upstream ``validate``. Order is preserved: the account and cost

        centre are checked first, then the text defaults are filled in, then the

        recipient list and the auto-email window.



            validate_account                      -> ported

            validate_company_for_table("Cost

            Center")                              -> ported

            subject / body / pdf_name defaults    -> ported

            "Customers not selected."             -> ported

            the enable_auto_email window          -> ported



        TODO(PORT-VALIDATION): three upstream rules are not ported.



          * ``validate_company_for_table("Project")`` -- the Project doctype is

            not converted, so a project row cannot be resolved to a tenant.

          * The three Print Format checks ("Selected Print Format does not

            exist.", "Print Format Type should be Jinja.", "Print Format must be

            an enabled Report Print Format matching the selected Report.") --

            Print Format is not converted.

          * ``validate_template`` on subject/body/pdf_name -- it runs Jinja in a

            restricted sandbox; there is no equivalent here.



        All three fail open: a statement may reference a project, a print format

        or a template that would be rejected upstream.

        """

        self._validate_account(db, business_id, row)

        self._validate_cost_center(db, business_id, row)

        self._apply_text_defaults(row)

        self._validate_customers(row)

        self._apply_auto_email_window(row)



    # ── validate_account ──────────────────────────────────────────────────

    def _validate_account(

        self, db: Session, business_id: uuid.UUID, row: ProcessStatementOfAccounts

    ) -> None:

        """

        Upstream compares the account's ``company``. Company is the tenant here,

        so an account owned elsewhere -- or one that does not exist at all --

        simply does not resolve.

        """

        if not row.account_id:

            return



        account = db.scalar(

            select(Account).where(

                Account.id == row.account_id,

                Account.business_id == business_id,

            )

        )

        if account is None:

            raise DomainValidationError(

                f"Account {row.account_id} doesn\'t belong to this business",

                code="process_statement_of_accounts_account_other_company",

                details={"account_id": str(row.account_id)},

            )



    # ── validate_company_for_table("Cost Center") ─────────────────────────

    def _validate_cost_center(

        self, db: Session, business_id: uuid.UUID, row: ProcessStatementOfAccounts

    ) -> None:

        """The same tenant check, applied to each selected cost centre."""

        ids = [c.cost_center_name_id for c in row.cost_center if c.cost_center_name_id]

        if not ids:

            return



        found = set(

            db.scalars(

                select(CostCenter.id).where(

                    CostCenter.id.in_(ids),

                    CostCenter.business_id == business_id,

                )

            ).all()

        )

        missing = [str(i) for i in ids if i not in found]

        if missing:

            raise DomainValidationError(

                "Cost Center doesn\'t belong to this business",

                code="process_statement_of_accounts_cost_center_other_company",

                details={"cost_center": missing},

            )



    # ── text defaults ─────────────────────────────────────────────────────

    def _apply_text_defaults(self, row: ProcessStatementOfAccounts) -> None:

        """

        Fill in subject, body and pdf_name when blank. The body wording depends

        on the report: a General Ledger covers a date range, an Accounts

        Receivable runs up to a posting date.

        """

        if not row.subject:

            row.subject = "Statement Of Accounts for {{ customer.customer_name }}"



        if not row.body:

            report = getattr(row.report, "value", row.report)

            if report == "General Ledger":

                body_str = " from {{ doc.from_date }} to {{ doc.to_date }}."

            else:

                body_str = " until {{ doc.posting_date }}."

            row.body = (

                "Hello {{ customer.customer_name }},<br>PFA your Statement Of "

                "Accounts" + body_str

            )



        if not row.pdf_name:

            row.pdf_name = "{{ customer.customer_name }}"



    # ── "Customers not selected." ─────────────────────────────────────────

    def _validate_customers(self, row: ProcessStatementOfAccounts) -> None:

        if not row.customers:

            raise DomainValidationError(

                "Customers not selected.",

                code="process_statement_of_accounts_no_customers",

            )



    # ── the enable_auto_email window ──────────────────────────────────────

    def _apply_auto_email_window(self, row: ProcessStatementOfAccounts) -> None:

        """

        When auto-email is on and the start date has not passed yet, the run

        covers exactly one period: ``to_date`` becomes the start date and

        ``from_date`` runs back by ``filter_duration`` months.

        """

        if not row.enable_auto_email:

            return

        if not row.start_date or row.start_date < dt.date.today():

            return



        row.to_date = row.start_date

        row.from_date = _add_months(row.start_date, -int(row.filter_duration or 0))



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProcessStatementOfAccounts:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ProcessStatementOfAccounts]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ProcessStatementOfAccounts].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_cost_center(

        self, business_id: uuid.UUID, row: ProcessStatementOfAccounts, items: list[dict]

    ) -> None:

        row.cost_center.clear()

        for idx, item in enumerate(items, start=1):

            row.cost_center.append(

                PsoaCostCenter(

                    business_id=business_id,

                    idx=idx,

                    cost_center_name_id=item.get('cost_center_name_id'),

                )

            )



    def _replace_project(

        self, business_id: uuid.UUID, row: ProcessStatementOfAccounts, items: list[dict]

    ) -> None:

        row.project.clear()

        for idx, item in enumerate(items, start=1):

            row.project.append(

                PsoaProject(

                    business_id=business_id,

                    idx=idx,

                    project_name=item.get('project_name'),

                )

            )



    def _replace_cc_to(

        self, business_id: uuid.UUID, row: ProcessStatementOfAccounts, items: list[dict]

    ) -> None:

        row.cc_to.clear()

        for idx, item in enumerate(items, start=1):

            row.cc_to.append(

                ProcessStatementOfAccountsCc(

                    business_id=business_id,

                    idx=idx,

                    cc=item.get('cc'),

                )

            )



    def _replace_customers(

        self, business_id: uuid.UUID, row: ProcessStatementOfAccounts, items: list[dict]

    ) -> None:

        row.customers.clear()

        for idx, item in enumerate(items, start=1):

            row.customers.append(

                ProcessStatementOfAccountsCustomer(

                    business_id=business_id,

                    idx=idx,

                    customer=item.get('customer'),

                    primary_email=item.get('primary_email'),

                    billing_email=item.get('billing_email'),

                    customer_name=item.get('customer_name'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(ProcessStatementOfAccounts).where(

                    ProcessStatementOfAccounts.business_id == business_id

                )

            )

            or 0

        )

        return f"PRO-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: ProcessStatementOfAccountsCreate

    ) -> ProcessStatementOfAccounts:

        row = ProcessStatementOfAccounts(

            business_id=business_id,

            name=self.next_name(db, business_id),

            frequency=payload.frequency,

            from_date=payload.from_date,

            to_date=payload.to_date,

            customer_collection=payload.customer_collection,

            collection_name=payload.collection_name,

            account_id=payload.account_id,

            finance_book_id=payload.finance_book_id,

            orientation=payload.orientation,

            start_date=payload.start_date,

            currency=payload.currency,

            include_ageing=payload.include_ageing,

            ageing_based_on=payload.ageing_based_on,

            enable_auto_email=payload.enable_auto_email,

            primary_mandatory=payload.primary_mandatory,

            filter_duration=payload.filter_duration,

            subject=payload.subject,

            body=payload.body,

            letter_head=payload.letter_head,

            terms_and_conditions=payload.terms_and_conditions,

            include_break=payload.include_break,

            show_net_values_in_party_account=payload.show_net_values_in_party_account,

            sender=payload.sender,

            report=payload.report,

            posting_date=payload.posting_date,

            payment_terms_template_id=payload.payment_terms_template_id,

            sales_partner=payload.sales_partner,

            sales_person=payload.sales_person,

            territory=payload.territory,

            based_on_payment_terms=payload.based_on_payment_terms,

            pdf_name=payload.pdf_name,

            ignore_exchange_rate_revaluation_journals=payload.ignore_exchange_rate_revaluation_journals,

            ignore_cr_dr_notes=payload.ignore_cr_dr_notes,

            show_remarks=payload.show_remarks,

            categorize_by=payload.categorize_by,

            show_future_payments=payload.show_future_payments,

            print_format=payload.print_format,

            show_opening_entries=payload.show_opening_entries,

        )

        self._replace_cost_center(business_id, row, [x.model_dump() for x in payload.cost_center])

        self._replace_project(business_id, row, [x.model_dump() for x in payload.project])

        self._replace_cc_to(business_id, row, [x.model_dump() for x in payload.cc_to])

        self._replace_customers(business_id, row, [x.model_dump() for x in payload.customers])



        try:

            db.flush()  # children need ids before validation reads them

            self._validate(db, business_id, row)

            self.repository.add(db, row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def update(

        self,

        db: Session,

        business_id: uuid.UUID,

        row_id: uuid.UUID,

        payload: ProcessStatementOfAccountsUpdate,

    ) -> ProcessStatementOfAccounts:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "cost_center":

                    self._replace_cost_center(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "project":

                    self._replace_project(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "cc_to":

                    self._replace_cc_to(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "customers":

                    self._replace_customers(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

            db.flush()

            self._validate(db, business_id, row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def delete(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> None:

        row = self._get_or_404(db, business_id, row_id)

        self.repository.delete(db, row)

        db.commit()
