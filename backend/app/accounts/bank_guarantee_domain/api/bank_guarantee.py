"""

HTTP surface for Bank Guarantee.



Submittable, so it adds ``/submit``, ``/cancel`` and ``/amend`` -- the API

equivalent of ERPNext's toolbar actions.

"""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.bank_guarantee_domain.models.bank_guarantee import BGType

from app.accounts.bank_guarantee_domain.schemas.bank_guarantee import (

    BankGuaranteeCreate,

    BankGuaranteeListResponse,

    BankGuaranteeRead,

    BankGuaranteeStatusResult,

    BankGuaranteeUpdate,

)

from app.accounts.bank_guarantee_domain.services.bank_guarantee_service import (

    BankGuaranteeService,

)

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = BankGuaranteeService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





def _read(row: object) -> BankGuaranteeRead:

    return BankGuaranteeRead.model_validate(row)





def _status(row: object) -> BankGuaranteeStatusResult:

    return BankGuaranteeStatusResult(

        id=row.id,  # type: ignore[attr-defined]

        name=row.name,  # type: ignore[attr-defined]

        docstatus=int(row.docstatus),  # type: ignore[attr-defined]

    )





@router.post(

    "",

    response_model=BankGuaranteeRead,

    status_code=status.HTTP_201_CREATED,

    summary="Create a bank guarantee (draft)",

)

def create_bank_guarantee(

    payload: BankGuaranteeCreate, db: DbDep, business_id: BusinessDep

) -> BankGuaranteeRead:

    try:

        return _read(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=BankGuaranteeListResponse, summary="List bank guarantees")

def list_bank_guarantees(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    bg_type: Optional[BGType] = Query(default=None),

    docstatus: Optional[int] = Query(default=None, ge=0, le=2),

    include_cancelled: bool = Query(default=False),

) -> BankGuaranteeListResponse:

    page = _service.list(

        db,

        business_id,

        offset=offset,

        limit=limit,

        bg_type=bg_type.value if bg_type else None,

        docstatus=docstatus,

        include_cancelled=include_cancelled,

    )

    return BankGuaranteeListResponse.from_result(page, [_read(r) for r in page.items])





@router.get(

    "/{guarantee_id}", response_model=BankGuaranteeRead, summary="Get one bank guarantee"

)

def get_bank_guarantee(

    guarantee_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> BankGuaranteeRead:

    try:

        return _read(_service.get(db, business_id, guarantee_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch(

    "/{guarantee_id}", response_model=BankGuaranteeRead, summary="Update a draft guarantee"

)

def update_bank_guarantee(

    guarantee_id: uuid.UUID,

    payload: BankGuaranteeUpdate,

    db: DbDep,

    business_id: BusinessDep,

) -> BankGuaranteeRead:

    try:

        return _read(_service.update(db, business_id, guarantee_id, payload))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete(

    "/{guarantee_id}",

    status_code=status.HTTP_204_NO_CONTENT,

    summary="Delete a draft guarantee",

)

def delete_bank_guarantee(

    guarantee_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> Response:

    # `-> Response` not `-> None`: under PEP 563 the annotation becomes the

    # string "None", which FastAPI resolves to the truthy NoneType class and

    # then rejects for a 204 at import time.

    try:

        _service.delete(db, business_id, guarantee_id)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)





@router.post(

    "/{guarantee_id}/submit",

    response_model=BankGuaranteeStatusResult,

    summary="Submit (draft -> submitted)",

)

def submit_bank_guarantee(

    guarantee_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> BankGuaranteeStatusResult:

    try:

        return _status(_service.submit(db, business_id, guarantee_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.post(

    "/{guarantee_id}/cancel",

    response_model=BankGuaranteeStatusResult,

    summary="Cancel (submitted -> cancelled)",

)

def cancel_bank_guarantee(

    guarantee_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> BankGuaranteeStatusResult:

    try:

        return _status(_service.cancel(db, business_id, guarantee_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.post(

    "/{guarantee_id}/amend",

    response_model=BankGuaranteeRead,

    status_code=status.HTTP_201_CREATED,

    summary="Amend (cancelled -> new draft)",

)

def amend_bank_guarantee(

    guarantee_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> BankGuaranteeRead:

    try:

        return _read(_service.amend(db, business_id, guarantee_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc
