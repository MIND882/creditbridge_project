"""Data access for SmsCenter. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.selling.sms_center_domain.models.sms_center import SmsCenter

from app.core.pagination import normalise_paging



__all__ = ["SmsCenterRepository"]





class SmsCenterRepository:

    model = SmsCenter





    def get_for_business(

        self, db: Session, business_id: uuid.UUID

    ) -> Optional[SmsCenter]:

        return db.scalar(

            select(SmsCenter).where(

                SmsCenter.business_id == business_id

            )

        )



    def add(self, db: Session, row: SmsCenter) -> SmsCenter:

        db.add(row)

        db.flush()

        return row
