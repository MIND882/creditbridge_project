"""Business logic for Item Price -- port of

``erpnext/stock/doctype/item_price/item_price.py``.



Upstream has 5 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.item_price_domain.models.item_price import ItemPrice

from app.stock.item_price_domain.repositories.item_price_repository import (

    ItemPriceRepository,

)

from app.stock.item_price_domain.schemas.item_price import (

    ItemPriceCreate,

    ItemPriceUpdate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ItemPriceService"]





class ItemPriceService:

    def __init__(self, repository: Optional[ItemPriceRepository] = None) -> None:

        self.repository = repository or ItemPriceRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ItemPrice:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Item Price", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: ItemPrice

    ) -> None:

        """

        Upstream has 5 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ItemPrice:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ItemPrice]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ItemPrice].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def create(

        self, db: Session, business_id: uuid.UUID, payload: ItemPriceCreate

    ) -> ItemPrice:

        row = ItemPrice(

            business_id=business_id,

            item_code_id=payload.item_code_id,

            uom_id=payload.uom_id,

            packing_unit=payload.packing_unit,

            item_name=payload.item_name,

            brand_id=payload.brand_id,

            item_description=payload.item_description,

            price_list_id=payload.price_list_id,

            customer=payload.customer,

            supplier=payload.supplier,

            buying=payload.buying,

            selling=payload.selling,

            currency=payload.currency,

            price_list_rate=payload.price_list_rate,

            valid_from=payload.valid_from,

            lead_time_days=payload.lead_time_days,

            valid_upto=payload.valid_upto,

            note=payload.note,

            reference=payload.reference,

            batch_no_id=payload.batch_no_id,

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

        payload: ItemPriceUpdate,

    ) -> ItemPrice:

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
