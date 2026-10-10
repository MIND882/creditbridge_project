"""HTTP surface for Party Link."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.party_link_domain.schemas.party_link import (

        PartyLinkCreate,

    PartyLinkUpdate,

    PartyLinkRead,

    PartyLinkListResponse,

)

from app.accounts.party_link_domain.services.party_link_service import PartyLinkService

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = PartyLinkService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.post(

    "", response_model=PartyLinkRead, status_code=status.HTTP_201_CREATED,

    summary="Create a party link",

)

def create_party_link(

    payload: PartyLinkCreate, db: DbDep, business_id: BusinessDep

) -> PartyLinkRead:

    try:

        return PartyLinkRead.model_validate(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=PartyLinkListResponse, summary="List party links")

def list_party_link(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    search: Optional[str] = Query(default=None, max_length=140),

) -> PartyLinkListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, search=search,

    )

    return PartyLinkListResponse.from_result(

        page, [PartyLinkRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=PartyLinkRead, summary="Get one party link"

)

def get_party_link(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> PartyLinkRead:

    try:

        return PartyLinkRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{row_id}", response_model=PartyLinkRead, summary="Update")

def update_party_link(

    row_id: uuid.UUID, payload: PartyLinkUpdate, db: DbDep, business_id: BusinessDep

) -> PartyLinkRead:

    try:

        return PartyLinkRead.model_validate(

            _service.update(db, business_id, row_id, payload)

        )

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete("/{row_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete")

def delete_party_link(

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
