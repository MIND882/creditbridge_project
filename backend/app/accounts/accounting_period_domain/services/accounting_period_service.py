"""

Business logic for Accounting Period -- port of

``erpnext/accounts/doctype/accounting_period/accounting_period.py``.



Upstream hook -> here

-------------------

``autoname`` (period_name - abbr)   :meth:`_build_name`

``validate``                        :meth:`_validate` (same order)

``validate_dates``                  :meth:`_validate_dates`

``validate_overlap``                :meth:`_validate_overlap`

``bootstrap_doctypes_for_closing``  :meth:`_bootstrap_closed_documents`

``validate_accounting_period_on_doc_save``  :meth:`assert_period_open`



``frappe.get_hooks("period_closing_doctypes")`` collects the closable doctypes

from every installed app. There is no app-registry here, so

``DEFAULT_CLOSING_DOCTYPES`` is the explicit equivalent -- a module-level list

other domains can extend.

"""



from __future__ import annotations



import uuid

from datetime import date

from typing import Optional, Sequence



from sqlalchemy.orm import Session



from app.accounts.accounting_period_domain.models.accounting_period import (

    AccountingPeriod,

    ClosedDocument,

)

from app.accounts.accounting_period_domain.repositories.accounting_period_repository import (

    AccountingPeriodRepository,

)

from app.accounts.accounting_period_domain.schemas.accounting_period import (

    AccountingPeriodCreate,

    AccountingPeriodUpdate,

)

from app.core.errors import ConflictError, DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = [

    "AccountingPeriodService",

    "DEFAULT_CLOSING_DOCTYPES",

    "ClosedAccountingPeriodError",

]



#: Port of the ``period_closing_doctypes`` hook. Upstream this is gathered from

#: every installed app's hooks.py; listed explicitly here.

DEFAULT_CLOSING_DOCTYPES: tuple[str, ...] = (

    "Sales Invoice",

    "Purchase Invoice",

    "Payment Entry",

    "Journal Entry",

    "Stock Entry",

    "Delivery Note",

    "Purchase Receipt",

)





class ClosedAccountingPeriodError(DomainValidationError):

    """

    Port of ``erpnext``'s ``ClosedAccountingPeriod`` ValidationError.



    Distinct class so callers posting dated documents can catch this one

    specifically instead of matching on a message.

    """



    def __init__(self, message: str, period_name: str) -> None:

        super().__init__(message, code="accounting_period_closed")

        self.period_name = period_name





