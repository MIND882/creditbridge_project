"""Business logic for Putaway Rule -- port of

``erpnext/stock/doctype/putaway_rule/putaway_rule.py``.



Upstream has 6 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.putaway_rule_domain.models.putaway_rule import PutawayRule

from app.stock.putaway_rule_domain.repositories.putaway_rule_repository import (

    PutawayRuleRepository,

)

from app.stock.putaway_rule_domain.schemas.putaway_rule import (

    PutawayRuleCreate,

    PutawayRuleUpdate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PutawayRuleService"]





class PutawayRuleService:

    def __init__(self, repository: Optional[PutawayRuleRepository] = None) -> None:

        self.repository = repository or PutawayRuleRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PutawayRule:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Putaway Rule", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: PutawayRule

    ) -> None:

        """

        Upstream has 6 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PutawayRule:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PutawayRule]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PutawayRule].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``PUT-.####``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(PutawayRule).where(

                    PutawayRule.business_id == business_id

                )

            )

            or 0

        )

        return f"PUT-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: PutawayRuleCreate

    ) -> PutawayRule:

        row = PutawayRule(

            business_id=business_id,

            name=self.next_name(db, business_id),

            item_code_id=payload.item_code_id,

            item_name=payload.item_name,

            warehouse_id=payload.warehouse_id,

            capacity=payload.capacity,

            stock_uom_id=payload.stock_uom_id,

            priority=payload.priority,

            company=payload.company,

            disable=payload.disable,

            uom_id=payload.uom_id,

            stock_capacity=payload.stock_capacity,

            conversion_factor=payload.conversion_factor,

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

        payload: PutawayRuleUpdate,

    ) -> PutawayRule:

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
