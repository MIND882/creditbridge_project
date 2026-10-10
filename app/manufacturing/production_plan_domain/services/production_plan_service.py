"""Business logic for Production Plan -- port of

``erpnext/manufacturing/doctype/production_plan/production_plan.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.production_plan_domain.models.production_plan import ProductionPlan

from app.manufacturing.production_plan_domain.repositories.production_plan_repository import (

    ProductionPlanRepository,

)

from app.manufacturing.production_plan_domain.schemas.production_plan import (

    ProductionPlanCreate,

    ProductionPlanUpdate,

)

from app.manufacturing.production_plan_item_domain.models.production_plan_item import ProductionPlanItem

from app.manufacturing.production_plan_item_reference_domain.models.production_plan_item_reference import ProductionPlanItemReference

from app.manufacturing.production_plan_sub_assembly_item_domain.models.production_plan_sub_assembly_item import ProductionPlanSubAssemblyItem

from app.manufacturing.material_request_plan_item_domain.models.material_request_plan_item import MaterialRequestPlanItem

from app.manufacturing.production_plan_material_request_warehouse_domain.models.production_plan_material_request_warehouse import ProductionPlanMaterialRequestWarehouse

from app.core.errors import NotFoundError

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.pagination import ResultPage



__all__ = ["ProductionPlanService"]





class ProductionPlanService:

    def __init__(self, repository: Optional[ProductionPlanRepository] = None) -> None:

        self.repository = repository or ProductionPlanRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProductionPlan:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Production Plan", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: ProductionPlan

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProductionPlan:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ProductionPlan]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ProductionPlan].build(

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

                select(func.count()).select_from(ProductionPlan).where(

                    ProductionPlan.business_id == business_id

                )

            )

            or 0

        )

        return f"{prefix}{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: ProductionPlanCreate

    ) -> ProductionPlan:

        row = ProductionPlan(

            business_id=business_id,

            name=self.next_name(db, business_id, payload.naming_series),

            naming_series=payload.naming_series,

            company=payload.company,

            get_items_from=payload.get_items_from,

            posting_date=payload.posting_date,

            reserve_stock=payload.reserve_stock,

            item_code_id=payload.item_code_id,

            customer_id=payload.customer_id,

            warehouse_id=payload.warehouse_id,

            project=payload.project,

            sales_order_status=payload.sales_order_status,

            from_date=payload.from_date,

            to_date=payload.to_date,

            from_delivery_date=payload.from_delivery_date,

            to_delivery_date=payload.to_delivery_date,

            combine_items=payload.combine_items,

            sub_assembly_warehouse_id=payload.sub_assembly_warehouse_id,

            skip_available_sub_assembly_item=payload.skip_available_sub_assembly_item,

            combine_sub_items=payload.combine_sub_items,

            include_non_stock_items=payload.include_non_stock_items,

            include_subcontracted_items=payload.include_subcontracted_items,

            consider_minimum_order_qty=payload.consider_minimum_order_qty,

            include_safety_stock=payload.include_safety_stock,

            ignore_existing_ordered_qty=payload.ignore_existing_ordered_qty,

            raw_material_group_warehouse_id=payload.raw_material_group_warehouse_id,

            for_warehouse_id=payload.for_warehouse_id,

            total_planned_qty=payload.total_planned_qty,

            total_produced_qty=payload.total_produced_qty,

            status=payload.status,

            amended_from_id=payload.amended_from_id,

        )

        self._replace_po_items(business_id, row, [x.model_dump() for x in payload.po_items])

        self._replace_prod_plan_references(business_id, row, [x.model_dump() for x in payload.prod_plan_references])

        self._replace_sub_assembly_items(business_id, row, [x.model_dump() for x in payload.sub_assembly_items])

        self._replace_mr_items(business_id, row, [x.model_dump() for x in payload.mr_items])

        self._replace_warehouses(business_id, row, [x.model_dump() for x in payload.warehouses])



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

        payload: ProductionPlanUpdate,

    ) -> ProductionPlan:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "po_items":

                    self._replace_po_items(business_id, row, value or [])

                    continue

                if field_name == "prod_plan_references":

                    self._replace_prod_plan_references(business_id, row, value or [])

                    continue

                if field_name == "sub_assembly_items":

                    self._replace_sub_assembly_items(business_id, row, value or [])

                    continue

                if field_name == "mr_items":

                    self._replace_mr_items(business_id, row, value or [])

                    continue

                if field_name == "warehouses":

                    self._replace_warehouses(business_id, row, value or [])

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

    ) -> ProductionPlan:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Production Plan")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProductionPlan:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Production Plan")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row



    def _replace_po_items(

        self, business_id: uuid.UUID, row: ProductionPlan, po_items: list[dict]

    ) -> None:

        row.po_items.clear()

        for idx, entry in enumerate(po_items, start=1):

            row.po_items.append(

                ProductionPlanItem(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Production Plan",

                    parentfield="po_items",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_prod_plan_references(

        self, business_id: uuid.UUID, row: ProductionPlan, prod_plan_references: list[dict]

    ) -> None:

        row.prod_plan_references.clear()

        for idx, entry in enumerate(prod_plan_references, start=1):

            row.prod_plan_references.append(

                ProductionPlanItemReference(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Production Plan",

                    parentfield="prod_plan_references",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_sub_assembly_items(

        self, business_id: uuid.UUID, row: ProductionPlan, sub_assembly_items: list[dict]

    ) -> None:

        row.sub_assembly_items.clear()

        for idx, entry in enumerate(sub_assembly_items, start=1):

            row.sub_assembly_items.append(

                ProductionPlanSubAssemblyItem(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Production Plan",

                    parentfield="sub_assembly_items",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_mr_items(

        self, business_id: uuid.UUID, row: ProductionPlan, mr_items: list[dict]

    ) -> None:

        row.mr_items.clear()

        for idx, entry in enumerate(mr_items, start=1):

            row.mr_items.append(

                MaterialRequestPlanItem(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Production Plan",

                    parentfield="mr_items",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_warehouses(

        self, business_id: uuid.UUID, row: ProductionPlan, warehouses: list[dict]

    ) -> None:

        row.warehouses.clear()

        for idx, entry in enumerate(warehouses, start=1):

            row.warehouses.append(

                ProductionPlanMaterialRequestWarehouse(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Production Plan",

                    parentfield="warehouses",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )
