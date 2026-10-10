"""Business logic for Warehouse -- port of

``erpnext/stock/doctype/warehouse/warehouse.py``.



Upstream has 3 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.warehouse_domain.models.warehouse import Warehouse

from app.stock.warehouse_domain.repositories.warehouse_repository import (

    WarehouseRepository,

)

from app.stock.warehouse_domain.schemas.warehouse import (

    WarehouseCreate,

    WarehouseUpdate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["WarehouseService"]





class WarehouseService:

    def __init__(self, repository: Optional[WarehouseRepository] = None) -> None:

        self.repository = repository or WarehouseRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Warehouse:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Warehouse", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: Warehouse

    ) -> None:

        """

        Upstream has 3 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Warehouse:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[Warehouse]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[Warehouse].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(Warehouse).where(

                    Warehouse.business_id == business_id

                )

            )

            or 0

        )

        return f"WAR-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: WarehouseCreate

    ) -> Warehouse:

        row = Warehouse(

            business_id=business_id,

            name=self.next_name(db, business_id),

            warehouse_name=payload.warehouse_name,

            is_group=payload.is_group,

            company=payload.company,

            disabled=payload.disabled,

            account_id=payload.account_id,

            email_id=payload.email_id,

            phone_no=payload.phone_no,

            mobile_no=payload.mobile_no,

            address_line_1=payload.address_line_1,

            address_line_2=payload.address_line_2,

            city=payload.city,

            state=payload.state,

            pin=payload.pin,

            parent_warehouse_id=payload.parent_warehouse_id,

            lft=payload.lft,

            rgt=payload.rgt,

            old_parent_id=payload.old_parent_id,

            warehouse_type_id=payload.warehouse_type_id,

            default_in_transit_warehouse_id=payload.default_in_transit_warehouse_id,

            is_rejected_warehouse=payload.is_rejected_warehouse,

            customer=payload.customer,

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

        payload: WarehouseUpdate,

    ) -> Warehouse:

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
