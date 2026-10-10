"""

Data access for Bank Transaction Mapping.



A child table: reads are by parent; writes go through the Bank service so

``idx`` ordering stays consistent.

"""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.bank_transaction_mapping_domain.models.bank_transaction_mapping import BankTransactionMapping

from app.core.pagination import normalise_paging



__all__ = ["BankTransactionMappingRepository"]





class BankTransactionMappingRepository:

    model = BankTransactionMapping



    def get_by_id(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> Optional[BankTransactionMapping]:

        return db.scalar(

            select(BankTransactionMapping).where(

                BankTransactionMapping.business_id == business_id, BankTransactionMapping.id == row_id

            )

        )



    def list_by_parent(

        self, db: Session, business_id: uuid.UUID, parent_id: uuid.UUID

    ) -> list[BankTransactionMapping]:

        return list(

            db.scalars(

                select(BankTransactionMapping)

                .where(

                    BankTransactionMapping.business_id == business_id,

                    BankTransactionMapping.parent_id == parent_id,

                )

                .order_by(BankTransactionMapping.idx.asc())

            )

        )



    def list(

        self, db: Session, business_id: uuid.UUID, *, offset: int = 0, limit: int = 20,

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[BankTransactionMapping], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [BankTransactionMapping.business_id == business_id]

        if parent_id is not None:

            conditions.append(BankTransactionMapping.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(BankTransactionMapping).where(*conditions)) or 0

        )

        rows = db.scalars(

            select(BankTransactionMapping).where(*conditions).order_by(BankTransactionMapping.idx.asc()).offset(offset).limit(limit)

        ).all()

        return rows, total



    def add(self, db: Session, row: BankTransactionMapping) -> BankTransactionMapping:

        db.add(row)

        db.flush()

        return row
