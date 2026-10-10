"""Data access for Bank Clearance. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.bank_clearance_domain.models.bank_clearance import BankClearance

from app.core.pagination import normalise_paging



__all__ = ["BankClearanceRepository"]





class BankClearanceRepository:

    model = BankClearance



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, clearance_id: uuid.UUID

    ) -> Optional[BankClearance]:

        return db.scalar(

            select(BankClearance)

            .options(selectinload(BankClearance.payment_entries))

            .where(

                BankClearance.business_id == business_id,

                BankClearance.id == clearance_id,

            )

        )



    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[BankClearance]:

        return db.scalar(

            select(BankClearance).where(

                BankClearance.business_id == business_id, BankClearance.name == name

            )

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """No ``autoname`` upstream, so a per-tenant counter is used."""

        count = int(

            db.scalar(

                select(func.count())

                .select_from(BankClearance)

                .where(BankClearance.business_id == business_id)

            )

            or 0

        )

        return f"BC-{count + 1:05d}"



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        account_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[BankClearance], int]:

        offset, limit = normalise_paging(offset, limit)



        conditions = [BankClearance.business_id == business_id]

        if account_id is not None:

            conditions.append(BankClearance.account_id == account_id)



        total = int(

            db.scalar(select(func.count()).select_from(BankClearance).where(*conditions)) or 0

        )

        rows = db.scalars(

            select(BankClearance)

            .options(selectinload(BankClearance.payment_entries))

            .where(*conditions)

            .order_by(BankClearance.name.desc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



    def add(self, db: Session, clearance: BankClearance) -> BankClearance:

        db.add(clearance)

        db.flush()

        return clearance



    def delete(self, db: Session, clearance: BankClearance) -> None:

        db.delete(clearance)

        db.flush()
