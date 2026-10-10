"""

HTTP surface for Account Category.



Wiring only: dependency injection, status codes, response models. Every rule

lives in the service, so the same behaviour is reachable from a CLI importer or

a background job without going through HTTP.



Not a tree doctype (``is_tree`` is absent from account_category.json), so there

is no ``GET /tree`` and no group/ledger conversion endpoints.

"""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.account_category_domain.schemas.account_category import (

    AccountCategoryCreate,

    AccountCategoryListResponse,

    AccountCategoryRead,

    AccountCategoryUpdate,

)

from app.accounts.account_category_domain.services.account_category_service import (

    AccountCategoryService,

)

from app.accounts.enums import RootType

from app.core.errors import to_http_exception, DomainValidationError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = AccountCategoryService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.post(

    "",

    response_model=AccountCategoryRead,

    status_code=status.HTTP_201_CREATED,

    summary="Create an account category",

)

def create_account_category(

    payload: AccountCategoryCreate, db: DbDep, business_id: BusinessDep

) -> AccountCategoryRead:

    try:

        return AccountCategoryRead.model_validate(

            _service.create(db, business_id, payload)

        )

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get(

    "",

    response_model=AccountCategoryListResponse,

    summary="List account categories",

)

def list_account_categories(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    search: Optional[str] = Query(default=None, max_length=140),

    root_type: Optional[RootType] = Query(default=None),

) -> AccountCategoryListResponse:

    page = _service.list(

        db,

        business_id,

        offset=offset,

        limit=limit,

        search=search,

        root_type=root_type,

    )

    return AccountCategoryListResponse.from_result(

        page, [AccountCategoryRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{category_id}",

    response_model=AccountCategoryRead,

    summary="Get one account category",

)

def get_account_category(

    category_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> AccountCategoryRead:

    from app.core.errors import NotFoundError



    try:

        return AccountCategoryRead.model_validate(_service.get(db, business_id, category_id))

    except NotFoundError as exc:

        from fastapi import HTTPException



        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch(

    "/{category_id}",

    response_model=AccountCategoryRead,

    summary="Update an account category",

)

def update_account_category(

    category_id: uuid.UUID,

    payload: AccountCategoryUpdate,

    db: DbDep,

    business_id: BusinessDep,

) -> AccountCategoryRead:

    from app.core.errors import NotFoundError



    try:

        return AccountCategoryRead.model_validate(

            _service.update(db, business_id, category_id, payload)

        )

    except NotFoundError as exc:

        from fastapi import HTTPException



        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete(

    "/{category_id}",

    status_code=status.HTTP_204_NO_CONTENT,

    summary="Delete an account category",

)

def delete_account_category(

    category_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> Response:

    # `-> Response` not `-> None`: under PEP 563 the annotation becomes the

    # string "None", which FastAPI resolves to the truthy NoneType class and

    # then rejects for a 204 at import time. See the note on delete_account.

    from fastapi import HTTPException



    from app.core.errors import NotFoundError



    try:

        _service.delete(db, business_id, category_id)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
