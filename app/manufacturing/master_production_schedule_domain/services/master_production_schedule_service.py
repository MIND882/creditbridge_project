"""Business logic for Master Production Schedule -- port of

``erpnext/manufacturing/doctype/master_production_schedule/master_production_schedule.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.master_production_schedule_domain.models.master_production_schedule import MasterProductionSchedule

from app.manufacturing.master_production_schedule_domain.repositories.master_production_schedule_repository import (

    MasterProductionScheduleRepository,

)

from app.manufacturing.master_production_schedule_domain.schemas.master_production_schedule import (

    MasterProductionScheduleCreate,

    MasterProductionScheduleUpdate,

)

from app.manufacturing.production_plan_sales_order_domain.models.production_plan_sales_order import ProductionPlanSalesOrder

from app.manufacturing.production_plan_material_request_domain.models.production_plan_material_request import ProductionPlanMaterialRequest

from app.manufacturing.master_production_schedule_item_domain.models.master_production_schedule_item import MasterProductionScheduleItem

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["MasterProductionScheduleService"]





class MasterProductionScheduleService:

    def __init__(self, repository: Optional[MasterProductionScheduleRepository] = None) -> None:

        self.repository = repository or MasterProductionScheduleRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> MasterProductionSchedule:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Master Production Schedule", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: MasterProductionSchedule

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> MasterProductionSchedule:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[MasterProductionSchedule]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[MasterProductionSchedule].build(

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

                select(func.count()).select_from(MasterProductionSchedule).where(

                    MasterProductionSchedule.business_id == business_id

                )

            )

            or 0

        )

        return f"{prefix}{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: MasterProductionScheduleCreate

    ) -> MasterProductionSchedule:

        row = MasterProductionSchedule(

            business_id=business_id,

            name=self.next_name(db, business_id, payload.naming_series),

            naming_series=payload.naming_series,

            company=payload.company,

            posting_date=payload.posting_date,

            from_date=payload.from_date,

            to_date=payload.to_date,

            parent_warehouse_id=payload.parent_warehouse_id,

            sales_forecast_id=payload.sales_forecast_id,

            amended_from_id=payload.amended_from_id,

        )

        self._replace_sales_orders(business_id, row, [x.model_dump() for x in payload.sales_orders])

        self._replace_material_requests(business_id, row, [x.model_dump() for x in payload.material_requests])

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

        payload: MasterProductionScheduleUpdate,

    ) -> MasterProductionSchedule:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "sales_orders":

                    self._replace_sales_orders(business_id, row, value or [])

                    continue

                if field_name == "material_requests":

                    self._replace_material_requests(business_id, row, value or [])

                    continue

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



    def _replace_sales_orders(

        self, business_id: uuid.UUID, row: MasterProductionSchedule, sales_orders: list[dict]

    ) -> None:

        row.sales_orders.clear()

        for idx, entry in enumerate(sales_orders, start=1):

            row.sales_orders.append(

                ProductionPlanSalesOrder(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Master Production Schedule",

                    parentfield="sales_orders",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_material_requests(

        self, business_id: uuid.UUID, row: MasterProductionSchedule, material_requests: list[dict]

    ) -> None:

        row.material_requests.clear()

        for idx, entry in enumerate(material_requests, start=1):

            row.material_requests.append(

                ProductionPlanMaterialRequest(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Master Production Schedule",

                    parentfield="material_requests",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_items(

        self, business_id: uuid.UUID, row: MasterProductionSchedule, items: list[dict]

    ) -> None:

        row.items.clear()

        for idx, entry in enumerate(items, start=1):

            row.items.append(

                MasterProductionScheduleItem(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Master Production Schedule",

                    parentfield="items",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )
