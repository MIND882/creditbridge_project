"""Data access for ItemWiseTaxDetail. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.item_wise_tax_detail_domain.models.item_wise_tax_detail import ItemWiseTaxDetail

from app.core.pagination import normalise_paging



__all__ = ["ItemWiseTaxDetailRepository"]





class ItemWiseTaxDetailRepository:

    model = ItemWiseTaxDetail



    def get_by_id(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> Optional[ItemWiseTaxDetail]:

        return db.scalar(

            select(ItemWiseTaxDetail).where(

                ItemWiseTaxDetail.business_id == business_id, ItemWiseTaxDetail.id == row_id

            )

        )



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        item_row: Optional[str] = None,

    ) -> tuple[Sequence[ItemWiseTaxDetail], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ItemWiseTaxDetail.business_id == business_id]

        if item_row is not None:

            conditions.append(ItemWiseTaxDetail.item_row == item_row)

        total = int(

            db.scalar(select(func.count()).select_from(ItemWiseTaxDetail).where(*conditions)) or 0

        )

        rows = db.scalars(

            select(ItemWiseTaxDetail)

            .where(*conditions)

            .order_by(ItemWiseTaxDetail.item_row.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
