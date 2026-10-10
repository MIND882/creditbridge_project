"""

Data access for Accounting Dimension Detail.



A child table: reads are by parent; writes go through the Accounting Dimension service so

``idx`` ordering stays consistent.

"""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.accounting_dimension_detail_domain.models.accounting_dimension_detail import AccountingDimensionDetail

from app.core.pagination import normalise_paging



__all__ = ["AccountingDimensionDetailRepository"]





class AccountingDimensionDetailRepository:

    model = AccountingDimensionDetail



    def get_by_id(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> Optional[AccountingDimensionDetail]:

        return db.scalar(

            select(AccountingDimensionDetail).where(

                AccountingDimensionDetail.business_id == business_id, AccountingDimensionDetail.id == row_id

            )

        )



    def list_by_parent(

        self, db: Session, business_id: uuid.UUID, parent_id: uuid.UUID

    ) -> list[AccountingDimensionDetail]:

        return list(

            db.scalars(

                select(AccountingDimensionDetail)

                .where(

                    AccountingDimensionDetail.business_id == business_id,

                    AccountingDimensionDetail.parent_id == parent_id,

                )

                .order_by(AccountingDimensionDetail.idx.asc())

            )

        )



    def list(

        self, db: Session, business_id: uuid.UUID, *, offset: int = 0, limit: int = 20,

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[AccountingDimensionDetail], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [AccountingDimensionDetail.business_id == business_id]

        if parent_id is not None:

            conditions.append(AccountingDimensionDetail.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(AccountingDimensionDetail).where(*conditions)) or 0

        )

        rows = db.scalars(

            select(AccountingDimensionDetail).where(*conditions).order_by(AccountingDimensionDetail.idx.asc()).offset(offset).limit(limit)

        ).all()

        return rows, total



    def add(self, db: Session, row: AccountingDimensionDetail) -> AccountingDimensionDetail:

        db.add(row)

        db.flush()

        return row
