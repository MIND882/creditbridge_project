"""

Read-only service for Payment Schedule.



Upstream's controller (``payment_schedule.py``) has no validation of its own --

the rows are computed by the parent invoice's ``set_payment_schedule``. The parent

is not converted, so there is nothing to write through here yet; reads are the

whole surface.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.payment_schedule_domain.models.payment_schedule import PaymentSchedule

from app.accounts.payment_schedule_domain.repositories.payment_schedule_repository import (

    PaymentScheduleRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PaymentScheduleService"]





class PaymentScheduleService:

    def __init__(self, repository: Optional[PaymentScheduleRepository] = None) -> None:

        self.repository = repository or PaymentScheduleRepository()



    def get(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> PaymentSchedule:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Payment Schedule", row_id)

        return row



    def list(self, db: Session, business_id: uuid.UUID, **filters: object) -> ResultPage[PaymentSchedule]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PaymentSchedule].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
