"""Business logic for Workstation Operating Component -- port of

``erpnext/manufacturing/doctype/workstation_operating_component/workstation_operating_component.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.workstation_operating_component_domain.models.workstation_operating_component import WorkstationOperatingComponent

from app.manufacturing.workstation_operating_component_domain.repositories.workstation_operating_component_repository import (

    WorkstationOperatingComponentRepository,

)

from app.manufacturing.workstation_operating_component_domain.schemas.workstation_operating_component import (

    WorkstationOperatingComponentCreate,

    WorkstationOperatingComponentUpdate,

)

from app.manufacturing.workstation_operating_component_account_domain.models.workstation_operating_component_account import WorkstationOperatingComponentAccount

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["WorkstationOperatingComponentService"]





class WorkstationOperatingComponentService:

    def __init__(self, repository: Optional[WorkstationOperatingComponentRepository] = None) -> None:

        self.repository = repository or WorkstationOperatingComponentRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> WorkstationOperatingComponent:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Workstation Operating Component", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: WorkstationOperatingComponent

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> WorkstationOperatingComponent:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[WorkstationOperatingComponent]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[WorkstationOperatingComponent].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    # ``autoname = 'field:component_name'``: the name is the value of

    # that field, derived at create time (Frappe derives it on every save;

    # the creation-time value is what migrated documents carry).



    def create(

        self, db: Session, business_id: uuid.UUID, payload: WorkstationOperatingComponentCreate

    ) -> WorkstationOperatingComponent:

        row = WorkstationOperatingComponent(

            business_id=business_id,

            name=payload.component_name,

            component_name=payload.component_name,

        )

        self._replace_accounts(business_id, row, [x.model_dump() for x in payload.accounts])



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

        payload: WorkstationOperatingComponentUpdate,

    ) -> WorkstationOperatingComponent:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "accounts":

                    self._replace_accounts(business_id, row, value or [])

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



    def _replace_accounts(

        self, business_id: uuid.UUID, row: WorkstationOperatingComponent, accounts: list[dict]

    ) -> None:

        row.accounts.clear()

        for idx, entry in enumerate(accounts, start=1):

            row.accounts.append(

                WorkstationOperatingComponentAccount(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Workstation Operating Component",

                    parentfield="accounts",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )
