"""Data access for PartyAccount. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.party_account_domain.models.party_account import PartyAccount

from app.core.pagination import normalise_paging



__all__ = ["PartyAccountRepository"]





class PartyAccountRepository:

    model = PartyAccount



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PartyAccount]:

        return db.scalar(

            select(PartyAccount).where(

                PartyAccount.business_id == business_id, PartyAccount.id == row_id

            )

        )



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        party_account_of: Optional[str] = None,

    ) -> tuple[Sequence[PartyAccount], int]:

        """

        Unlike the other child tables, there is no ``parent_id`` to filter on:

        Customer/Supplier are not converted, so rows are keyed on the party-type

        label instead.

        """

        offset, limit = normalise_paging(offset, limit)



        conditions = [PartyAccount.business_id == business_id]

        if party_account_of:

            conditions.append(PartyAccount.party_account_of == party_account_of)



        total = int(

            db.scalar(select(func.count()).select_from(PartyAccount).where(*conditions)) or 0

        )

        rows = db.scalars(

            select(PartyAccount)

            .where(*conditions)

            .order_by(PartyAccount.party_account_of.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
