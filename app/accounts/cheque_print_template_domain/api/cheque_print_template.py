"""HTTP surface for Cheque Print Template."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.cheque_print_template_domain.schemas.cheque_print_template import (

        ChequePrintTemplateCreate,

    ChequePrintTemplateUpdate,

    ChequePrintTemplateRead,

    ChequePrintTemplateListResponse,

)

from app.accounts.cheque_print_template_domain.services.cheque_print_template_service import ChequePrintTemplateService

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = ChequePrintTemplateService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.post(

    "", response_model=ChequePrintTemplateRead, status_code=status.HTTP_201_CREATED,

    summary="Create a cheque print template",

)

def create_cheque_print_template(

    payload: ChequePrintTemplateCreate, db: DbDep, business_id: BusinessDep

) -> ChequePrintTemplateRead:

    try:

        return ChequePrintTemplateRead.model_validate(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=ChequePrintTemplateListResponse, summary="List cheque print templates")

def list_cheque_print_template(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    search: Optional[str] = Query(default=None, max_length=140),

) -> ChequePrintTemplateListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, search=search,

    )

    return ChequePrintTemplateListResponse.from_result(

        page, [ChequePrintTemplateRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=ChequePrintTemplateRead, summary="Get one cheque print template"

)

def get_cheque_print_template(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> ChequePrintTemplateRead:

    try:

        return ChequePrintTemplateRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{row_id}", response_model=ChequePrintTemplateRead, summary="Update")

def update_cheque_print_template(

    row_id: uuid.UUID, payload: ChequePrintTemplateUpdate, db: DbDep, business_id: BusinessDep

) -> ChequePrintTemplateRead:

    try:

        return ChequePrintTemplateRead.model_validate(

            _service.update(db, business_id, row_id, payload)

        )

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete("/{row_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete")

def delete_cheque_print_template(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> Response:

    # `-> Response` not `-> None`: under PEP 563 the annotation becomes the

    # string "None", which FastAPI resolves to NoneType and then rejects for a

    # 204 at import time.

    try:

        _service.delete(db, business_id, row_id)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
