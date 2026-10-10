"""Business logic for Material Request -- port of

``erpnext/stock/doctype/material_request/material_request.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream has 10 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.material_request_domain.models.material_request import MaterialRequest

from app.stock.material_request_domain.repositories.material_request_repository import (

    MaterialRequestRepository,

)

from app.stock.material_request_domain.schemas.material_request import (

    MaterialRequestCreate,

    MaterialRequestUpdate,

)

from app.stock.material_request_item_domain.models.material_request_item import MaterialRequestItem

from app.core.errors import NotFoundError

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.pagination import ResultPage



__all__ = ["MaterialRequestService"]





class MaterialRequestService:

    def __init__(self, repository: Optional[MaterialRequestRepository] = None) -> None:

        self.repository = repository or MaterialRequestRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> MaterialRequest:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Material Request", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: MaterialRequest

    ) -> None:

        """

        Upstream has 10 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> MaterialRequest:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[MaterialRequest]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[MaterialRequest].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID, series: Optional[str] = None) -> str:

        """A per-tenant sequential name; upstream mints one from ``naming_series``."""

        # ``naming_series`` is optional on input (Frappe fills it from a

        # default), so fall back to the doctype prefix when it is absent.

        series = series or ""

        prefix = series.split(".")[0].split("#")[0]

        if prefix and not prefix.endswith("-"):

            prefix += "-"

        count = int(

            db.scalar(

                select(func.count()).select_from(MaterialRequest).where(

                    MaterialRequest.business_id == business_id

                )

            )

            or 0

        )

        return f"{prefix}{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: MaterialRequestCreate

    ) -> MaterialRequest:

        row = MaterialRequest(

            business_id=business_id,

            name=self.next_name(db, business_id, payload.naming_series),

            naming_series=payload.naming_series,

            title=payload.title,

            material_request_type=payload.material_request_type,

            customer=payload.customer,

            schedule_date=payload.schedule_date,

            company=payload.company,

            amended_from_id=payload.amended_from_id,

            scan_barcode=payload.scan_barcode,

            transaction_date=payload.transaction_date,

            status=payload.status,

            per_ordered=payload.per_ordered,

            per_received=payload.per_received,

            letter_head=payload.letter_head,

            select_print_heading=payload.select_print_heading,

            tc_name=payload.tc_name,

            terms=payload.terms,

            job_card=payload.job_card,

            set_warehouse_id=payload.set_warehouse_id,

            set_from_warehouse_id=payload.set_from_warehouse_id,

            transfer_status=payload.transfer_status,

            work_order=payload.work_order,

            buying_price_list_id=payload.buying_price_list_id,

            last_scanned_warehouse=payload.last_scanned_warehouse,

            auto_created_via_reorder=payload.auto_created_via_reorder,

        )

        self._replace_items(business_id, row, [x.model_dump() for x in payload.items])



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

        payload: MaterialRequestUpdate,

    ) -> MaterialRequest:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "items":

                    self._replace_items(business_id, row, value or [])

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

    ) -> MaterialRequest:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Material Request")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> MaterialRequest:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Material Request")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row



    def _replace_items(

        self, business_id: uuid.UUID, row: MaterialRequest, items: list[dict]

    ) -> None:

        row.items.clear()

        for idx, entry in enumerate(items, start=1):

            row.items.append(

                MaterialRequestItem(

                    business_id=business_id,

                    idx=idx,

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )
