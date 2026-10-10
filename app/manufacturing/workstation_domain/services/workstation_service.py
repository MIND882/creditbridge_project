"""Business logic for Workstation -- port of

``erpnext/manufacturing/doctype/workstation/workstation.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.workstation_domain.models.workstation import Workstation

from app.manufacturing.workstation_domain.repositories.workstation_repository import (

    WorkstationRepository,

)

from app.manufacturing.workstation_domain.schemas.workstation import (

    WorkstationCreate,

    WorkstationUpdate,

)

from app.manufacturing.workstation_cost_domain.models.workstation_cost import WorkstationCost

from app.manufacturing.workstation_working_hour_domain.models.workstation_working_hour import WorkstationWorkingHour

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["WorkstationService"]





class WorkstationService:

    def __init__(self, repository: Optional[WorkstationRepository] = None) -> None:

        self.repository = repository or WorkstationRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Workstation:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Workstation", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: Workstation

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Workstation:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[Workstation]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[Workstation].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    # ``autoname = 'field:workstation_name'``: the name is the value of

    # that field, derived at create time (Frappe derives it on every save;

    # the creation-time value is what migrated documents carry).



    def create(

        self, db: Session, business_id: uuid.UUID, payload: WorkstationCreate

    ) -> Workstation:

        row = Workstation(

            business_id=business_id,

            name=payload.workstation_name,

            workstation_name=payload.workstation_name,

            workstation_type_id=payload.workstation_type_id,

            plant_floor_id=payload.plant_floor_id,

            disabled=payload.disabled,

            production_capacity=payload.production_capacity,

            warehouse_id=payload.warehouse_id,

            status=payload.status,

            on_status_image=payload.on_status_image,

            off_status_image=payload.off_status_image,

            hour_rate=payload.hour_rate,

            description=payload.description,

            holiday_list=payload.holiday_list,

            total_working_hours=payload.total_working_hours,

        )

        self._replace_workstation_costs(business_id, row, [x.model_dump() for x in payload.workstation_costs])

        self._replace_working_hours(business_id, row, [x.model_dump() for x in payload.working_hours])



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

        payload: WorkstationUpdate,

    ) -> Workstation:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "workstation_costs":

                    self._replace_workstation_costs(business_id, row, value or [])

                    continue

                if field_name == "working_hours":

                    self._replace_working_hours(business_id, row, value or [])

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



    def _replace_workstation_costs(

        self, business_id: uuid.UUID, row: Workstation, workstation_costs: list[dict]

    ) -> None:

        row.workstation_costs.clear()

        for idx, entry in enumerate(workstation_costs, start=1):

            row.workstation_costs.append(

                WorkstationCost(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Workstation",

                    parentfield="workstation_costs",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_working_hours(

        self, business_id: uuid.UUID, row: Workstation, working_hours: list[dict]

    ) -> None:

        row.working_hours.clear()

        for idx, entry in enumerate(working_hours, start=1):

            row.working_hours.append(

                WorkstationWorkingHour(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Workstation",

                    parentfield="working_hours",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )
