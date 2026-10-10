"""Business logic for Routing -- port of

``erpnext/manufacturing/doctype/routing/routing.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.routing_domain.models.routing import Routing

from app.manufacturing.routing_domain.repositories.routing_repository import (

    RoutingRepository,

)

from app.manufacturing.routing_domain.schemas.routing import (

    RoutingCreate,

    RoutingUpdate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["RoutingService"]





class RoutingService:

    def __init__(self, repository: Optional[RoutingRepository] = None) -> None:

        self.repository = repository or RoutingRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Routing:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Routing", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: Routing

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Routing:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[Routing]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[Routing].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    # ``autoname = 'field:routing_name'``: the name is the value of

    # that field, derived at create time (Frappe derives it on every save;

    # the creation-time value is what migrated documents carry).



    def create(

        self, db: Session, business_id: uuid.UUID, payload: RoutingCreate

    ) -> Routing:

        row = Routing(

            business_id=business_id,

            name=payload.routing_name,

            routing_name=payload.routing_name,

            disabled=payload.disabled,

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

        payload: RoutingUpdate,

    ) -> Routing:

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
