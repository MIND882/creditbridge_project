"""Data access for Bank Guarantee. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from datetime import date

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.bank_guarantee_domain.models.bank_guarantee import BankGuarantee

from app.core.pagination import normalise_paging



__all__ = ["BankGuaranteeRepository"]





class BankGuaranteeRepository:

    model = BankGuarantee



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, guarantee_id: uuid.UUID

    ) -> Optional[BankGuarantee]:

        return db.scalar(

            select(BankGuarantee).where(

                BankGuarantee.business_id == business_id,

                BankGuarantee.id == guarantee_id,

            )

        )



    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[BankGuarantee]:

        return db.scalar(

            select(BankGuarantee).where(

                BankGuarantee.business_id == business_id, BankGuarantee.name == name

            )

        )



    def next_name(self, db: Session, business_id: uuid.UUID, on: date) -> str:

        """

        ``ACC-BG-.YYYY.-.#####`` scoped per tenant and year.



        The counter is per (tenant, year) so the series restarts each financial

        year, matching the ``.YYYY.`` token in the upstream series.

        """

        start, end = date(on.year, 1, 1), date(on.year, 12, 31)

        count = int(

            db.scalar(

                select(func.count())

                .select_from(BankGuarantee)

                .where(

                    BankGuarantee.business_id == business_id,

                    BankGuarantee.created_at >= start,

                    BankGuarantee.created_at <= end,

                )

            )

            or 0

        )

        return f"ACC-BG-{on.year}-{count + 1:05d}"



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        bg_type: Optional[str] = None,

        docstatus: Optional[int] = None,

        include_cancelled: bool = False,

    ) -> tuple[Sequence[BankGuarantee], int]:

        offset, limit = normalise_paging(offset, limit)



        conditions = [BankGuarantee.business_id == business_id]

        if bg_type:

            conditions.append(BankGuarantee.bg_type == bg_type)

        if docstatus is not None:

            conditions.append(BankGuarantee.docstatus == docstatus)

        elif not include_cancelled:

            # Mirrors ERPNext's ubiquitous `docstatus != 2`.

            conditions.append(BankGuarantee.docstatus != 2)



        total = int(

            db.scalar(select(func.count()).select_from(BankGuarantee).where(*conditions)) or 0

        )

        rows = db.scalars(

            select(BankGuarantee)

            .where(*conditions)

            .order_by(BankGuarantee.name.desc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



    def add(self, db: Session, guarantee: BankGuarantee) -> BankGuarantee:

        db.add(guarantee)

        db.flush()

        return guarantee



    def delete(self, db: Session, guarantee: BankGuarantee) -> None:

        db.delete(guarantee)

        db.flush()
