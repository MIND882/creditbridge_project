"""

HTTP surface for Cost Center Allocation.



Submittable, so beyond the standard endpoints it exposes ``/submit``,

``/cancel`` and ``/amend`` -- the API equivalent of ERPNext's toolbar actions.

"""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.cost_center_allocation_domain.schemas.cost_center_allocation import (

    CostCenterAllocationCreate,

    CostCenterAllocationListResponse,

    CostCenterAllocationRead,

    CostCenterAllocationUpdate,

    DocStatusResult,

)

from app.accounts.cost_center_allocation_domain.services.cost_center_allocation_service import (

    CostCenterAllocationService,

)

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = CostCenterAllocationService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





def _read(row: object) -> CostCenterAllocationRead:

    return CostCenterAllocationRead.model_validate(row)





def _status(row: object) -> DocStatusResult:

    return DocStatusResult(

        id=row.id,  # type: ignore[attr-defined]

        name=row.name,  # type: ignore[attr-defined]

        docstatus=int(row.docstatus),  # type: ignore[attr-defined]

    )





@router.post(

    "",

    response_model=CostCenterAllocationRead,

    status_code=status.HTTP_201_CREATED,

    summary="Create a cost center allocation (draft)",

)

def create_allocation(

    payload: CostCenterAllocationCreate, db: DbDep, business_id: BusinessDep

) -> CostCenterAllocationRead:

    try:

        return _read(_service.create(db, business_id, payload).allocation)

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=CostCenterAllocationListResponse, summary="List allocations")

def list_allocations(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    main_cost_center_id: Optional[uuid.UUID] = Query(default=None),

    docstatus: Optional[int] = Query(default=None, ge=0, le=2),

    include_cancelled: bool = Query(default=False),

) -> CostCenterAllocationListResponse:

    page = _service.list(

        db,

        business_id,

        offset=offset,

        limit=limit,

        main_cost_center_id=main_cost_center_id,

        docstatus=docstatus,

        include_cancelled=include_cancelled,

    )

    return CostCenterAllocationListResponse.from_result(page, [_read(r) for r in page.items])





@router.get(

    "/{allocation_id}",

    response_model=CostCenterAllocationRead,

    summary="Get one allocation",

)

def get_allocation(

    allocation_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> CostCenterAllocationRead:

    try:

        return _read(_service.get(db, business_id, allocation_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch(

    "/{allocation_id}",

    response_model=CostCenterAllocationRead,

    summary="Update a draft allocation",

)

def update_allocation(

    allocation_id: uuid.UUID,

    payload: CostCenterAllocationUpdate,

    db: DbDep,

    business_id: BusinessDep,

) -> CostCenterAllocationRead:

    try:

        return _read(_service.update(db, business_id, allocation_id, payload).allocation)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete(

    "/{allocation_id}",

    status_code=status.HTTP_204_NO_CONTENT,

    summary="Delete a draft allocation",

)

def delete_allocation(

    allocation_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> Response:

    # `-> Response` not `-> None`: under PEP 563 the annotation becomes the

    # string "None", which FastAPI resolves to the truthy NoneType class and

    # then rejects for a 204 at import time.

    try:

        _service.delete(db, business_id, allocation_id)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)





@router.post(

    "/{allocation_id}/submit",

    response_model=DocStatusResult,

    summary="Submit (draft -> submitted)",

)

def submit_allocation(

    allocation_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> DocStatusResult:

    try:

        return _status(_service.submit(db, business_id, allocation_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.post(

    "/{allocation_id}/cancel",

    response_model=DocStatusResult,

    summary="Cancel (submitted -> cancelled)",

)

def cancel_allocation(

    allocation_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> DocStatusResult:

    try:

        return _status(_service.cancel(db, business_id, allocation_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.post(

    "/{allocation_id}/amend",

    response_model=CostCenterAllocationRead,

    status_code=status.HTTP_201_CREATED,

    summary="Amend (cancelled -> new draft)",

)

def amend_allocation(

    allocation_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> CostCenterAllocationRead:

    try:

        return _read(_service.amend(db, business_id, allocation_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc
