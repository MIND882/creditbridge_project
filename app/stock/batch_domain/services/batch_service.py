"""Business logic for Batch -- port of

``erpnext/stock/doctype/batch/batch.py``.



Upstream has 5 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.batch_domain.models.batch import Batch

from app.stock.batch_domain.repositories.batch_repository import (

    BatchRepository,

)

from app.stock.batch_domain.schemas.batch import (

    BatchCreate,

    BatchUpdate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BatchService"]





class BatchService:

    def __init__(self, repository: Optional[BatchRepository] = None) -> None:

        self.repository = repository or BatchRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Batch:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Batch", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: Batch

    ) -> None:

        """

        Upstream has 5 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Batch:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[Batch]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[Batch].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    # ``autoname = 'field:batch_id'``: the name is the value of

    # that field, derived at create time (Frappe derives it on every save;

    # the creation-time value is what migrated documents carry).



    def create(

        self, db: Session, business_id: uuid.UUID, payload: BatchCreate

    ) -> Batch:

        row = Batch(

            business_id=business_id,

            name=payload.batch_id,

            disabled=payload.disabled,

            batch_id=payload.batch_id,

            item_id=payload.item_id,

            image=payload.image,

            parent_batch_id=payload.parent_batch_id,

            manufacturing_date=payload.manufacturing_date,

            expiry_date=payload.expiry_date,

            supplier=payload.supplier,

            reference_doctype=payload.reference_doctype,

            reference_name=payload.reference_name,

            description=payload.description,

            item_name=payload.item_name,

            batch_qty=payload.batch_qty,

            stock_uom_id=payload.stock_uom_id,

            qty_to_produce=payload.qty_to_produce,

            produced_qty=payload.produced_qty,

            use_batchwise_valuation=payload.use_batchwise_valuation,

            allow_negative_stock_for_batch=payload.allow_negative_stock_for_batch,

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

        payload: BatchUpdate,

    ) -> Batch:

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
