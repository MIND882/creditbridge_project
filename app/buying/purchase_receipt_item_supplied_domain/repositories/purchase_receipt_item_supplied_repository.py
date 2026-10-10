"""Data access for PurchaseReceiptItemSupplied. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.buying.purchase_receipt_item_supplied_domain.models.purchase_receipt_item_supplied import PurchaseReceiptItemSupplied

from app.core.pagination import normalise_paging



__all__ = ["PurchaseReceiptItemSuppliedRepository"]





class PurchaseReceiptItemSuppliedRepository:

    model = PurchaseReceiptItemSupplied





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PurchaseReceiptItemSupplied]:

        return db.scalar(

            select(PurchaseReceiptItemSupplied).where(

                PurchaseReceiptItemSupplied.business_id == business_id, PurchaseReceiptItemSupplied.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[PurchaseReceiptItemSupplied]:

        return db.scalar(

            select(PurchaseReceiptItemSupplied).where(

                PurchaseReceiptItemSupplied.business_id == business_id, PurchaseReceiptItemSupplied.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[PurchaseReceiptItemSupplied], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PurchaseReceiptItemSupplied.business_id == business_id]

        if parent_id is not None:

            conditions.append(PurchaseReceiptItemSupplied.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(PurchaseReceiptItemSupplied).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PurchaseReceiptItemSupplied)

            .where(*conditions)

            .order_by(PurchaseReceiptItemSupplied.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
