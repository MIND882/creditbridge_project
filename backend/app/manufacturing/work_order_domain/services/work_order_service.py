"""Business logic for Work Order -- port of

``erpnext/manufacturing/doctype/work_order/work_order.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.work_order_domain.models.work_order import WorkOrder

from app.manufacturing.work_order_domain.repositories.work_order_repository import (

    WorkOrderRepository,

)

from app.manufacturing.work_order_domain.schemas.work_order import (

    WorkOrderCreate,

    WorkOrderUpdate,

)

from app.manufacturing.work_order_operation_domain.models.work_order_operation import WorkOrderOperation

from app.manufacturing.work_order_item_domain.models.work_order_item import WorkOrderItem

from app.manufacturing.work_order_additional_item_domain.models.work_order_additional_item import WorkOrderAdditionalItem

from app.manufacturing.work_order_additional_item_domain.models.work_order_additional_item import WorkOrderAdditionalItem

from app.core.errors import NotFoundError

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.pagination import ResultPage



__all__ = ["WorkOrderService"]





class WorkOrderService:

    def __init__(self, repository: Optional[WorkOrderRepository] = None) -> None:

        self.repository = repository or WorkOrderRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> WorkOrder:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Work Order", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: WorkOrder

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> WorkOrder:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[WorkOrder]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[WorkOrder].build(

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

                select(func.count()).select_from(WorkOrder).where(

                    WorkOrder.business_id == business_id

                )

            )

            or 0

        )

        return f"{prefix}{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: WorkOrderCreate

    ) -> WorkOrder:

        row = WorkOrder(

            business_id=business_id,

            name=self.next_name(db, business_id, payload.naming_series),

            company=payload.company,

            naming_series=payload.naming_series,

            production_item_id=payload.production_item_id,

            bom_no_id=payload.bom_no_id,

            qty=payload.qty,

            sales_order_id=payload.sales_order_id,

            reserve_stock=payload.reserve_stock,

            max_producible_qty=payload.max_producible_qty,

            material_transferred_for_manufacturing=payload.material_transferred_for_manufacturing,

            additional_transferred_qty=payload.additional_transferred_qty,

            produced_qty=payload.produced_qty,

            process_loss_qty=payload.process_loss_qty,

            disassembled_qty=payload.disassembled_qty,

            source_warehouse_id=payload.source_warehouse_id,

            wip_warehouse_id=payload.wip_warehouse_id,

            fg_warehouse_id=payload.fg_warehouse_id,

            scrap_warehouse_id=payload.scrap_warehouse_id,

            transfer_material_against=payload.transfer_material_against,

            allow_alternative_item=payload.allow_alternative_item,

            use_multi_level_bom=payload.use_multi_level_bom,

            skip_transfer=payload.skip_transfer,

            from_wip_warehouse=payload.from_wip_warehouse,

            update_consumed_material_cost_in_project=payload.update_consumed_material_cost_in_project,

            planned_start_date=payload.planned_start_date,

            planned_end_date=payload.planned_end_date,

            expected_delivery_date=payload.expected_delivery_date,

            actual_start_date=payload.actual_start_date,

            actual_end_date=payload.actual_end_date,

            lead_time=payload.lead_time,

            planned_operating_cost=payload.planned_operating_cost,

            actual_operating_cost=payload.actual_operating_cost,

            additional_operating_cost=payload.additional_operating_cost,

            corrective_operation_cost=payload.corrective_operation_cost,

            total_operating_cost=payload.total_operating_cost,

            image=payload.image,

            item_name=payload.item_name,

            stock_uom_id=payload.stock_uom_id,

            description=payload.description,

            has_serial_no=payload.has_serial_no,

            has_batch_no=payload.has_batch_no,

            batch_size=payload.batch_size,

            project=payload.project,

            subcontracting_inward_order=payload.subcontracting_inward_order,

            production_plan_id=payload.production_plan_id,

            mps_id=payload.mps_id,

            material_request_id=payload.material_request_id,

            material_request_item=payload.material_request_item,

            subcontracting_inward_order_item=payload.subcontracting_inward_order_item,

            sales_order_item=payload.sales_order_item,

            production_plan_sub_assembly_item=payload.production_plan_sub_assembly_item,

            production_plan_item=payload.production_plan_item,

            product_bundle_item_id=payload.product_bundle_item_id,

            status=payload.status,

            track_semi_finished_goods=payload.track_semi_finished_goods,

            amended_from_id=payload.amended_from_id,

        )

        self._replace_operations(business_id, row, [x.model_dump() for x in payload.operations])

        self._replace_required_items(business_id, row, [x.model_dump() for x in payload.required_items])

        self._replace_non_stock_items(business_id, row, [x.model_dump() for x in payload.non_stock_items])

        self._replace_secondary_items(business_id, row, [x.model_dump() for x in payload.secondary_items])



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

        payload: WorkOrderUpdate,

    ) -> WorkOrder:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "operations":

                    self._replace_operations(business_id, row, value or [])

                    continue

                if field_name == "required_items":

                    self._replace_required_items(business_id, row, value or [])

                    continue

                if field_name == "non_stock_items":

                    self._replace_non_stock_items(business_id, row, value or [])

                    continue

                if field_name == "secondary_items":

                    self._replace_secondary_items(business_id, row, value or [])

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

    ) -> WorkOrder:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Work Order")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> WorkOrder:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Work Order")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row



    def _replace_operations(

        self, business_id: uuid.UUID, row: WorkOrder, operations: list[dict]

    ) -> None:

        row.operations.clear()

        for idx, entry in enumerate(operations, start=1):

            row.operations.append(

                WorkOrderOperation(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Work Order",

                    parentfield="operations",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_required_items(

        self, business_id: uuid.UUID, row: WorkOrder, required_items: list[dict]

    ) -> None:

        row.required_items.clear()

        for idx, entry in enumerate(required_items, start=1):

            row.required_items.append(

                WorkOrderItem(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Work Order",

                    parentfield="required_items",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_non_stock_items(

        self, business_id: uuid.UUID, row: WorkOrder, non_stock_items: list[dict]

    ) -> None:

        row.non_stock_items.clear()

        for idx, entry in enumerate(non_stock_items, start=1):

            row.non_stock_items.append(

                WorkOrderAdditionalItem(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Work Order",

                    parentfield="non_stock_items",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_secondary_items(

        self, business_id: uuid.UUID, row: WorkOrder, secondary_items: list[dict]

    ) -> None:

        row.secondary_items.clear()

        for idx, entry in enumerate(secondary_items, start=1):

            row.secondary_items.append(

                WorkOrderAdditionalItem(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Work Order",

                    parentfield="secondary_items",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )
