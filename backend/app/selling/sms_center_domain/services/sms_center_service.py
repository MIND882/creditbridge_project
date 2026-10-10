"""Business logic for SMS Center -- port of

``erpnext/selling/doctype/sms_center/sms_center.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.selling.sms_center_domain.models.sms_center import SmsCenter

from app.selling.sms_center_domain.repositories.sms_center_repository import (

    SmsCenterRepository,

)

from app.selling.sms_center_domain.schemas.sms_center import (

    SmsCenterUpdate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SmsCenterService"]





class SmsCenterService:

    def __init__(self, repository: Optional[SmsCenterRepository] = None) -> None:

        self.repository = repository or SmsCenterRepository()





    def get_or_create(

        self, db: Session, business_id: uuid.UUID

    ) -> SmsCenter:

        """The tenant's settings row, created with upstream defaults on first read."""

        row = self.repository.get_for_business(db, business_id)

        if row is None:

            row = SmsCenter(business_id=business_id)

            try:

                self.repository.add(db, row)

                db.commit()

            except Exception:

                db.rollback()

                raise

            db.refresh(row)

        return row



    def update(

        self, db: Session, business_id: uuid.UUID, payload: SmsCenterUpdate

    ) -> SmsCenter:

        row = self.get_or_create(db, business_id)

        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row

        try:

            for field_name, value in changes.items():

                setattr(row, field_name, value)

            db.flush()

        except Exception:

            db.rollback()

            raise

        db.commit()

        db.refresh(row)

        return row
