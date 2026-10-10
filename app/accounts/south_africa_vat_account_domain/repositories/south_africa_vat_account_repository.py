"""Data access for SouthAfricaVatAccount. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.south_africa_vat_account_domain.models.south_africa_vat_account import SouthAfricaVatAccount

from app.core.pagination import normalise_paging



__all__ = ["SouthAfricaVatAccountRepository"]





class SouthAfricaVatAccountRepository:

    model = SouthAfricaVatAccount





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SouthAfricaVatAccount]:

        return db.scalar(

            select(SouthAfricaVatAccount).where(

                SouthAfricaVatAccount.business_id == business_id, SouthAfricaVatAccount.id == row_id

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

    ) -> tuple[Sequence[SouthAfricaVatAccount], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SouthAfricaVatAccount.business_id == business_id]

        if parent_id is not None:

            conditions.append(SouthAfricaVatAccount.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(SouthAfricaVatAccount).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SouthAfricaVatAccount)

            .where(*conditions)

            .order_by(SouthAfricaVatAccount.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


