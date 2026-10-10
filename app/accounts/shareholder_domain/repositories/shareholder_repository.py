"""Data access for Shareholder. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import datetime as dt

import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.shareholder_domain.models.shareholder import Shareholder

from app.core.pagination import normalise_paging



__all__ = ["ShareholderRepository"]





class ShareholderRepository:

    model = Shareholder



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks conftest

        # collection with "failed to locate a name".

        return [selectinload(Shareholder.share_balance)]



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[Shareholder]:

        return db.scalar(

            select(Shareholder)

            .where(

                Shareholder.business_id == business_id,

                Shareholder.id == row_id,

            )

            .options(*self._options())

        )



    def next_name(self, db: Session, business_id: uuid.UUID, on: dt.date) -> str:

        """``ACC-SH-<year>-<#####>``, counted per tenant per year."""

        count = int(

            db.scalar(

                select(func.count())

                .select_from(Shareholder)

                .where(Shareholder.business_id == business_id)

                .where(Shareholder.name.like(f"ACC-SH-{on.year}-%"))

            )

            or 0

        )

        return f"ACC-SH-{on.year}-{count + 1:05d}"



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        search: Optional[str] = None,

    ) -> tuple[Sequence[Shareholder], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [Shareholder.business_id == business_id]

        if search:

            like = f"%{search.strip()}%"

            conditions.append(

                Shareholder.title.ilike(like) | Shareholder.name.ilike(like)

            )



        total = int(

            db.scalar(select(func.count()).select_from(Shareholder).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(Shareholder)

            .where(*conditions)

            .order_by(Shareholder.name.asc())

            .offset(offset)

            .limit(limit)

            .options(*self._options())

        ).all()

        return rows, total



    def add(self, db: Session, row: Shareholder) -> Shareholder:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: Shareholder) -> None:

        db.delete(row)

        db.flush()
