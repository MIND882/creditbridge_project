"""Business logic for Shipment Parcel Template -- port of

``erpnext/stock/doctype/shipment_parcel_template/shipment_parcel_template.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.shipment_parcel_template_domain.models.shipment_parcel_template import ShipmentParcelTemplate

from app.stock.shipment_parcel_template_domain.repositories.shipment_parcel_template_repository import (

    ShipmentParcelTemplateRepository,

)

from app.stock.shipment_parcel_template_domain.schemas.shipment_parcel_template import (

    ShipmentParcelTemplateCreate,

    ShipmentParcelTemplateUpdate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ShipmentParcelTemplateService"]





class ShipmentParcelTemplateService:

    def __init__(self, repository: Optional[ShipmentParcelTemplateRepository] = None) -> None:

        self.repository = repository or ShipmentParcelTemplateRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ShipmentParcelTemplate:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Shipment Parcel Template", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: ShipmentParcelTemplate

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ShipmentParcelTemplate:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ShipmentParcelTemplate]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ShipmentParcelTemplate].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    # ``autoname = 'field:parcel_template_name'``: the name is the value of

    # that field, derived at create time (Frappe derives it on every save;

    # the creation-time value is what migrated documents carry).



    def create(

        self, db: Session, business_id: uuid.UUID, payload: ShipmentParcelTemplateCreate

    ) -> ShipmentParcelTemplate:

        row = ShipmentParcelTemplate(

            business_id=business_id,

            name=payload.parcel_template_name,

            length=payload.length,

            width=payload.width,

            height=payload.height,

            weight=payload.weight,

            parcel_template_name=payload.parcel_template_name,

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

        payload: ShipmentParcelTemplateUpdate,

    ) -> ShipmentParcelTemplate:

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
