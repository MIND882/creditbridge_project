"""Data access for ProductBundle. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.selling.product_bundle_domain.models.product_bundle import ProductBundle

from app.core.pagination import normalise_paging



__all__ = ["ProductBundleRepository"]





class ProductBundleRepository:

    model = ProductBundle





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ProductBundle]:

        return db.scalar(

            select(ProductBundle).where(

                ProductBundle.business_id == business_id, ProductBundle.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ProductBundle]:

        return db.scalar(

            select(ProductBundle).where(

                ProductBundle.business_id == business_id, ProductBundle.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        search: Optional[str] = None,

        include_cancelled: bool = False,

    ) -> tuple[Sequence[ProductBundle], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ProductBundle.business_id == business_id]

        if search:

            conditions.append(ProductBundle.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(ProductBundle).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ProductBundle)

            .where(*conditions)

            .order_by(ProductBundle.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: ProductBundle) -> ProductBundle:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: ProductBundle) -> None:

        db.delete(row)

        db.flush()
