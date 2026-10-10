"""Business logic for Item Website Specification -- port of

``erpnext/stock/doctype/item_website_specification/item_website_specification.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.item_website_specification_domain.models.item_website_specification import ItemWebsiteSpecification

from app.stock.item_website_specification_domain.repositories.item_website_specification_repository import (

    ItemWebsiteSpecificationRepository,

)

from app.stock.item_website_specification_domain.schemas.item_website_specification import (

    ItemWebsiteSpecificationCreate,

    ItemWebsiteSpecificationUpdate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ItemWebsiteSpecificationService"]





class ItemWebsiteSpecificationService:

    def __init__(self, repository: Optional[ItemWebsiteSpecificationRepository] = None) -> None:

        self.repository = repository or ItemWebsiteSpecificationRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ItemWebsiteSpecification:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Item Website Specification", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: ItemWebsiteSpecification

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ItemWebsiteSpecification:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ItemWebsiteSpecification]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ItemWebsiteSpecification].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(ItemWebsiteSpecification).where(

                    ItemWebsiteSpecification.business_id == business_id

                )

            )

            or 0

        )

        return f"ITE-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: ItemWebsiteSpecificationCreate

    ) -> ItemWebsiteSpecification:

        row = ItemWebsiteSpecification(

            business_id=business_id,

            name=self.next_name(db, business_id),

            label=payload.label,

            description=payload.description,

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

        payload: ItemWebsiteSpecificationUpdate,

    ) -> ItemWebsiteSpecification:

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
