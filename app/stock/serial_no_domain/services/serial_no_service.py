"""Business logic for Serial No -- port of

``erpnext/stock/doctype/serial_no/serial_no.py``.



Upstream has 4 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.serial_no_domain.models.serial_no import SerialNo

from app.stock.serial_no_domain.repositories.serial_no_repository import (

    SerialNoRepository,

)

from app.stock.serial_no_domain.schemas.serial_no import (

    SerialNoCreate,

    SerialNoUpdate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SerialNoService"]





class SerialNoService:

    def __init__(self, repository: Optional[SerialNoRepository] = None) -> None:

        self.repository = repository or SerialNoRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SerialNo:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Serial No", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: SerialNo

    ) -> None:

        """

        Upstream has 4 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SerialNo:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[SerialNo]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SerialNo].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    # ``autoname = 'field:serial_no'``: the name is the value of

    # that field, derived at create time (Frappe derives it on every save;

    # the creation-time value is what migrated documents carry).



    def create(

        self, db: Session, business_id: uuid.UUID, payload: SerialNoCreate

    ) -> SerialNo:

        row = SerialNo(

            business_id=business_id,

            name=payload.serial_no,

            serial_no=payload.serial_no,

            item_code_id=payload.item_code_id,

            item_name=payload.item_name,

            description=payload.description,

            item_group_id=payload.item_group_id,

            brand_id=payload.brand_id,

            asset=payload.asset,

            asset_status=payload.asset_status,

            location=payload.location,

            employee=payload.employee,

            maintenance_status=payload.maintenance_status,

            warranty_period=payload.warranty_period,

            warranty_expiry_date=payload.warranty_expiry_date,

            amc_expiry_date=payload.amc_expiry_date,

            company=payload.company,

            work_order=payload.work_order,

            warehouse_id=payload.warehouse_id,

            batch_no_id=payload.batch_no_id,

            purchase_rate=payload.purchase_rate,

            status=payload.status,

            customer=payload.customer,

            reference_doctype=payload.reference_doctype,

            reference_name=payload.reference_name,

            posting_date=payload.posting_date,

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

        payload: SerialNoUpdate,

    ) -> SerialNo:

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
