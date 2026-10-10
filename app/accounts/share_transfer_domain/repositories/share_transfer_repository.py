"""Data access for ShareTransfer. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.share_transfer_domain.models.share_transfer import ShareTransfer

from app.core.pagination import normalise_paging



__all__ = ["ShareTransferRepository"]





class ShareTransferRepository:

    model = ShareTransfer





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ShareTransfer]:

        return db.scalar(

            select(ShareTransfer).where(

                ShareTransfer.business_id == business_id, ShareTransfer.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ShareTransfer]:

        return db.scalar(

            select(ShareTransfer).where(

                ShareTransfer.business_id == business_id, ShareTransfer.name == name

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

        include_cancelled: bool = False,

    ) -> tuple[Sequence[ShareTransfer], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ShareTransfer.business_id == business_id]

        if not include_cancelled:

            conditions.append(ShareTransfer.docstatus != 2)

        if search:

            conditions.append(ShareTransfer.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(ShareTransfer).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ShareTransfer)

            .where(*conditions)

            .order_by(ShareTransfer.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: ShareTransfer) -> ShareTransfer:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: ShareTransfer) -> None:

        db.delete(row)

        db.flush()
