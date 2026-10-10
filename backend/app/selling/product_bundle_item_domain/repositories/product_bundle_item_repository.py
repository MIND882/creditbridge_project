"""Data access for ProductBundleItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.selling.product_bundle_item_domain.models.product_bundle_item import ProductBundleItem

from app.core.pagination import normalise_paging



__all__ = ["ProductBundleItemRepository"]





class ProductBundleItemRepository:

    model = ProductBundleItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ProductBundleItem]:

        return db.scalar(

            select(ProductBundleItem).where(

                ProductBundleItem.business_id == business_id, ProductBundleItem.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ProductBundleItem]:

        return db.scalar(

            select(ProductBundleItem).where(

                ProductBundleItem.business_id == business_id, ProductBundleItem.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[ProductBundleItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ProductBundleItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(ProductBundleItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(ProductBundleItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ProductBundleItem)

            .where(*conditions)

            .order_by(ProductBundleItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
