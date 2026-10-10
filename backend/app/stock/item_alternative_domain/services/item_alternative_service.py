"""Business logic for Item Alternative -- port of

``erpnext/stock/doctype/item_alternative/item_alternative.py``.



Upstream has 5 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.item_alternative_domain.models.item_alternative import ItemAlternative

from app.stock.item_alternative_domain.repositories.item_alternative_repository import (

    ItemAlternativeRepository,

)

from app.stock.item_alternative_domain.schemas.item_alternative import (

    ItemAlternativeCreate,

    ItemAlternativeUpdate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ItemAlternativeService"]





class ItemAlternativeService:

    def __init__(self, repository: Optional[ItemAlternativeRepository] = None) -> None:

        self.repository = repository or ItemAlternativeRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ItemAlternative:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Item Alternative", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: ItemAlternative

    ) -> None:

        """

        Upstream has 5 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ItemAlternative:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ItemAlternative]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ItemAlternative].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(ItemAlternative).where(

                    ItemAlternative.business_id == business_id

                )

            )

            or 0

        )

        return f"ITE-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: ItemAlternativeCreate

    ) -> ItemAlternative:

        row = ItemAlternative(

            business_id=business_id,

            name=self.next_name(db, business_id),

            item_code_id=payload.item_code_id,

            alternative_item_code_id=payload.alternative_item_code_id,

            two_way=payload.two_way,

            item_name=payload.item_name,

            alternative_item_name=payload.alternative_item_name,

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

        payload: ItemAlternativeUpdate,

    ) -> ItemAlternative:

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
