"""Business logic for BOM -- port of

``erpnext/manufacturing/doctype/bom/bom.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.bom_domain.models.bom import Bom

from app.manufacturing.bom_domain.repositories.bom_repository import (

    BomRepository,

)

from app.manufacturing.bom_domain.schemas.bom import (

    BomCreate,

    BomUpdate,

)

from app.manufacturing.bom_operation_domain.models.bom_operation import BomOperation

from app.manufacturing.bom_item_domain.models.bom_item import BomItem

from app.manufacturing.bom_secondary_item_domain.models.bom_secondary_item import BomSecondaryItem

from app.manufacturing.bom_explosion_item_domain.models.bom_explosion_item import BomExplosionItem

from app.manufacturing.bom_website_item_domain.models.bom_website_item import BomWebsiteItem

from app.manufacturing.bom_website_operation_domain.models.bom_website_operation import BomWebsiteOperation

from app.core.errors import NotFoundError

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.pagination import ResultPage



__all__ = ["BomService"]





class BomService:

    def __init__(self, repository: Optional[BomRepository] = None) -> None:

        self.repository = repository or BomRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Bom:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("BOM", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: Bom

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Bom:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[Bom]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[Bom].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(Bom).where(

                    Bom.business_id == business_id

                )

            )

            or 0

        )

        return f"BOM-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: BomCreate

    ) -> Bom:

        row = Bom(

            business_id=business_id,

            name=self.next_name(db, business_id),

            company=payload.company,

            item_id=payload.item_id,

            quantity=payload.quantity,

            uom_id=payload.uom_id,

            cost_allocation_per=payload.cost_allocation_per,

            cost_allocation=payload.cost_allocation,

            process_loss_percentage=payload.process_loss_percentage,

            process_loss_qty=payload.process_loss_qty,

            with_operations=payload.with_operations,

            track_semi_finished_goods=payload.track_semi_finished_goods,

            transfer_material_against=payload.transfer_material_against,

            routing_id=payload.routing_id,

            fg_based_operating_cost=payload.fg_based_operating_cost,

            operating_cost_per_bom_quantity=payload.operating_cost_per_bom_quantity,

            is_active=payload.is_active,

            is_default=payload.is_default,

            set_rate_of_sub_assembly_item_based_on_bom=payload.set_rate_of_sub_assembly_item_based_on_bom,

            is_phantom_bom=payload.is_phantom_bom,

            allow_alternative_item=payload.allow_alternative_item,

            inspection_required=payload.inspection_required,

            quality_inspection_template_id=payload.quality_inspection_template_id,

            default_source_warehouse_id=payload.default_source_warehouse_id,

            default_target_warehouse_id=payload.default_target_warehouse_id,

            backflush_based_on=payload.backflush_based_on,

            operating_cost=payload.operating_cost,

            raw_material_cost=payload.raw_material_cost,

            secondary_items_cost=payload.secondary_items_cost,

            base_operating_cost=payload.base_operating_cost,

            base_raw_material_cost=payload.base_raw_material_cost,

            base_secondary_items_cost=payload.base_secondary_items_cost,

            total_cost=payload.total_cost,

            base_total_cost=payload.base_total_cost,

            rm_cost_as_per=payload.rm_cost_as_per,

            buying_price_list_id=payload.buying_price_list_id,

            price_list_currency=payload.price_list_currency,

            plc_conversion_rate=payload.plc_conversion_rate,

            currency=payload.currency,

            conversion_rate=payload.conversion_rate,

            item_name=payload.item_name,

            image=payload.image,

            description=payload.description,

            has_variants=payload.has_variants,

            project=payload.project,

            show_in_website=payload.show_in_website,

            route=payload.route,

            website_image=payload.website_image,

            thumbnail=payload.thumbnail,

            show_items=payload.show_items,

            show_operations=payload.show_operations,

            web_long_description=payload.web_long_description,

            bom_creator_id=payload.bom_creator_id,

            bom_creator_item=payload.bom_creator_item,

            amended_from_id=payload.amended_from_id,

        )

        self._replace_operations(business_id, row, [x.model_dump() for x in payload.operations])

        self._replace_items(business_id, row, [x.model_dump() for x in payload.items])

        self._replace_secondary_items(business_id, row, [x.model_dump() for x in payload.secondary_items])

        self._replace_exploded_items(business_id, row, [x.model_dump() for x in payload.exploded_items])

        self._replace_website_items(business_id, row, [x.model_dump() for x in payload.website_items])

        self._replace_website_operations(business_id, row, [x.model_dump() for x in payload.website_operations])



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

        payload: BomUpdate,

    ) -> Bom:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "operations":

                    self._replace_operations(business_id, row, value or [])

                    continue

                if field_name == "items":

                    self._replace_items(business_id, row, value or [])

                    continue

                if field_name == "secondary_items":

                    self._replace_secondary_items(business_id, row, value or [])

                    continue

                if field_name == "exploded_items":

                    self._replace_exploded_items(business_id, row, value or [])

                    continue

                if field_name == "website_items":

                    self._replace_website_items(business_id, row, value or [])

                    continue

                if field_name == "website_operations":

                    self._replace_website_operations(business_id, row, value or [])

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

    ) -> Bom:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "BOM")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Bom:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "BOM")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row



    def _replace_operations(

        self, business_id: uuid.UUID, row: Bom, operations: list[dict]

    ) -> None:

        row.operations.clear()

        for idx, entry in enumerate(operations, start=1):

            row.operations.append(

                BomOperation(

                    business_id=business_id,

                    idx=idx,

                    parenttype="BOM",

                    parentfield="operations",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_items(

        self, business_id: uuid.UUID, row: Bom, items: list[dict]

    ) -> None:

        row.items.clear()

        for idx, entry in enumerate(items, start=1):

            row.items.append(

                BomItem(

                    business_id=business_id,

                    idx=idx,

                    parenttype="BOM",

                    parentfield="items",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_secondary_items(

        self, business_id: uuid.UUID, row: Bom, secondary_items: list[dict]

    ) -> None:

        row.secondary_items.clear()

        for idx, entry in enumerate(secondary_items, start=1):

            row.secondary_items.append(

                BomSecondaryItem(

                    business_id=business_id,

                    idx=idx,

                    parenttype="BOM",

                    parentfield="secondary_items",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_exploded_items(

        self, business_id: uuid.UUID, row: Bom, exploded_items: list[dict]

    ) -> None:

        row.exploded_items.clear()

        for idx, entry in enumerate(exploded_items, start=1):

            row.exploded_items.append(

                BomExplosionItem(

                    business_id=business_id,

                    idx=idx,

                    parenttype="BOM",

                    parentfield="exploded_items",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_website_items(

        self, business_id: uuid.UUID, row: Bom, website_items: list[dict]

    ) -> None:

        row.website_items.clear()

        for idx, entry in enumerate(website_items, start=1):

            row.website_items.append(

                BomWebsiteItem(

                    business_id=business_id,

                    idx=idx,

                    parenttype="BOM",

                    parentfield="website_items",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_website_operations(

        self, business_id: uuid.UUID, row: Bom, website_operations: list[dict]

    ) -> None:

        row.website_operations.clear()

        for idx, entry in enumerate(website_operations, start=1):

            row.website_operations.append(

                BomWebsiteOperation(

                    business_id=business_id,

                    idx=idx,

                    parenttype="BOM",

                    parentfield="website_operations",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )
