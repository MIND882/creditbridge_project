# HAND-WRITTEN

"""

Business logic for Bisect Accounting Statements -- port of

``erpnext/accounts/doctype/bisect_accounting_statements/bisect_accounting_statements.py``.







Upstream hooks:

    validate

    validate_dates

    bfs

    dfs

    build_tree

    get_report_summary

    update_node

    current_node_has_summary_info

    fetch_summary_info_from_current_node

    fetch_or_calculate

    bisect_left

    bisect_right

    move_up



**Upstream has 1 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.bisect_accounting_statements_domain.models.bisect_accounting_statements import BisectAccountingStatements

from app.accounts.bisect_accounting_statements_domain.repositories.bisect_accounting_statements_repository import (

    BisectAccountingStatementsRepository,

)

from app.accounts.bisect_accounting_statements_domain.schemas.bisect_accounting_statements import (

    BisectAccountingStatementsCreate,

    BisectAccountingStatementsUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BisectAccountingStatementsService"]





class BisectAccountingStatementsService:

    def __init__(self, repository: Optional[BisectAccountingStatementsRepository] = None) -> None:

        self.repository = repository or BisectAccountingStatementsRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> BisectAccountingStatements:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Bisect Accounting Statements", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: BisectAccountingStatements

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

    ) -> BisectAccountingStatements:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[BisectAccountingStatements]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[BisectAccountingStatements].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(BisectAccountingStatements).where(

                    BisectAccountingStatements.business_id == business_id

                )

            )

            or 0

        )

        return f"BIS-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: BisectAccountingStatementsCreate

    ) -> BisectAccountingStatements:

        row = BisectAccountingStatements(

            business_id=business_id,

            name=self.next_name(db, business_id),

            from_date=payload.from_date,

            to_date=payload.to_date,

            algorithm=payload.algorithm,

            current_node=payload.current_node,

            current_from_date=payload.current_from_date,

            current_to_date=payload.current_to_date,

            p_l_summary=payload.p_l_summary,

            b_s_summary=payload.b_s_summary,

            difference=payload.difference,

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

        payload: BisectAccountingStatementsUpdate,

    ) -> BisectAccountingStatements:

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
