"""Data access for Tax Withholding Category. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.tax_withholding_category_domain.models.tax_withholding_category import (

    TaxWithholdingCategory,

)

from app.core.pagination import normalise_paging



__all__ = ["TaxWithholdingCategoryRepository"]





class TaxWithholdingCategoryRepository:

    model = TaxWithholdingCategory



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks conftest

        # collection with "failed to locate a name".

        return [

            selectinload(TaxWithholdingCategory.rates),

            selectinload(TaxWithholdingCategory.accounts),

        ]



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, category_id: uuid.UUID

    ) -> Optional[TaxWithholdingCategory]:

        return db.scalar(

            select(TaxWithholdingCategory)

            .where(

                TaxWithholdingCategory.business_id == business_id,

                TaxWithholdingCategory.id == category_id,

            )

            .options(*self._options())

        )



    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[TaxWithholdingCategory]:

        return db.scalar(

            select(TaxWithholdingCategory)

            .where(

                TaxWithholdingCategory.business_id == business_id,

                TaxWithholdingCategory.name == name,

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

        search: Optional[str] = None,

    ) -> tuple[Sequence[TaxWithholdingCategory], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [TaxWithholdingCategory.business_id == business_id]

        if search:

            like = f"%{search.strip()}%"

            conditions.append(

                TaxWithholdingCategory.name.ilike(like)

                | TaxWithholdingCategory.category_name.ilike(like)

            )



        total = int(

            db.scalar(

                select(func.count()).select_from(TaxWithholdingCategory).where(*conditions)

            )

            or 0

        )

        rows = db.scalars(

            select(TaxWithholdingCategory)

            .where(*conditions)

            .order_by(TaxWithholdingCategory.name.asc())

            .offset(offset)

            .limit(limit)

            .options(*self._options())

        ).all()

        return rows, total



    def add(self, db: Session, row: TaxWithholdingCategory) -> TaxWithholdingCategory:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: TaxWithholdingCategory) -> None:

        db.delete(row)

        db.flush()
