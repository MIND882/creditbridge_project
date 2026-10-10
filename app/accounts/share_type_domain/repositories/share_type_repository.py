"""Data access for ShareType. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.share_type_domain.models.share_type import ShareType

from app.core.pagination import normalise_paging



__all__ = ["ShareTypeRepository"]





class ShareTypeRepository:

    model = ShareType



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ShareType]:

        return db.scalar(

            select(ShareType).where(

                ShareType.business_id == business_id, ShareType.id == row_id

            )

        )



    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ShareType]:

        return db.scalar(

            select(ShareType).where(

                ShareType.business_id == business_id, ShareType.name == name

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

    ) -> tuple[Sequence[ShareType], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ShareType.business_id == business_id]

        if search:

            conditions.append(ShareType.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(ShareType).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ShareType)

            .where(*conditions)

            .order_by(ShareType.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



    def add(self, db: Session, row: ShareType) -> ShareType:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: ShareType) -> None:

        db.delete(row)

        db.flush()
