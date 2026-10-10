# HAND-WRITTEN

"""

Business logic for Account Closing Balance -- port of

``erpnext/accounts/doctype/account_closing_balance/account_closing_balance.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream hooks:

    (none -- upstream's controller defines no hooks)



**Upstream has 1 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.account_closing_balance_domain.models.account_closing_balance import AccountClosingBalance

from app.accounts.account_closing_balance_domain.repositories.account_closing_balance_repository import (

    AccountClosingBalanceRepository,

)

from app.accounts.account_closing_balance_domain.schemas.account_closing_balance import (

    AccountClosingBalanceCreate,

    AccountClosingBalanceUpdate,

)

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["AccountClosingBalanceService"]





class AccountClosingBalanceService:

    def __init__(self, repository: Optional[AccountClosingBalanceRepository] = None) -> None:

        self.repository = repository or AccountClosingBalanceRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> AccountClosingBalance:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Account Closing Balance", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: AccountClosingBalance

    ) -> None:

        """

        TODO(PORT-VALIDATION): upstream validation is NOT ported.



        This controller has **1 ``frappe.throw`` site(s)** upstream.

        None are enforced here, so writes upstream would reject

        currently succeed. It fails open deliberately rather than

        blocking the CRUD surface, but must not be read as complete.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> AccountClosingBalance:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[AccountClosingBalance]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[AccountClosingBalance].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(AccountClosingBalance).where(

                    AccountClosingBalance.business_id == business_id

                )

            )

            or 0

        )

        return f"ACC-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: AccountClosingBalanceCreate

    ) -> AccountClosingBalance:

        row = AccountClosingBalance(

            business_id=business_id,

            name=self.next_name(db, business_id),

            closing_date=payload.closing_date,

            account_id=payload.account_id,

            cost_center_id=payload.cost_center_id,

            debit=payload.debit,

            credit=payload.credit,

            account_currency=payload.account_currency,

            debit_in_account_currency=payload.debit_in_account_currency,

            credit_in_account_currency=payload.credit_in_account_currency,

            project=payload.project,

            finance_book_id=payload.finance_book_id,

            period_closing_voucher=payload.period_closing_voucher,

            is_period_closing_voucher_entry=payload.is_period_closing_voucher_entry,

            debit_in_reporting_currency=payload.debit_in_reporting_currency,

            credit_in_reporting_currency=payload.credit_in_reporting_currency,

            reporting_currency_exchange_rate=payload.reporting_currency_exchange_rate,

        )



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

        payload: AccountClosingBalanceUpdate,

    ) -> AccountClosingBalance:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

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



    def submit(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> AccountClosingBalance:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Account Closing Balance")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> AccountClosingBalance:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Account Closing Balance")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row
