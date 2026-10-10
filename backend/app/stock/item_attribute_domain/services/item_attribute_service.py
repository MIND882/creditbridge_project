"""Business logic for Item Attribute -- port of

``erpnext/stock/doctype/item_attribute/item_attribute.py``.



Upstream has 5 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.item_attribute_domain.models.item_attribute import ItemAttribute

from app.stock.item_attribute_domain.repositories.item_attribute_repository import (

    ItemAttributeRepository,

)

from app.stock.item_attribute_domain.schemas.item_attribute import (

    ItemAttributeCreate,

    ItemAttributeUpdate,

)

from app.stock.item_attribute_value_domain.models.item_attribute_value import ItemAttributeValue

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ItemAttributeService"]





class ItemAttributeService:

    def __init__(self, repository: Optional[ItemAttributeRepository] = None) -> None:

        self.repository = repository or ItemAttributeRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ItemAttribute:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Item Attribute", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: ItemAttribute

    ) -> None:

        """

        Upstream has 5 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ItemAttribute:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ItemAttribute]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ItemAttribute].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    # ``autoname = 'field:attribute_name'``: the name is the value of

    # that field, derived at create time (Frappe derives it on every save;

    # the creation-time value is what migrated documents carry).



    def create(

        self, db: Session, business_id: uuid.UUID, payload: ItemAttributeCreate

    ) -> ItemAttribute:

        row = ItemAttribute(

            business_id=business_id,

            name=payload.attribute_name,

            attribute_name=payload.attribute_name,

            numeric_values=payload.numeric_values,

            from_range=payload.from_range,

            increment=payload.increment,

            to_range=payload.to_range,

            disabled=payload.disabled,

        )

        self._replace_item_attribute_values(business_id, row, [x.model_dump() for x in payload.item_attribute_values])



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

        payload: ItemAttributeUpdate,

    ) -> ItemAttribute:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "item_attribute_values":

                    self._replace_item_attribute_values(business_id, row, value or [])

                    continue

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



    def _replace_item_attribute_values(

        self, business_id: uuid.UUID, row: ItemAttribute, item_attribute_values: list[dict]

    ) -> None:

        row.item_attribute_values.clear()

        for idx, entry in enumerate(item_attribute_values, start=1):

            row.item_attribute_values.append(

                ItemAttributeValue(

                    business_id=business_id,

                    idx=idx,

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )
