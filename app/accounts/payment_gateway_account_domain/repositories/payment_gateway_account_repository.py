"""Data access for PaymentGatewayAccount. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.payment_gateway_account_domain.models.payment_gateway_account import PaymentGatewayAccount

from app.core.pagination import normalise_paging



__all__ = ["PaymentGatewayAccountRepository"]





class PaymentGatewayAccountRepository:

    model = PaymentGatewayAccount





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PaymentGatewayAccount]:

        return db.scalar(

            select(PaymentGatewayAccount).where(

                PaymentGatewayAccount.business_id == business_id, PaymentGatewayAccount.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[PaymentGatewayAccount]:

        return db.scalar(

            select(PaymentGatewayAccount).where(

                PaymentGatewayAccount.business_id == business_id, PaymentGatewayAccount.name == name

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

    ) -> tuple[Sequence[PaymentGatewayAccount], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PaymentGatewayAccount.business_id == business_id]

        if search:

            conditions.append(PaymentGatewayAccount.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(PaymentGatewayAccount).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PaymentGatewayAccount)

            .where(*conditions)

            .order_by(PaymentGatewayAccount.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: PaymentGatewayAccount) -> PaymentGatewayAccount:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: PaymentGatewayAccount) -> None:

        db.delete(row)

        db.flush()
