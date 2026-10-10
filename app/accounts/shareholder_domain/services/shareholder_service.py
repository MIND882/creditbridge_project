"""

Business logic for Shareholder -- port of

``erpnext/accounts/doctype/shareholder/shareholder.py``.



Upstream hook -> here

-------------------

``autoname`` (``naming_series:``)  :meth:`create` via

                                   :meth:`ShareholderRepository.next_name`

``before_save``                    :meth:`_before_save`

``onload`` / ``on_trash``          not ported (see below)



``before_save`` is the one piece of real logic upstream:



    for entry in self.share_balance:

        entry.amount = entry.no_of_shares * entry.rate



``amount`` is a derived column, so it is recomputed on every write and whatever

the client sent for it is discarded. That is a deliberate choice rather than an

oversight -- trusting a client-supplied amount on a share register would let the

holding and the valuation disagree.



``onload`` and ``on_trash`` only delegate to Frappe's address-and-contact

helpers, which have no counterpart here.

"""



from __future__ import annotations



import datetime as dt

import uuid

from decimal import Decimal

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.share_balance_domain.models.share_balance import ShareBalance

from app.accounts.shareholder_domain.models.shareholder import NAMING_SERIES, Shareholder

from app.accounts.shareholder_domain.repositories.shareholder_repository import (

    ShareholderRepository,

)

from app.accounts.shareholder_domain.schemas.shareholder import (

    ShareholderCreate,

    ShareholderUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ShareholderService"]





class ShareholderService:

    def __init__(self, repository: Optional[ShareholderRepository] = None) -> None:

        self.repository = repository or ShareholderRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Shareholder:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Shareholder", row_id)

        return row



    # ── ported hooks ─────────────────────────────────────────────────────────

    @staticmethod

    def _before_save(row: Shareholder) -> None:

        """Port of ``before_save``: recompute each holding's amount."""

        for entry in row.share_balance:

            entry.amount = Decimal(entry.no_of_shares) * Decimal(entry.rate)



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Shareholder:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[Shareholder]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[Shareholder].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_share_balance(

        self, business_id: uuid.UUID, row: Shareholder, balances: list[dict]

    ) -> None:

        row.share_balance.clear()

        for idx, item in enumerate(balances, start=1):

            row.share_balance.append(

                ShareBalance(

                    business_id=business_id,

                    idx=idx,

                    share_type_id=item["share_type_id"],

                    from_no=item["from_no"],

                    to_no=item["to_no"],

                    rate=item["rate"],

                    no_of_shares=item["no_of_shares"],

                    # Placeholder; ``_before_save`` overwrites it. The column is

                    # NOT NULL, so a value has to exist before the flush.

                    amount=Decimal("0"),

                    is_company=bool(item.get("is_company")),

                    current_state=item.get("current_state"),

                )

            )



    def create(

        self, db: Session, business_id: uuid.UUID, payload: ShareholderCreate

    ) -> Shareholder:

        title = payload.title.strip()

        if not title:

            raise DomainValidationError(

                "Title is mandatory", code="shareholder_title_mandatory"

            )



        row = Shareholder(

            business_id=business_id,

            name=self.repository.next_name(db, business_id, dt.date.today()),

            naming_series=NAMING_SERIES,

            title=title,

            folio_no=payload.folio_no,

            is_company=bool(payload.is_company),

            contact_list=payload.contact_list,

        )

        self._replace_share_balance(

            business_id, row, [b.model_dump() for b in payload.share_balance]

        )



        try:

            self._before_save(row)

            db.flush()  # children need ids before they are persisted

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

        payload: ShareholderUpdate,

    ) -> Shareholder:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "share_balance":

                    self._replace_share_balance(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

            self._before_save(row)

            db.flush()

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
