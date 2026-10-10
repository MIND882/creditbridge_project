"""Data access for ClosedDocument. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.closed_document_domain.models.closed_document import ClosedDocument

from app.core.pagination import normalise_paging



__all__ = ["ClosedDocumentRepository"]





class ClosedDocumentRepository:

    model = ClosedDocument





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ClosedDocument]:

        return db.scalar(

            select(ClosedDocument).where(

                ClosedDocument.business_id == business_id, ClosedDocument.id == row_id

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

    ) -> tuple[Sequence[ClosedDocument], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ClosedDocument.business_id == business_id]

        if parent_id is not None:

            conditions.append(ClosedDocument.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(ClosedDocument).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ClosedDocument)

            .where(*conditions)

            .order_by(ClosedDocument.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


