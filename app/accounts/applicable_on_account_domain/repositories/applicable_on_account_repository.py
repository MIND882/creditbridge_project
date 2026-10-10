"""

Data access for Applicable On Account.



A child table: reads are by parent; writes go through the Accounting Dimension Filter service so

``idx`` ordering stays consistent.

"""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.applicable_on_account_domain.models.applicable_on_account import ApplicableOnAccount

from app.core.pagination import normalise_paging



__all__ = ["ApplicableOnAccountRepository"]





class ApplicableOnAccountRepository:

    model = ApplicableOnAccount



    def get_by_id(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> Optional[ApplicableOnAccount]:

        return db.scalar(

            select(ApplicableOnAccount).where(

                ApplicableOnAccount.business_id == business_id, ApplicableOnAccount.id == row_id

            )

        )



    def list_by_parent(

        self, db: Session, business_id: uuid.UUID, parent_id: uuid.UUID

    ) -> list[ApplicableOnAccount]:

        return list(

            db.scalars(

                select(ApplicableOnAccount)

                .where(

                    ApplicableOnAccount.business_id == business_id,

                    ApplicableOnAccount.parent_id == parent_id,

                )

                .order_by(ApplicableOnAccount.idx.asc())

            )

        )



    def list(

        self, db: Session, business_id: uuid.UUID, *, offset: int = 0, limit: int = 20,

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[ApplicableOnAccount], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ApplicableOnAccount.business_id == business_id]

        if parent_id is not None:

            conditions.append(ApplicableOnAccount.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(ApplicableOnAccount).where(*conditions)) or 0

        )

        rows = db.scalars(

            select(ApplicableOnAccount).where(*conditions).order_by(ApplicableOnAccount.idx.asc()).offset(offset).limit(limit)

        ).all()

        return rows, total



    def add(self, db: Session, row: ApplicableOnAccount) -> ApplicableOnAccount:

        db.add(row)

        db.flush()

        return row
