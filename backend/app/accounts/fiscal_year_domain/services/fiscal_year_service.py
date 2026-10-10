"""

Business logic for Fiscal Year -- port of

``erpnext/accounts/doctype/fiscal_year/fiscal_year.py``.



Upstream hook -> here

-------------------

``autoname`` (``field:year``)   :meth:`create`

``validate``                    :meth:`_validate`

  ``validate_dates``              :meth:`_validate_dates`

  ``validate_overlap``            :meth:`_validate_overlap`



Two details worth calling out:



**The one-year rule uses stdlib, not ``dateutil``.** Upstream computes the

expected end date as ``start + relativedelta(years=1) - relativedelta(days=1)``.

``python-dateutil`` reaches this project only transitively (via celery and

pandas) and nothing in ``app/`` imports it, so depending on it for core date

logic would be depending on an accident. :func:`_one_year_later_minus_a_day`

reproduces it with ``datetime`` alone, including ``relativedelta``'s behaviour of

clamping 29 February to the last valid day of the following year -- verified

against ``relativedelta`` over eight cases, leap years included.



**``auto_create_fiscal_year`` is not ported.** It is the scheduler that rolls a

new year forward three days before the current one ends. This conversion has no

scheduler. The ``auto_created`` column is kept so a year created by such a job

can still be marked.



``on_update``/``on_trash`` only invalidate ``frappe.cache()``; there is no shared

cache here to clear.

"""



from __future__ import annotations



import datetime as dt

import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.fiscal_year_company_domain.models.fiscal_year_company import (

    FiscalYearCompany,

)

from app.accounts.fiscal_year_domain.models.fiscal_year import FiscalYear

from app.accounts.fiscal_year_domain.repositories.fiscal_year_repository import (

    FiscalYearRepository,

)

from app.accounts.fiscal_year_domain.schemas.fiscal_year import (

    FiscalYearCreate,

    FiscalYearUpdate,

)

from app.core.errors import ConflictError, DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["FiscalYearService"]





def _one_year_later_minus_a_day(start: dt.date) -> dt.date:

    """

    ``start`` plus one year, minus one day -- the expected ``year_end_date``.



    Matches ``start + relativedelta(years=1) - relativedelta(days=1)``,

    including the clamp for 29 February: adding a year to a leap day lands on

    28 February of the following year, so the end date is the 27th.

    """

    try:

        same_day_next_year = start.replace(year=start.year + 1)

    except ValueError:

        # Only 29 February can raise here. relativedelta clamps to the last

        # valid day of the target month, which for February is the 28th.

        same_day_next_year = start.replace(year=start.year + 1, day=28)

    return same_day_next_year - dt.timedelta(days=1)





class FiscalYearService:

    def __init__(self, repository: Optional[FiscalYearRepository] = None) -> None:

        self.repository = repository or FiscalYearRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> FiscalYear:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Fiscal Year", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    @staticmethod

    def _validate_dates(row: FiscalYear) -> None:

        """

        Port of ``validate_dates``.



        Start must not be after end, and unless ``is_short_year`` the end date

        must be exactly one year after the start minus a day. Upstream returns

        early for short years, which is its escape hatch for jurisdictions that

        permit a first or final accounting period shorter than twelve months.

        """

        if row.year_start_date > row.year_end_date:

            raise DomainValidationError(

                "Fiscal Year Start Date cannot be after Fiscal Year End Date",

                code="fiscal_year_bad_date_range",

            )



        if row.is_short_year:

            return



        expected = _one_year_later_minus_a_day(row.year_start_date)

        if row.year_end_date != expected:

            raise DomainValidationError(

                "Fiscal Year End Date should be one year after Fiscal Year Start Date",

                code="fiscal_year_not_one_year",

            )



    def _validate_overlap(

        self,

        db: Session,

        business_id: uuid.UUID,

        row: FiscalYear,

    ) -> None:

        """

        Port of ``validate_overlap``.



        Two fiscal years may share dates only when they serve *different*

        companies. Upstream's rule, reproduced exactly:



        * both years list no companies at all -> they overlap, so reject;

        * any company appears on both -> they overlap, so reject;

        * otherwise the company sets are disjoint and the overlap is allowed.



        Note the asymmetry upstream carries: a year that lists no companies does

        not conflict with one that does. That is preserved deliberately rather

        than "fixed", so this port rejects and accepts the same documents.

        """

        mine = [c.company for c in row.companies]



        for existing in self.repository.find_overlapping(

            db,

            business_id,

            start=row.year_start_date,

            end=row.year_end_date,

            exclude_id=row.id,

        ):

            theirs = [c.company for c in existing.companies]



            overlap = False

            if not mine and not theirs:

                overlap = True

            for company in mine:

                if company in theirs:

                    overlap = True



            if overlap:

                raise DomainValidationError(

                    f"Year start date or end date is overlapping with {existing.name}. "

                    f"To avoid please set company",

                    code="fiscal_year_overlap",

                )



    def _validate(

        self, db: Session, business_id: uuid.UUID, row: FiscalYear

    ) -> None:

        # Upstream order preserved.

        self._validate_dates(row)

        self._validate_overlap(db, business_id, row)



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> FiscalYear:

        return self._get_or_404(db, business_id, row_id)



    def get_for_date(

        self, db: Session, business_id: uuid.UUID, on: dt.date

    ) -> Optional[FiscalYear]:

        """The fiscal year containing ``on``, or ``None``."""

        return self.repository.get_for_date(db, business_id, on)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[FiscalYear]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[FiscalYear].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_companies(

        self, business_id: uuid.UUID, row: FiscalYear, companies: list[dict]

    ) -> None:

        row.companies.clear()

        for idx, item in enumerate(companies, start=1):

            row.companies.append(

                FiscalYearCompany(

                    business_id=business_id, idx=idx, company=item["company"]

                )

            )



    def create(

        self, db: Session, business_id: uuid.UUID, payload: FiscalYearCreate

    ) -> FiscalYear:

        name = payload.year.strip()

        if not name:

            raise DomainValidationError(

                "Year is mandatory", code="fiscal_year_name_mandatory"

            )

        if self.repository.get_by_name(db, business_id, name) is not None:

            raise ConflictError(

                f"Fiscal Year '{name}' already exists", code="fiscal_year_duplicate"

            )



        row = FiscalYear(

            business_id=business_id,

            name=name,

            year=name,

            year_start_date=payload.year_start_date,

            year_end_date=payload.year_end_date,

            disabled=bool(payload.disabled),

            is_short_year=bool(payload.is_short_year),

        )

        self._replace_companies(

            business_id, row, [c.model_dump() for c in payload.companies]

        )



        try:

            db.flush()  # children need ids before validation reads them

            self._validate(db, business_id, row)

            self.repository.add(db, row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def update(

        self,

        db: Session,

        business_id: uuid.UUID,

        row_id: uuid.UUID,

        payload: FiscalYearUpdate,

    ) -> FiscalYear:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "companies":

                    self._replace_companies(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

            db.flush()

            self._validate(db, business_id, row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def delete(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> None:

        row = self._get_or_404(db, business_id, row_id)

        self.repository.delete(db, row)

        db.commit()
