"""Data access for VariantField. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.variant_field_domain.models.variant_field import VariantField

from app.core.pagination import normalise_paging



__all__ = ["VariantFieldRepository"]





class VariantFieldRepository:

    model = VariantField





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[VariantField]:

        return db.scalar(

            select(VariantField).where(

                VariantField.business_id == business_id, VariantField.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[VariantField]:

        return db.scalar(

            select(VariantField).where(

                VariantField.business_id == business_id, VariantField.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[VariantField], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [VariantField.business_id == business_id]

        if parent_id is not None:

            conditions.append(VariantField.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(VariantField).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(VariantField)

            .where(*conditions)

            .order_by(VariantField.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
