# HAND-WRITTEN

"""

Business logic for Bisect Nodes -- port of

``erpnext/accounts/doctype/bisect_nodes/bisect_nodes.py``.







Upstream hooks:

    (none -- upstream's controller defines no hooks)



Upstream declares no validation, so `_validate` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.bisect_nodes_domain.models.bisect_nodes import BisectNodes

from app.accounts.bisect_nodes_domain.repositories.bisect_nodes_repository import (

    BisectNodesRepository,

)

from app.accounts.bisect_nodes_domain.schemas.bisect_nodes import (

    BisectNodesCreate,

    BisectNodesUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BisectNodesService"]





class BisectNodesService:

    def __init__(self, repository: Optional[BisectNodesRepository] = None) -> None:

        self.repository = repository or BisectNodesRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> BisectNodes:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Bisect Nodes", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: BisectNodes

    ) -> None:

        """

        Upstream's controller defines no ``frappe.throw``, so there is

        no rule to port. Empty by design, not by omission.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> BisectNodes:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[BisectNodes]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[BisectNodes].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(BisectNodes).where(

                    BisectNodes.business_id == business_id

                )

            )

            or 0

        )

        return f"BIS-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: BisectNodesCreate

    ) -> BisectNodes:

        row = BisectNodes(

            business_id=business_id,

            name=self.next_name(db, business_id),

            root=payload.root,

            left_child=payload.left_child,

            right_child=payload.right_child,

            period_from_date=payload.period_from_date,

            period_to_date=payload.period_to_date,

            difference=payload.difference,

            balance_sheet_summary=payload.balance_sheet_summary,

            profit_loss_summary=payload.profit_loss_summary,

            generated=payload.generated,

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

        payload: BisectNodesUpdate,

    ) -> BisectNodes:

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
