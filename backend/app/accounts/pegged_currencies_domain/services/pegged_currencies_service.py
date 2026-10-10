# HAND-WRITTEN

"""

Business logic for Pegged Currencies -- port of

``erpnext/accounts/doctype/pegged_currencies/pegged_currencies.py``.







Upstream hooks:

    (none -- upstream's controller defines no hooks)



Upstream declares no validation, so `_validate` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.pegged_currencies_domain.models.pegged_currencies import PeggedCurrencies

from app.accounts.pegged_currency_details_domain.models.pegged_currency_details import PeggedCurrencyDetails

from app.accounts.pegged_currencies_domain.repositories.pegged_currencies_repository import (

    PeggedCurrenciesRepository,

)

from app.accounts.pegged_currencies_domain.schemas.pegged_currencies import (

    PeggedCurrenciesCreate,

    PeggedCurrenciesUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PeggedCurrenciesService"]





class PeggedCurrenciesService:

    def __init__(self, repository: Optional[PeggedCurrenciesRepository] = None) -> None:

        self.repository = repository or PeggedCurrenciesRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PeggedCurrencies:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Pegged Currencies", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: PeggedCurrencies

    ) -> None:

        """

        Upstream's controller defines no ``frappe.throw``, so there is

        no rule to port. Empty by design, not by omission.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PeggedCurrencies:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PeggedCurrencies]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PeggedCurrencies].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_pegged_currency_item(

        self, business_id: uuid.UUID, row: PeggedCurrencies, items: list[dict]

    ) -> None:

        row.pegged_currency_item.clear()

        for idx, item in enumerate(items, start=1):

            row.pegged_currency_item.append(

                PeggedCurrencyDetails(

                    business_id=business_id,

                    idx=idx,

                    source_currency=item.get('source_currency'),

                    pegged_exchange_rate=item.get('pegged_exchange_rate'),

                    pegged_against=item.get('pegged_against'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(PeggedCurrencies).where(

                    PeggedCurrencies.business_id == business_id

                )

            )

            or 0

        )

        return f"PEG-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: PeggedCurrenciesCreate

    ) -> PeggedCurrencies:

        row = PeggedCurrencies(

            business_id=business_id,

            name=self.next_name(db, business_id),



        )

        self._replace_pegged_currency_item(business_id, row, [x.model_dump() for x in payload.pegged_currency_item])



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

        payload: PeggedCurrenciesUpdate,

    ) -> PeggedCurrencies:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "pegged_currency_item":

                    self._replace_pegged_currency_item(business_id, row, value or [])

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
