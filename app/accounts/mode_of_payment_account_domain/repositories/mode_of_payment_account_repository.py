"""Data access for ModeOfPaymentAccount. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.mode_of_payment_account_domain.models.mode_of_payment_account import ModeOfPaymentAccount

from app.core.pagination import normalise_paging



__all__ = ["ModeOfPaymentAccountRepository"]





class ModeOfPaymentAccountRepository:

    model = ModeOfPaymentAccount



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ModeOfPaymentAccount]:

        return db.scalar(

            select(ModeOfPaymentAccount).where(

                ModeOfPaymentAccount.business_id == business_id,

                ModeOfPaymentAccount.id == row_id,

            )

        )



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[ModeOfPaymentAccount], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ModeOfPaymentAccount.business_id == business_id]

        if parent_id is not None:

            conditions.append(ModeOfPaymentAccount.parent_id == parent_id)

        total = int(

            db.scalar(

                select(func.count()).select_from(ModeOfPaymentAccount).where(*conditions)

            )

            or 0

        )

        rows = db.scalars(

            select(ModeOfPaymentAccount)

            .where(*conditions)

            .order_by(ModeOfPaymentAccount.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