class AccountingPeriodService:

    def __init__(

        self,

        repository: Optional[AccountingPeriodRepository] = None,

        *,

        company_abbr: Optional[str] = None,

        closing_doctypes: Sequence[str] = DEFAULT_CLOSING_DOCTYPES,

        today: Optional[date] = None,

    ) -> None:

        self.repository = repository or AccountingPeriodRepository()

        self.company_abbr = company_abbr

        self.closing_doctypes = tuple(closing_doctypes)

        #: Injectable so the "no future periods" rule is testable without

        #: monkeypatching the clock. Defaults to the real current date.

        self._today = today



    # ── helpers ──────────────────────────────────────────────────────────────

    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, period_id: uuid.UUID

    ) -> AccountingPeriod:

        row = self.repository.get_by_id(db, business_id, period_id)

        if row is None:

            raise NotFoundError("Accounting Period", period_id)

        return row



    @property

    def today(self) -> date:

        return self._today or date.today()



    def _build_name(self, period_name: str) -> str:

        """Port of ``autoname``: ``" - ".join([period_name, company_abbr])``."""

        parts = [period_name.strip()]

        if self.company_abbr and self.company_abbr.strip():

            parts.append(self.company_abbr.strip())

        return " - ".join(parts)



    def _bootstrap_closed_documents(self) -> list[ClosedDocument]:

        """

        Port of ``bootstrap_doctypes_for_closing``.



        Upstream only fills the child table when it is empty, so an explicit

        client-supplied list always wins.

        """

        return [

            ClosedDocument(document_type=dt, closed=True, idx=i)

            for i, dt in enumerate(self.closing_doctypes, start=1)

        ]



    # ── ported validators ────────────────────────────────────────────────────

    def _validate_dates(self, start_date: date, end_date: date) -> None:

        """

        Port of ``validate_dates`` -- two throws.



        Order matters and is preserved: the ordering check first, then the

        future check.

        """

        if start_date > end_date:

            raise DomainValidationError(

                "Start Date cannot be after End Date",

                code="accounting_period_start_after_end",

            )

        if end_date > self.today:

            raise DomainValidationError(

                f"Accounting Period cannot be created for a future date. "

                f"End Date {end_date} is after today.",

                code="accounting_period_end_in_future",

            )



    def _validate_overlap(

        self,

        db: Session,

        business_id: uuid.UUID,

        start_date: date,

        end_date: date,

        *,

        exclude_id: Optional[uuid.UUID] = None,

    ) -> None:

        """Port of ``validate_overlap`` (``OverlapError``)."""

        clash = self.repository.find_overlapping(

            db, business_id, start_date, end_date, exclude_id=exclude_id

        )

        if clash is not None:

            raise ConflictError(

                f"Accounting Period overlaps with {clash.name}",

                code="accounting_period_overlap",

                details={"overlaps_with": clash.name},

            )



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, period_id: uuid.UUID

    ) -> AccountingPeriod:

        return self._get_or_404(db, business_id, period_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[AccountingPeriod]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[AccountingPeriod].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def create(

        self, db: Session, business_id: uuid.UUID, payload: AccountingPeriodCreate

    ) -> AccountingPeriod:

        self._validate_dates(payload.start_date, payload.end_date)

        self._validate_overlap(db, business_id, payload.start_date, payload.end_date)



        period = AccountingPeriod(

            business_id=business_id,

            name=self._build_name(payload.period_name),

            period_name=payload.period_name,

            start_date=payload.start_date,

            end_date=payload.end_date,

            disabled=payload.disabled,

            exempted_role=payload.exempted_role,

        )



        # bootstrap_doctypes_for_closing: only when the client sent none.

        if payload.closed_documents:

            for idx, row in enumerate(payload.closed_documents, start=1):

                period.closed_documents.append(

                    ClosedDocument(

                        business_id=business_id,

                        idx=idx,

                        document_type=row.document_type,

                        closed=row.closed,

                    )

                )

        else:

            for row in self._bootstrap_closed_documents():

                row.business_id = business_id

                period.closed_documents.append(row)



        try:

            self.repository.add(db, period)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(period)

        return period



    def update(

        self,

        db: Session,

        business_id: uuid.UUID,

        period_id: uuid.UUID,

        payload: AccountingPeriodUpdate,

    ) -> AccountingPeriod:

        period = self._get_or_404(db, business_id, period_id)

        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return period



        try:

            for field_name in ("period_name", "start_date", "end_date", "disabled", "exempted_role"):

                if field_name in changes:

                    setattr(period, field_name, changes[field_name])



            if "period_name" in changes:

                period.name = self._build_name(period.period_name)



            if "closed_documents" in changes:

                period.closed_documents.clear()

                for idx, row in enumerate(changes["closed_documents"] or [], start=1):

                    period.closed_documents.append(

                        ClosedDocument(

                            business_id=business_id,

                            idx=idx,

                            document_type=row["document_type"],

                            closed=row["closed"],

                        )

                    )



            self._validate_dates(period.start_date, period.end_date)

            self._validate_overlap(

                db, business_id, period.start_date, period.end_date, exclude_id=period.id

            )

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(period)

        return period



    def delete(self, db: Session, business_id: uuid.UUID, period_id: uuid.UUID) -> None:

        period = self._get_or_404(db, business_id, period_id)

        self.repository.delete(db, period)

        db.commit()



    # ── the guard other domains call ─────────────────────────────────────────

    def assert_period_open(

        self,

        db: Session,

        business_id: uuid.UUID,

        document_type: str,

        posting_date: date,

        *,

        actor_roles: Sequence[str] = (),

    ) -> None:

        """

        Port of the module-level ``validate_accounting_period_on_doc_save``.



        Refuses to let a dated document be written inside a closed period,

        unless the actor holds the period's ``exempted_role``. Other domains

        (Sales Invoice, Payment Entry, ...) call this before saving.

        """

        period = self.repository.find_period_for_date(

            db, business_id, document_type, posting_date

        )

        if period is None:

            return



        if period.exempted_role and period.exempted_role in actor_roles:

            return



        raise ClosedAccountingPeriodError(

            f"You cannot create a {document_type} within the closed "

            f"Accounting Period {period.name}",

            period_name=period.name,

        )
