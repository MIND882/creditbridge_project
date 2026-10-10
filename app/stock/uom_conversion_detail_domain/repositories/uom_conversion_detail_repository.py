"""Data access for UomConversionDetail. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.uom_conversion_detail_domain.models.uom_conversion_detail import UomConversionDetail

from app.core.pagination import normalise_paging



__all__ = ["UomConversionDetailRepository"]





class UomConversionDetailRepository:

    model = UomConversionDetail





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[UomConversionDetail]:

        return db.scalar(

            select(UomConversionDetail).where(

                UomConversionDetail.business_id == business_id, UomConversionDetail.id == row_id

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[UomConversionDetail], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [UomConversionDetail.business_id == business_id]

        if parent_id is not None:

            conditions.append(UomConversionDetail.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(UomConversionDetail).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(UomConversionDetail)

            .where(*conditions)

            .order_by(UomConversionDetail.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
