"""Data access for PurchaseReceipt. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.purchase_receipt_domain.models.purchase_receipt import PurchaseReceipt

from app.core.pagination import normalise_paging



__all__ = ["PurchaseReceiptRepository"]





class PurchaseReceiptRepository:

    model = PurchaseReceipt





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PurchaseReceipt]:

        return db.scalar(

            select(PurchaseReceipt).where(

                PurchaseReceipt.business_id == business_id, PurchaseReceipt.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[PurchaseReceipt]:

        return db.scalar(

            select(PurchaseReceipt).where(

                PurchaseReceipt.business_id == business_id, PurchaseReceipt.name == name

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

    ) -> tuple[Sequence[PurchaseReceipt], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PurchaseReceipt.business_id == business_id]

        if not include_cancelled:

            conditions.append(PurchaseReceipt.docstatus != 2)

        if search:

            conditions.append(PurchaseReceipt.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(PurchaseReceipt).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PurchaseReceipt)

            .where(*conditions)

            .order_by(PurchaseReceipt.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: PurchaseReceipt) -> PurchaseReceipt:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: PurchaseReceipt) -> None:

        db.delete(row)

        db.flush()
