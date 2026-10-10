# HAND-WRITTEN

"""

Business logic for Bank Reconciliation Tool -- port of

``erpnext/accounts/doctype/bank_reconciliation_tool/bank_reconciliation_tool.py``.







Upstream hooks:

    (none -- upstream's controller defines no hooks)



**Upstream has 1 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.bank_reconciliation_tool_domain.models.bank_reconciliation_tool import BankReconciliationTool

from app.accounts.bank_reconciliation_tool_domain.repositories.bank_reconciliation_tool_repository import (

    BankReconciliationToolRepository,

)

from app.accounts.bank_reconciliation_tool_domain.schemas.bank_reconciliation_tool import (

    BankReconciliationToolCreate,

    BankReconciliationToolUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BankReconciliationToolService"]





class BankReconciliationToolService:

    def __init__(self, repository: Optional[BankReconciliationToolRepository] = None) -> None:

        self.repository = repository or BankReconciliationToolRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> BankReconciliationTool:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Bank Reconciliation Tool", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: BankReconciliationTool

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

    ) -> BankReconciliationTool:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[BankReconciliationTool]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[BankReconciliationTool].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(BankReconciliationTool).where(

                    BankReconciliationTool.business_id == business_id

                )

            )

            or 0

        )

        return f"BAN-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: BankReconciliationToolCreate

    ) -> BankReconciliationTool:

        row = BankReconciliationTool(

            business_id=business_id,

            name=self.next_name(db, business_id),

            bank_account_id=payload.bank_account_id,

            bank_statement_from_date=payload.bank_statement_from_date,

            bank_statement_to_date=payload.bank_statement_to_date,

            account_opening_balance=payload.account_opening_balance,

            bank_statement_closing_balance=payload.bank_statement_closing_balance,

            from_reference_date=payload.from_reference_date,

            to_reference_date=payload.to_reference_date,

            filter_by_reference_date=payload.filter_by_reference_date,

            account_currency=payload.account_currency,

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

        payload: BankReconciliationToolUpdate,

    ) -> BankReconciliationTool:

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
