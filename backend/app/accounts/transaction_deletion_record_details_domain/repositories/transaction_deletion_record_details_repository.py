"""Data access for TransactionDeletionRecordDetails. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.transaction_deletion_record_details_domain.models.transaction_deletion_record_details import TransactionDeletionRecordDetails

from app.core.pagination import normalise_paging



__all__ = ["TransactionDeletionRecordDetailsRepository"]





class TransactionDeletionRecordDetailsRepository:

    model = TransactionDeletionRecordDetails





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[TransactionDeletionRecordDetails]:

        return db.scalar(

            select(TransactionDeletionRecordDetails).where(

                TransactionDeletionRecordDetails.business_id == business_id, TransactionDeletionRecordDetails.id == row_id

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

    ) -> tuple[Sequence[TransactionDeletionRecordDetails], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [TransactionDeletionRecordDetails.business_id == business_id]

        if parent_id is not None:

            conditions.append(TransactionDeletionRecordDetails.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(TransactionDeletionRecordDetails).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(TransactionDeletionRecordDetails)

            .where(*conditions)

            .order_by(TransactionDeletionRecordDetails.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


