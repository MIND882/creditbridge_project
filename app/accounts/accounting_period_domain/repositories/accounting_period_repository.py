"""Data access for Accounting Period. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from datetime import date

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.accounting_period_domain.models.accounting_period import AccountingPeriod

from app.core.pagination import normalise_paging



__all__ = ["AccountingPeriodRepository"]





class AccountingPeriodRepository:

    model = AccountingPeriod



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, period_id: uuid.UUID

    ) -> Optional[AccountingPeriod]:

        return db.scalar(

            select(AccountingPeriod)

            .options(selectinload(AccountingPeriod.closed_documents))

            .where(

                AccountingPeriod.business_id == business_id,

                AccountingPeriod.id == period_id,

            )

        )



    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[AccountingPeriod]:

        return db.scalar(

            select(AccountingPeriod)

            .options(selectinload(AccountingPeriod.closed_documents))

            .where(

                AccountingPeriod.business_id == business_id,

                AccountingPeriod.name == name,

            )

        )



    def find_overlapping(

        self,

        db: Session,

        business_id: uuid.UUID,

        start_date: date,

        end_date: date,

        *,

        exclude_id: Optional[uuid.UUID] = None,

    ) -> Optional[AccountingPeriod]:

        """

        Port of ``validate_overlap``'s query.



        Upstream::



            .where(AccountingPeriod.start_date <= self.end_date)

            .where(AccountingPeriod.end_date >= self.start_date)

            .where(AccountingPeriod.name != self.name)

            .where(AccountingPeriod.company == self.company)



        The two comparisons are the standard interval-overlap test. Scoped to

        the tenant, which is what the ``company`` clause was doing.

        """

        conditions = [

            AccountingPeriod.business_id == business_id,

            AccountingPeriod.start_date <= end_date,

            AccountingPeriod.end_date >= start_date,

        ]

        if exclude_id is not None:

            conditions.append(AccountingPeriod.id != exclude_id)

        return db.scalar(

            select(AccountingPeriod).where(*conditions).order_by(AccountingPeriod.start_date).limit(1)

        )



    def find_period_for_date(

        self,

        db: Session,

        business_id: uuid.UUID,

        document_type: str,

        posting_date: date,

    ) -> Optional[AccountingPeriod]:

        """

        Port of ``validate_accounting_period_on_doc_save``.



        Finds an enabled period that (a) covers ``posting_date``, and (b) has

        the document type marked closed. Called by other domains before they

        write a dated document.

        """

        from app.accounts.accounting_period_domain.models.accounting_period import ClosedDocument



        return db.scalar(

            select(AccountingPeriod)

            .options(selectinload(AccountingPeriod.closed_documents))

            .join(ClosedDocument, ClosedDocument.parent_id == AccountingPeriod.id)

            .where(

                AccountingPeriod.business_id == business_id,

                AccountingPeriod.disabled.is_(False),

                ClosedDocument.closed.is_(True),

                ClosedDocument.document_type == document_type,

                AccountingPeriod.start_date <= posting_date,

                AccountingPeriod.end_date >= posting_date,

            )

            .limit(1)

        )



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        search: Optional[str] = None,

        include_disabled: bool = True,

    ) -> tuple[Sequence[AccountingPeriod], int]:

        offset, limit = normalise_paging(offset, limit)



        conditions = [AccountingPeriod.business_id == business_id]

        if search:

            conditions.append(

                AccountingPeriod.period_name.ilike(f"%{search}%")

                | AccountingPeriod.name.ilike(f"%{search}%")

            )

        if not include_disabled:

            conditions.append(AccountingPeriod.disabled.is_(False))



        total = int(

            db.scalar(select(func.count()).select_from(AccountingPeriod).where(*conditions)) or 0

        )

        rows = db.scalars(

            select(AccountingPeriod)

            .options(selectinload(AccountingPeriod.closed_documents))

            .where(*conditions)

            .order_by(AccountingPeriod.start_date.desc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



    def add(self, db: Session, period: AccountingPeriod) -> AccountingPeriod:

        db.add(period)

        db.flush()

        return period



    def delete(self, db: Session, period: AccountingPeriod) -> None:

        db.delete(period)

        db.flush()
