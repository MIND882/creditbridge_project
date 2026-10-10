"""Business logic for Item Manufacturer -- port of

``erpnext/stock/doctype/item_manufacturer/item_manufacturer.py``.



Upstream has 1 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.item_manufacturer_domain.models.item_manufacturer import ItemManufacturer

from app.stock.item_manufacturer_domain.repositories.item_manufacturer_repository import (

    ItemManufacturerRepository,

)

from app.stock.item_manufacturer_domain.schemas.item_manufacturer import (

    ItemManufacturerCreate,

    ItemManufacturerUpdate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ItemManufacturerService"]





class ItemManufacturerService:

    def __init__(self, repository: Optional[ItemManufacturerRepository] = None) -> None:

        self.repository = repository or ItemManufacturerRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ItemManufacturer:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Item Manufacturer", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: ItemManufacturer

    ) -> None:

        """

        Upstream has 1 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ItemManufacturer:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ItemManufacturer]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ItemManufacturer].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(ItemManufacturer).where(

                    ItemManufacturer.business_id == business_id

                )

            )

            or 0

        )

        return f"ITE-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: ItemManufacturerCreate

    ) -> ItemManufacturer:

        row = ItemManufacturer(

            business_id=business_id,

            name=self.next_name(db, business_id),

            manufacturer_id=payload.manufacturer_id,

            manufacturer_part_no=payload.manufacturer_part_no,

            item_code_id=payload.item_code_id,

            item_name=payload.item_name,

            description=payload.description,

            is_default=payload.is_default,

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

        payload: ItemManufacturerUpdate,

    ) -> ItemManufacturer:

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
