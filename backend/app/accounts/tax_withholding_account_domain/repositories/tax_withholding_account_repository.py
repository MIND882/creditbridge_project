"""Data access for TaxWithholdingAccount. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.tax_withholding_account_domain.models.tax_withholding_account import TaxWithholdingAccount

from app.core.pagination import normalise_paging



__all__ = ["TaxWithholdingAccountRepository"]





class TaxWithholdingAccountRepository:

    model = TaxWithholdingAccount



    def get_by_id(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> Optional[TaxWithholdingAccount]:

        return db.scalar(

            select(TaxWithholdingAccount).where(

                TaxWithholdingAccount.business_id == business_id, TaxWithholdingAccount.id == row_id

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

    ) -> tuple[Sequence[TaxWithholdingAccount], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [TaxWithholdingAccount.business_id == business_id]

        if parent_id is not None:

            conditions.append(TaxWithholdingAccount.parent_id == parent_id)

        total = int(

            db.scalar(select(func.count()).select_from(TaxWithholdingAccount).where(*conditions)) or 0

        )

        rows = db.scalars(

            select(TaxWithholdingAccount)

            .where(*conditions)

            .order_by(TaxWithholdingAccount.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
