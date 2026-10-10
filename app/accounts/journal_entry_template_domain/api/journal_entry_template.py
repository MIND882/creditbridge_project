"""HTTP surface for Journal Entry Template."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.journal_entry_domain.models.journal_entry import JournalVoucherType

from app.accounts.journal_entry_template_domain.schemas.journal_entry_template import (

    JournalEntryTemplateCreate,

    JournalEntryTemplateListResponse,

    JournalEntryTemplateRead,

    JournalEntryTemplateUpdate,

)

from app.accounts.journal_entry_template_domain.services.journal_entry_template_service import (

    JournalEntryTemplateService,

)

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = JournalEntryTemplateService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.post(

    "", response_model=JournalEntryTemplateRead, status_code=status.HTTP_201_CREATED,

    summary="Create a journal entry template",

)

def create_journal_entry_template(

    payload: JournalEntryTemplateCreate, db: DbDep, business_id: BusinessDep

) -> JournalEntryTemplateRead:

    try:

        return JournalEntryTemplateRead.model_validate(

            _service.create(db, business_id, payload)

        )

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get(

    "", response_model=JournalEntryTemplateListResponse,

    summary="List journal entry templates",

)

def list_journal_entry_templates(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    voucher_type: Optional[JournalVoucherType] = Query(default=None),

    search: Optional[str] = Query(default=None, max_length=140),

) -> JournalEntryTemplateListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit,

        voucher_type=voucher_type, search=search,

    )

    return JournalEntryTemplateListResponse.from_result(

        page, [JournalEntryTemplateRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=JournalEntryTemplateRead, summary="Get one template"

)

def get_journal_entry_template(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> JournalEntryTemplateRead:

    try:

        return JournalEntryTemplateRead.model_validate(

            _service.get(db, business_id, row_id)

        )

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{row_id}", response_model=JournalEntryTemplateRead, summary="Update")

def update_journal_entry_template(

    row_id: uuid.UUID, payload: JournalEntryTemplateUpdate, db: DbDep,

    business_id: BusinessDep,

) -> JournalEntryTemplateRead:

    try:

        return JournalEntryTemplateRead.model_validate(

            _service.update(db, business_id, row_id, payload)

        )

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete("/{row_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete")

def delete_journal_entry_template(

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
