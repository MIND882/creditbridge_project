"""Data access for Payment Term. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.payment_term_domain.models.payment_term import PaymentTerm

from app.core.pagination import normalise_paging



__all__ = ["PaymentTermRepository"]





class PaymentTermRepository:

    model = PaymentTerm



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, term_id: uuid.UUID

    ) -> Optional[PaymentTerm]:

        return db.scalar(

            select(PaymentTerm).where(

                PaymentTerm.business_id == business_id, PaymentTerm.id == term_id

            )

        )



    def get_by_name(self, db: Session, business_id: uuid.UUID, name: str) -> Optional[PaymentTerm]:

        return db.scalar(

            select(PaymentTerm).where(

                PaymentTerm.business_id == business_id, PaymentTerm.name == name

            )

        )



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        search: Optional[str] = None,

    ) -> tuple[Sequence[PaymentTerm], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PaymentTerm.business_id == business_id]

        if search:

            like = f"%{search.strip()}%"

            conditions.append(

                PaymentTerm.name.ilike(like) | PaymentTerm.payment_term_name.ilike(like)

            )



        total = int(

            db.scalar(select(func.count()).select_from(PaymentTerm).where(*conditions)) or 0

        )

        rows = db.scalars(

            select(PaymentTerm)

            .where(*conditions)

            .order_by(PaymentTerm.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



    def add(self, db: Session, row: PaymentTerm) -> PaymentTerm:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: PaymentTerm) -> None:

        db.delete(row)

        db.flush()
