"""Read-only HTTP surface for PaymentTermsTemplateDetail."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.payment_terms_template_detail_domain.schemas.payment_terms_template_detail import PaymentTermsTemplateDetailListResponse, PaymentTermsTemplateDetailRead

from app.accounts.payment_terms_template_detail_domain.services.payment_terms_template_detail_service import PaymentTermsTemplateDetailService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = PaymentTermsTemplateDetailService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=PaymentTermsTemplateDetailListResponse, summary="List PaymentTermsTemplateDetail rows")

def list_rows(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> PaymentTermsTemplateDetailListResponse:

    page = _service.list(db, business_id, offset=offset, limit=limit, parent_id=parent_id)

    return PaymentTermsTemplateDetailListResponse.from_result(

        page, [PaymentTermsTemplateDetailRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=PaymentTermsTemplateDetailRead, summary="Get one row")

def get_row(row_id: uuid.UUID, db: DbDep, business_id: BusinessDep) -> PaymentTermsTemplateDetailRead:

    try:

        return PaymentTermsTemplateDetailRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
