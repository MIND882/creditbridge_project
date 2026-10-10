"""Business logic for Serial and Batch Bundle -- port of

``erpnext/stock/doctype/serial_and_batch_bundle/serial_and_batch_bundle.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream has 22 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.serial_and_batch_bundle_domain.models.serial_and_batch_bundle import SerialAndBatchBundle

from app.stock.serial_and_batch_bundle_domain.repositories.serial_and_batch_bundle_repository import (

    SerialAndBatchBundleRepository,

)

from app.stock.serial_and_batch_bundle_domain.schemas.serial_and_batch_bundle import (

    SerialAndBatchBundleCreate,

    SerialAndBatchBundleUpdate,

)

from app.stock.serial_and_batch_entry_domain.models.serial_and_batch_entry import SerialAndBatchEntry

from app.core.errors import NotFoundError

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.pagination import ResultPage



__all__ = ["SerialAndBatchBundleService"]





class SerialAndBatchBundleService:

    def __init__(self, repository: Optional[SerialAndBatchBundleRepository] = None) -> None:

        self.repository = repository or SerialAndBatchBundleRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SerialAndBatchBundle:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Serial and Batch Bundle", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: SerialAndBatchBundle

    ) -> None:

        """

        Upstream has 22 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SerialAndBatchBundle:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[SerialAndBatchBundle]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SerialAndBatchBundle].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def create(

        self, db: Session, business_id: uuid.UUID, payload: SerialAndBatchBundleCreate

    ) -> SerialAndBatchBundle:

        row = SerialAndBatchBundle(

            business_id=business_id,

            company=payload.company,

            item_group_id=payload.item_group_id,

            has_serial_no=payload.has_serial_no,

            item_code_id=payload.item_code_id,

            item_name=payload.item_name,

            has_batch_no=payload.has_batch_no,

            voucher_type=payload.voucher_type,

            voucher_no=payload.voucher_no,

            is_cancelled=payload.is_cancelled,

            amended_from_id=payload.amended_from_id,

            avg_rate=payload.avg_rate,

            total_amount=payload.total_amount,

            total_qty=payload.total_qty,

            warehouse_id=payload.warehouse_id,

            type_of_transaction=payload.type_of_transaction,

            is_rejected=payload.is_rejected,

            voucher_detail_no=payload.voucher_detail_no,

            returned_against=payload.returned_against,

            naming_series=payload.naming_series,

            is_packed=payload.is_packed,

            posting_datetime=payload.posting_datetime,

        )

        self._replace_entries(business_id, row, [x.model_dump() for x in payload.entries])



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

        payload: SerialAndBatchBundleUpdate,

    ) -> SerialAndBatchBundle:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "entries":

                    self._replace_entries(business_id, row, value or [])

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



    def submit(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SerialAndBatchBundle:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Serial and Batch Bundle")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SerialAndBatchBundle:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Serial and Batch Bundle")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row



    def _replace_entries(

        self, business_id: uuid.UUID, row: SerialAndBatchBundle, entries: list[dict]

    ) -> None:

        row.entries.clear()

        for idx, entry in enumerate(entries, start=1):

            row.entries.append(

                SerialAndBatchEntry(

                    business_id=business_id,

                    idx=idx,

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )
