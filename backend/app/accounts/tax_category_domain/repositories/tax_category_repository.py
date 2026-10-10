"""Data access for Tax Category. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.tax_category_domain.models.tax_category import TaxCategory

from app.core.pagination import normalise_paging



__all__ = ["TaxCategoryRepository"]





class TaxCategoryRepository:

    model = TaxCategory



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, category_id: uuid.UUID

    ) -> Optional[TaxCategory]:

        return db.scalar(

            select(TaxCategory).where(

                TaxCategory.business_id == business_id, TaxCategory.id == category_id

            )

        )



    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[TaxCategory]:

        return db.scalar(

            select(TaxCategory).where(

                TaxCategory.business_id == business_id, TaxCategory.name == name

            )

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

    ) -> tuple[Sequence[TaxCategory], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [TaxCategory.business_id == business_id]

        if not include_disabled:

            conditions.append(TaxCategory.disabled.is_(False))

        if search:

            like = f"%{search.strip()}%"

            conditions.append(TaxCategory.name.ilike(like) | TaxCategory.title.ilike(like))



        total = int(

            db.scalar(select(func.count()).select_from(TaxCategory).where(*conditions)) or 0

        )

        rows = db.scalars(

            select(TaxCategory)

            .where(*conditions)

            .order_by(TaxCategory.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



    def add(self, db: Session, row: TaxCategory) -> TaxCategory:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: TaxCategory) -> None:

        db.delete(row)

        db.flush()
