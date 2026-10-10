"""Read-only service for PaymentTermsTemplateDetail; writes go through the parent doctype."""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.payment_terms_template_detail_domain.models.payment_terms_template_detail import PaymentTermsTemplateDetail

from app.accounts.payment_terms_template_detail_domain.repositories.payment_terms_template_detail_repository import PaymentTermsTemplateDetailRepository

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PaymentTermsTemplateDetailService"]





class PaymentTermsTemplateDetailService:

    def __init__(self, repository: Optional[PaymentTermsTemplateDetailRepository] = None) -> None:

        self.repository = repository or PaymentTermsTemplateDetailRepository()



    def get(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> PaymentTermsTemplateDetail:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("PaymentTermsTemplateDetail", row_id)

        return row



    def list(self, db: Session, business_id: uuid.UUID, **filters: object) -> ResultPage[PaymentTermsTemplateDetail]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PaymentTermsTemplateDetail].build(

            rows, total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
