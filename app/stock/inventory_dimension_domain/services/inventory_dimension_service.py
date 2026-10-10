"""Business logic for Inventory Dimension -- port of

``erpnext/stock/doctype/inventory_dimension/inventory_dimension.py``.



Upstream has 3 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.inventory_dimension_domain.models.inventory_dimension import InventoryDimension

from app.stock.inventory_dimension_domain.repositories.inventory_dimension_repository import (

    InventoryDimensionRepository,

)

from app.stock.inventory_dimension_domain.schemas.inventory_dimension import (

    InventoryDimensionCreate,

    InventoryDimensionUpdate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["InventoryDimensionService"]





class InventoryDimensionService:

    def __init__(self, repository: Optional[InventoryDimensionRepository] = None) -> None:

        self.repository = repository or InventoryDimensionRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> InventoryDimension:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Inventory Dimension", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: InventoryDimension

    ) -> None:

        """

        Upstream has 3 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> InventoryDimension:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[InventoryDimension]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[InventoryDimension].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    # ``autoname = 'field:dimension_name'``: the name is the value of

    # that field, derived at create time (Frappe derives it on every save;

    # the creation-time value is what migrated documents carry).



    def create(

        self, db: Session, business_id: uuid.UUID, payload: InventoryDimensionCreate

    ) -> InventoryDimension:

        row = InventoryDimension(

            business_id=business_id,

            name=payload.dimension_name,

            reference_document=payload.reference_document,

            dimension_name=payload.dimension_name,

            document_type=payload.document_type,

            istable=payload.istable,

            condition=payload.condition,

            apply_to_all_doctypes=payload.apply_to_all_doctypes,

            target_fieldname=payload.target_fieldname,

            source_fieldname=payload.source_fieldname,

            type_of_transaction=payload.type_of_transaction,

            fetch_from_parent=payload.fetch_from_parent,

            mandatory_depends_on=payload.mandatory_depends_on,

            reqd=payload.reqd,

            validate_negative_stock=payload.validate_negative_stock,

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

        payload: InventoryDimensionUpdate,

    ) -> InventoryDimension:

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
