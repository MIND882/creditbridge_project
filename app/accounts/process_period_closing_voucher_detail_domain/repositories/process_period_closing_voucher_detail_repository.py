"""Data access for ProcessPeriodClosingVoucherDetail. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.process_period_closing_voucher_detail_domain.models.process_period_closing_voucher_detail import ProcessPeriodClosingVoucherDetail

from app.core.pagination import normalise_paging



__all__ = ["ProcessPeriodClosingVoucherDetailRepository"]





class ProcessPeriodClosingVoucherDetailRepository:

    model = ProcessPeriodClosingVoucherDetail





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ProcessPeriodClosingVoucherDetail]:

        return db.scalar(

            select(ProcessPeriodClosingVoucherDetail).where(

                ProcessPeriodClosingVoucherDetail.business_id == business_id, ProcessPeriodClosingVoucherDetail.id == row_id

            )

        )







    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[ProcessPeriodClosingVoucherDetail], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ProcessPeriodClosingVoucherDetail.business_id == business_id]

        if parent_id is not None:

            conditions.append(ProcessPeriodClosingVoucherDetail.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(ProcessPeriodClosingVoucherDetail).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ProcessPeriodClosingVoucherDetail)

            .where(*conditions)

            .order_by(ProcessPeriodClosingVoucherDetail.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


