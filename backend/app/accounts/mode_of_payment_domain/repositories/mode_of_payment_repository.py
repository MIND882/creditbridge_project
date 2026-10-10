"""Data access for ModeOfPayment. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.mode_of_payment_domain.models.mode_of_payment import (

    ModeOfPayment,

    ModeOfPaymentType,

)

from app.core.pagination import normalise_paging



__all__ = ["ModeOfPaymentRepository"]





class ModeOfPaymentRepository:

    model = ModeOfPayment



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks conftest

        # collection with "failed to locate a name".

        return [selectinload(ModeOfPayment.accounts)]



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ModeOfPayment]:

        return db.scalar(

            select(ModeOfPayment)

            .where(

                ModeOfPayment.business_id == business_id,

                ModeOfPayment.id == row_id,

            )

            .options(*self._options())

        )



    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ModeOfPayment]:

        return db.scalar(

            select(ModeOfPayment)

            .where(

                ModeOfPayment.business_id == business_id,

                ModeOfPayment.name == name,

            )

            .options(*self._options())

        )



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        include_disabled: bool = True,

        type: Optional[ModeOfPaymentType] = None,

        search: Optional[str] = None,

    ) -> tuple[Sequence[ModeOfPayment], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ModeOfPayment.business_id == business_id]

        if not include_disabled:

            conditions.append(ModeOfPayment.enabled.is_(True))

        if type is not None:

            conditions.append(ModeOfPayment.type == type)

        if search:

            conditions.append(ModeOfPayment.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(

                select(func.count()).select_from(ModeOfPayment).where(*conditions)

            )

            or 0

        )

        rows = db.scalars(

            select(ModeOfPayment)

            .where(*conditions)

            .order_by(ModeOfPayment.name.asc())

            .offset(offset)

            .limit(limit)

            .options(*self._options())

        ).all()

        return rows, total



    def add(self, db: Session, row: ModeOfPayment) -> ModeOfPayment:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: ModeOfPayment) -> None:

        db.delete(row)

        db.flush()
