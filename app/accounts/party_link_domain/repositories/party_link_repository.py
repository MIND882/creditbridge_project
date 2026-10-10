"""Data access for PartyLink. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.party_link_domain.models.party_link import PartyLink

from app.core.pagination import normalise_paging



__all__ = ["PartyLinkRepository"]





class PartyLinkRepository:

    model = PartyLink





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PartyLink]:

        return db.scalar(

            select(PartyLink).where(

                PartyLink.business_id == business_id, PartyLink.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[PartyLink]:

        return db.scalar(

            select(PartyLink).where(

                PartyLink.business_id == business_id, PartyLink.name == name

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

    ) -> tuple[Sequence[PartyLink], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PartyLink.business_id == business_id]

        if search:

            conditions.append(PartyLink.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(PartyLink).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PartyLink)

            .where(*conditions)

            .order_by(PartyLink.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: PartyLink) -> PartyLink:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: PartyLink) -> None:

        db.delete(row)

        db.flush()
