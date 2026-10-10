"""Business logic for Pick List -- port of

``erpnext/stock/doctype/pick_list/pick_list.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream has 15 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.pick_list_domain.models.pick_list import PickList

from app.stock.pick_list_domain.repositories.pick_list_repository import (

    PickListRepository,

)

from app.stock.pick_list_domain.schemas.pick_list import (

    PickListCreate,

    PickListUpdate,

)

from app.stock.pick_list_item_domain.models.pick_list_item import PickListItem

from app.core.errors import NotFoundError

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.pagination import ResultPage



__all__ = ["PickListService"]





class PickListService:

    def __init__(self, repository: Optional[PickListRepository] = None) -> None:

        self.repository = repository or PickListRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PickList:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Pick List", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: PickList

    ) -> None:

        """

        Upstream has 15 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PickList:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PickList]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PickList].build(

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

                select(func.count()).select_from(PickList).where(

                    PickList.business_id == business_id

                )

            )

            or 0

        )

        return f"{prefix}{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: PickListCreate

    ) -> PickList:

        row = PickList(

            business_id=business_id,

            name=self.next_name(db, business_id, payload.naming_series),

            company=payload.company,

            parent_warehouse_id=payload.parent_warehouse_id,

            customer=payload.customer,

            work_order=payload.work_order,

            for_qty=payload.for_qty,

            amended_from_id=payload.amended_from_id,

            purpose=payload.purpose,

            material_request_id=payload.material_request_id,

            naming_series=payload.naming_series,

            group_same_items=payload.group_same_items,

            scan_barcode=payload.scan_barcode,

            scan_mode=payload.scan_mode,

            prompt_qty=payload.prompt_qty,

            customer_name=payload.customer_name,

            status=payload.status,

            consider_rejected_warehouses=payload.consider_rejected_warehouses,

            pick_manually=payload.pick_manually,

            ignore_pricing_rule=payload.ignore_pricing_rule,

            delivery_status=payload.delivery_status,

            per_delivered=payload.per_delivered,

        )

        self._replace_locations(business_id, row, [x.model_dump() for x in payload.locations])



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

        payload: PickListUpdate,

    ) -> PickList:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "locations":

                    self._replace_locations(business_id, row, value or [])

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

    ) -> PickList:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Pick List")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PickList:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Pick List")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row



    def _replace_locations(

        self, business_id: uuid.UUID, row: PickList, locations: list[dict]

    ) -> None:

        row.locations.clear()

        for idx, entry in enumerate(locations, start=1):

            row.locations.append(

                PickListItem(

                    business_id=business_id,

                    idx=idx,

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )
