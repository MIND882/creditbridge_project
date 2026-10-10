"""Business logic for Item Lead Time -- port of

``erpnext/stock/doctype/item_lead_time/item_lead_time.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.item_lead_time_domain.models.item_lead_time import ItemLeadTime

from app.stock.item_lead_time_domain.repositories.item_lead_time_repository import (

    ItemLeadTimeRepository,

)

from app.stock.item_lead_time_domain.schemas.item_lead_time import (

    ItemLeadTimeCreate,

    ItemLeadTimeUpdate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ItemLeadTimeService"]





class ItemLeadTimeService:

    def __init__(self, repository: Optional[ItemLeadTimeRepository] = None) -> None:

        self.repository = repository or ItemLeadTimeRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ItemLeadTime:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Item Lead Time", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: ItemLeadTime

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ItemLeadTime:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ItemLeadTime]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ItemLeadTime].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    # ``autoname = 'field:item_code'``: the name is the value of

    # that field, derived at create time (Frappe derives it on every save;

    # the creation-time value is what migrated documents carry).



    def create(

        self, db: Session, business_id: uuid.UUID, payload: ItemLeadTimeCreate

    ) -> ItemLeadTime:

        row = ItemLeadTime(

            business_id=business_id,

            name=str(payload.item_code_id),

            item_code_id=payload.item_code_id,

            item_name=payload.item_name,

            buffer_time=payload.buffer_time,

            no_of_shift=payload.no_of_shift,

            manufacturing_time_in_mins=payload.manufacturing_time_in_mins,

            total_workstation_time=payload.total_workstation_time,

            daily_yield=payload.daily_yield,

            capacity_per_day=payload.capacity_per_day,

            no_of_units_produced=payload.no_of_units_produced,

            purchase_time=payload.purchase_time,

            shift_time_in_hours=payload.shift_time_in_hours,

            no_of_workstations=payload.no_of_workstations,

            stock_uom_id=payload.stock_uom_id,

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

        payload: ItemLeadTimeUpdate,

    ) -> ItemLeadTime:

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
