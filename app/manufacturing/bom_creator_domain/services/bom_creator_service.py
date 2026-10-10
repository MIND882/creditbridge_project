"""Business logic for BOM Creator -- port of

``erpnext/manufacturing/doctype/bom_creator/bom_creator.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.bom_creator_domain.models.bom_creator import BomCreator

from app.manufacturing.bom_creator_domain.repositories.bom_creator_repository import (

    BomCreatorRepository,

)

from app.manufacturing.bom_creator_domain.schemas.bom_creator import (

    BomCreatorCreate,

    BomCreatorUpdate,

)

from app.manufacturing.bom_creator_item_domain.models.bom_creator_item import BomCreatorItem

from app.core.errors import NotFoundError

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.pagination import ResultPage



__all__ = ["BomCreatorService"]





class BomCreatorService:

    def __init__(self, repository: Optional[BomCreatorRepository] = None) -> None:

        self.repository = repository or BomCreatorRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> BomCreator:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("BOM Creator", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: BomCreator

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> BomCreator:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[BomCreator]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[BomCreator].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``prompt``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(BomCreator).where(

                    BomCreator.business_id == business_id

                )

            )

            or 0

        )

        return f"prompt{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: BomCreatorCreate

    ) -> BomCreator:

        row = BomCreator(

            business_id=business_id,

            name=self.next_name(db, business_id),

            item_code_id=payload.item_code_id,

            is_phantom=payload.is_phantom,

            item_name=payload.item_name,

            item_group_id=payload.item_group_id,

            qty=payload.qty,

            project=payload.project,

            uom_id=payload.uom_id,

            routing_id=payload.routing_id,

            rm_cost_as_per=payload.rm_cost_as_per,

            set_rate_based_on_warehouse=payload.set_rate_based_on_warehouse,

            buying_price_list_id=payload.buying_price_list_id,

            price_list_currency=payload.price_list_currency,

            plc_conversion_rate=payload.plc_conversion_rate,

            currency=payload.currency,

            conversion_rate=payload.conversion_rate,

            default_warehouse_id=payload.default_warehouse_id,

            company=payload.company,

            raw_material_cost=payload.raw_material_cost,

            remarks=payload.remarks,

            status=payload.status,

            error_log=payload.error_log,

            amended_from_id=payload.amended_from_id,

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

        payload: BomCreatorUpdate,

    ) -> BomCreator:

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

    ) -> BomCreator:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "BOM Creator")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> BomCreator:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "BOM Creator")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row



    def _replace_items(

        self, business_id: uuid.UUID, row: BomCreator, items: list[dict]

    ) -> None:

        row.items.clear()

        for idx, entry in enumerate(items, start=1):

            row.items.append(

                BomCreatorItem(

                    business_id=business_id,

                    idx=idx,

                    parenttype="BOM Creator",

                    parentfield="items",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )
