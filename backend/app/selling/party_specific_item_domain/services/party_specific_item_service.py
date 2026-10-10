"""Business logic for Party Specific Item -- port of

``erpnext/selling/doctype/party_specific_item/party_specific_item.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.selling.party_specific_item_domain.models.party_specific_item import PartySpecificItem

from app.selling.party_specific_item_domain.repositories.party_specific_item_repository import (

    PartySpecificItemRepository,

)

from app.selling.party_specific_item_domain.schemas.party_specific_item import (

    PartySpecificItemCreate,

    PartySpecificItemUpdate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PartySpecificItemService"]





class PartySpecificItemService:

    def __init__(self, repository: Optional[PartySpecificItemRepository] = None) -> None:

        self.repository = repository or PartySpecificItemRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PartySpecificItem:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Party Specific Item", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: PartySpecificItem

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PartySpecificItem:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PartySpecificItem]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PartySpecificItem].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(PartySpecificItem).where(

                    PartySpecificItem.business_id == business_id

                )

            )

            or 0

        )

        return f"PAR-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: PartySpecificItemCreate

    ) -> PartySpecificItem:

        row = PartySpecificItem(

            business_id=business_id,

            name=self.next_name(db, business_id),

            party_type=payload.party_type,

            party=payload.party,

            restrict_based_on=payload.restrict_based_on,

            based_on_value=payload.based_on_value,

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

        payload: PartySpecificItemUpdate,

    ) -> PartySpecificItem:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

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
