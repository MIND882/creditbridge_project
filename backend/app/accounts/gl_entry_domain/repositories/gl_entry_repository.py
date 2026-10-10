"""

Data access for GL Entry. Scoped by ``business_id`` throughout.



Every balance read filters on ``is_cancelled == 0`` rather than on ``docstatus``,

matching upstream's queries exactly.

"""



from __future__ import annotations



import uuid

from datetime import date

from decimal import Decimal

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.gl_entry_domain.models.gl_entry import GLEntry

from app.core.pagination import normalise_paging



__all__ = ["GLEntryRepository"]



ZERO = Decimal("0")





class GLEntryRepository:

    model = GLEntry



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, entry_id: uuid.UUID

    ) -> Optional[GLEntry]:

        return db.scalar(

            select(GLEntry).where(

                GLEntry.business_id == business_id, GLEntry.id == entry_id

            )

        )



    def get_by_name(self, db: Session, business_id: uuid.UUID, name: str) -> Optional[GLEntry]:

        return db.scalar(

            select(GLEntry).where(

                GLEntry.business_id == business_id, GLEntry.name == name

            )

        )



    def next_name(self, db: Session, business_id: uuid.UUID, on: date) -> str:

        """``ACC-GLE-.YYYY.-.#####``, counter scoped per tenant and year."""

        start, end = date(on.year, 1, 1), date(on.year, 12, 31)

        count = int(

            db.scalar(

                select(func.count())

                .select_from(GLEntry)

                .where(

                    GLEntry.business_id == business_id,

                    GLEntry.created_at >= start,

                    GLEntry.created_at <= end,

                )

            )

            or 0

        )

        return f"ACC-GLE-{on.year}-{count + 1:05d}"



    # ── balances ─────────────────────────────────────────────────────────────

    def account_balance(

        self,

        db: Session,

        business_id: uuid.UUID,

        account_id: uuid.UUID,

        *,

        up_to: Optional[date] = None,

        include_cancelled: bool = False,

    ) -> tuple[Decimal, Decimal]:

        """

        ``(total_debit, total_credit)`` for one account, excluding cancelled rows.



        This is the query the account / cost-centre services need in order to

        stop failing open.

        """

        conditions = [

            GLEntry.business_id == business_id,

            GLEntry.account_id == account_id,

        ]

        if not include_cancelled:

            conditions.append(GLEntry.is_cancelled.is_(False))

        if up_to is not None:

            conditions.append(GLEntry.posting_date <= up_to)



        row = db.execute(

            select(

                func.coalesce(func.sum(GLEntry.debit), 0),

                func.coalesce(func.sum(GLEntry.credit), 0),

            ).where(*conditions)

        ).one()

        return Decimal(str(row[0])), Decimal(str(row[1]))



    def cost_center_balance(

        self,

        db: Session,

        business_id: uuid.UUID,

        cost_center_id: uuid.UUID,

        *,

        up_to: Optional[date] = None,

    ) -> tuple[Decimal, Decimal]:

        conditions = [

            GLEntry.business_id == business_id,

            GLEntry.cost_center_id == cost_center_id,

            GLEntry.is_cancelled.is_(False),

        ]

        if up_to is not None:

            conditions.append(GLEntry.posting_date <= up_to)



        row = db.execute(

            select(

                func.coalesce(func.sum(GLEntry.debit), 0),

                func.coalesce(func.sum(GLEntry.credit), 0),

            ).where(*conditions)

        ).one()

        return Decimal(str(row[0])), Decimal(str(row[1]))



    def balances_by_cost_center(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        up_to: Optional[date] = None,

    ) -> dict[uuid.UUID, Decimal]:

        """

        ``{cost_center_id: debit - credit}`` across the tenant.



        Used by the cost-centre allocation guards, which need per-child totals

        without issuing one query per cost centre.

        """

        conditions = [

            GLEntry.business_id == business_id,

            GLEntry.is_cancelled.is_(False),

            GLEntry.cost_center_id.is_not(None),

        ]

        if up_to is not None:

            conditions.append(GLEntry.posting_date <= up_to)



        rows = db.execute(

            select(

                GLEntry.cost_center_id,

                func.coalesce(func.sum(GLEntry.debit), 0)

                - func.coalesce(func.sum(GLEntry.credit), 0),

            )

            .where(*conditions)

            .group_by(GLEntry.cost_center_id)

        ).all()

        return {cc_id: Decimal(str(balance)) for cc_id, balance in rows}



    def has_entries_for_cost_center(

        self, db: Session, business_id: uuid.UUID, cost_center_id: uuid.UUID

    ) -> bool:

        return (

            db.scalar(

                select(func.count())

                .select_from(GLEntry)

                .where(

                    GLEntry.business_id == business_id,

                    GLEntry.cost_center_id == cost_center_id,

                    GLEntry.is_cancelled.is_(False),

                )

            )

            or 0

        ) > 0



    def last_entry_date_for_cost_center(

        self, db: Session, business_id: uuid.UUID, cost_center_id: uuid.UUID

    ) -> Optional[date]:

        """

        The newest non-cancelled posting date for a cost centre.



        Port of the lookup behind

        ``validate_from_date_based_on_existing_gle``, which refuses a cost-centre

        allocation that starts before the centre already has history.

        """

        return db.scalar(

            select(func.max(GLEntry.posting_date)).where(

                GLEntry.business_id == business_id,

                GLEntry.cost_center_id == cost_center_id,

                GLEntry.is_cancelled.is_(False),

            )

        )



    def has_entries_for_account(

        self, db: Session, business_id: uuid.UUID, account_id: uuid.UUID

    ) -> bool:

        return (

            db.scalar(

                select(func.count())

                .select_from(GLEntry)

                .where(

                    GLEntry.business_id == business_id,

                    GLEntry.account_id == account_id,

                    GLEntry.is_cancelled.is_(False),

                )

            )

            or 0

        ) > 0



    def list_for_voucher(

        self, db: Session, business_id: uuid.UUID, voucher_type: str, voucher_no: str

    ) -> list[GLEntry]:

        return list(

            db.scalars(

                select(GLEntry).where(

                    GLEntry.business_id == business_id,

                    GLEntry.voucher_type == voucher_type,

                    GLEntry.voucher_no == voucher_no,

                )

            )

        )



    # ── writes ───────────────────────────────────────────────────────────────

    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        account_id: Optional[uuid.UUID] = None,

        cost_center_id: Optional[uuid.UUID] = None,

        voucher_type: Optional[str] = None,

        voucher_no: Optional[str] = None,

        party_type: Optional[str] = None,

        party: Optional[str] = None,

        from_date: Optional[date] = None,

        to_date: Optional[date] = None,

        include_cancelled: bool = False,

    ) -> tuple[Sequence[GLEntry], int]:

        offset, limit = normalise_paging(offset, limit)



        conditions = [GLEntry.business_id == business_id]

        if account_id is not None:

            conditions.append(GLEntry.account_id == account_id)

        if cost_center_id is not None:

            conditions.append(GLEntry.cost_center_id == cost_center_id)

        if voucher_type:

            conditions.append(GLEntry.voucher_type == voucher_type)

        if voucher_no:

            conditions.append(GLEntry.voucher_no == voucher_no)

        if party_type:

            conditions.append(GLEntry.party_type == party_type)

        if party:

            conditions.append(GLEntry.party == party)

        if from_date is not None:

            conditions.append(GLEntry.posting_date >= from_date)

        if to_date is not None:

            conditions.append(GLEntry.posting_date <= to_date)

        if not include_cancelled:

            conditions.append(GLEntry.is_cancelled.is_(False))



        total = int(

            db.scalar(select(func.count()).select_from(GLEntry).where(*conditions)) or 0

        )

        rows = db.scalars(

            select(GLEntry)

            .where(*conditions)

            .order_by(GLEntry.posting_date.desc(), GLEntry.name.desc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



    def add(self, db: Session, entry: GLEntry) -> GLEntry:

        db.add(entry)

        db.flush()

        return entry
