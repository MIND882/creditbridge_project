"""Data access for FiscalYear. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import datetime as dt

import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.fiscal_year_domain.models.fiscal_year import FiscalYear

from app.core.pagination import normalise_paging



__all__ = ["FiscalYearRepository"]





class FiscalYearRepository:

    model = FiscalYear



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks conftest

        # collection with "failed to locate a name".

        return [selectinload(FiscalYear.companies)]



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[FiscalYear]:

        return db.scalar(

            select(FiscalYear)

            .where(

                FiscalYear.business_id == business_id,

                FiscalYear.id == row_id,

            )

            .options(*self._options())

        )



    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[FiscalYear]:

        return db.scalar(

            select(FiscalYear)

            .where(

                FiscalYear.business_id == business_id,

                FiscalYear.name == name,

            )

            .options(*self._options())

        )



    def find_overlapping(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        start: dt.date,

        end: dt.date,

        exclude_id: Optional[uuid.UUID] = None,

    ) -> Sequence[FiscalYear]:

        """

        Fiscal years whose date range touches ``[start, end]``.



        Port of the ``frappe.qb`` predicate in ``validate_overlap``:



            (year_start_date <= self.year_end_date)

            & (year_end_date >= self.year_start_date)

            & (name != self.name)



        Upstream excludes by ``name``; excluding by ``id`` here is the same

        intent and stays correct when a year is renamed.

        """

        conditions = [

            FiscalYear.business_id == business_id,

            FiscalYear.year_start_date <= end,

            FiscalYear.year_end_date >= start,

        ]

        if exclude_id is not None:

            conditions.append(FiscalYear.id != exclude_id)

        return db.scalars(

            select(FiscalYear).where(*conditions).options(*self._options())

        ).all()



    def get_for_date(

        self, db: Session, business_id: uuid.UUID, on: dt.date

    ) -> Optional[FiscalYear]:

        """

        The enabled fiscal year containing ``on``, if any.



        Disabled years are excluded, matching upstream ``_get_fiscal_years``,

        which filters ``FY.disabled == 0``. Including them would let a

        transaction validate against a year the tenant has closed off.

        """

        return db.scalar(

            select(FiscalYear)

            .where(

                FiscalYear.business_id == business_id,

                FiscalYear.year_start_date <= on,

                FiscalYear.year_end_date >= on,

                FiscalYear.disabled.is_(False),

            )

            .options(*self._options())

        )



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        include_disabled: bool = True,

        search: Optional[str] = None,

    ) -> tuple[Sequence[FiscalYear], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [FiscalYear.business_id == business_id]

        if not include_disabled:

            conditions.append(FiscalYear.disabled.is_(False))

        if search:

            conditions.append(FiscalYear.year.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(FiscalYear).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(FiscalYear)

            .where(*conditions)

            .order_by(FiscalYear.year_start_date.desc())

            .offset(offset)

            .limit(limit)

            .options(*self._options())

        ).all()

        return rows, total



    def add(self, db: Session, row: FiscalYear) -> FiscalYear:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: FiscalYear) -> None:

        db.delete(row)

        db.flush()
