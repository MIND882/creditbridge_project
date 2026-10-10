"""Data access for PaymentTermsTemplateDetail. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.payment_terms_template_detail_domain.models.payment_terms_template_detail import PaymentTermsTemplateDetail

from app.core.pagination import normalise_paging



__all__ = ["PaymentTermsTemplateDetailRepository"]





class PaymentTermsTemplateDetailRepository:

    model = PaymentTermsTemplateDetail



    def get_by_id(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> Optional[PaymentTermsTemplateDetail]:

        return db.scalar(

            select(PaymentTermsTemplateDetail).where(

                PaymentTermsTemplateDetail.business_id == business_id, PaymentTermsTemplateDetail.id == row_id

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

    ) -> tuple[Sequence[PaymentTermsTemplateDetail], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PaymentTermsTemplateDetail.business_id == business_id]

        if parent_id is not None:

            conditions.append(PaymentTermsTemplateDetail.parent_id == parent_id)

        total = int(

            db.scalar(select(func.count()).select_from(PaymentTermsTemplateDetail).where(*conditions)) or 0

        )

        rows = db.scalars(

            select(PaymentTermsTemplateDetail)

            .where(*conditions)

            .order_by(PaymentTermsTemplateDetail.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
