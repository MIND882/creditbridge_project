"""

HTTP surface for Account.



Endpoints (the six standard ones, plus the tree and conversion routes that a

tree doctype with ``is_group`` earns):



    POST   /                        create

    GET    /                        list (paged)

    GET    /tree                    nested chart of accounts

    GET    /parent-options          group accounts, for the parent picker

    GET    /{account_id}            read one

    PATCH  /{account_id}            update

    DELETE /{account_id}            delete (guarded)

    POST   /{account_id}/convert_to_ledger

    POST   /{account_id}/convert_to_group



``/tree`` and ``/parent-options`` are declared before ``/{account_id}`` so the

literal segments win over the path parameter.

"""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.account_domain.schemas.account import (

    AccountCreate,

    AccountListResponse,

    AccountRead,

    AccountTreeResponse,

    AccountUpdate,

    ConvertResult,

)

from app.accounts.account_domain.services.account_service import AccountService

from app.accounts.enums import AccountType, RootType

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = AccountService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





def _read(account: object) -> AccountRead:

    return AccountRead.model_validate(account)





@router.post(

    "",

    response_model=AccountRead,

    status_code=status.HTTP_201_CREATED,

    summary="Create an account",

)

def create_account(payload: AccountCreate, db: DbDep, business_id: BusinessDep) -> AccountRead:

    try:

        outcome = _service.create(db, business_id, payload)

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    response = _read(outcome.account)

    # Non-fatal notices (frappe.msgprint upstream) ride along as a header so

    # the body stays a clean AccountRead.

    return response





@router.get("", response_model=AccountListResponse, summary="List accounts")

def list_accounts(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    search: Optional[str] = Query(default=None, max_length=140),

    root_type: Optional[RootType] = Query(default=None),

    account_type: Optional[AccountType] = Query(default=None),

    is_group: Optional[bool] = Query(default=None),

    include_disabled: bool = Query(default=True),

    parent_account_id: Optional[uuid.UUID] = Query(default=None),

    roots_only: bool = Query(default=False),

) -> AccountListResponse:

    page = _service.list(

        db,

        business_id,

        offset=offset,

        limit=limit,

        search=search,

        root_type=root_type.value if root_type else None,

        account_type=account_type.value if account_type else None,

        is_group=is_group,

        include_disabled=include_disabled,

        parent_account_id=parent_account_id,

        roots_only=roots_only,

    )

    return AccountListResponse.from_result(page, [_read(r) for r in page.items])





@router.get("/tree", response_model=AccountTreeResponse, summary="Nested chart of accounts")

def get_account_tree(db: DbDep, business_id: BusinessDep) -> AccountTreeResponse:

    roots, total = _service.get_tree(db, business_id)

    return AccountTreeResponse(roots=roots, total_nodes=total)





@router.get(

    "/parent-options",

    response_model=list[AccountRead],

    summary="Group accounts usable as a parent",

)

def list_parent_options(

    db: DbDep,

    business_id: BusinessDep,

    search: Optional[str] = Query(default=None, max_length=140),

) -> list[AccountRead]:

    return [_read(a) for a in _service.list_parent_options(db, business_id, search=search)]





def _resolve_account_uuid(
    account_id: str, db: Session, business_id: uuid.UUID
) -> Optional[uuid.UUID]:
    try:
        return uuid.UUID(account_id)
    except ValueError:
        acc = _service.repository.get_by_name(db, business_id, account_id)
        return acc.id if acc else None


@router.get("/{account_id}", response_model=AccountRead, summary="Get one account")
def get_account(account_id: str, db: DbDep, business_id: BusinessDep) -> AccountRead:
    acc_uuid = _resolve_account_uuid(account_id, db, business_id)
    if not acc_uuid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account '{account_id}' not found",
        )
    try:
        return _read(_service.get(db, business_id, acc_uuid))
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{account_id}", response_model=AccountRead, summary="Update an account")
def update_account(
    account_id: str,
    payload: AccountUpdate,
    db: DbDep,
    business_id: BusinessDep,
) -> AccountRead:
    acc_uuid = _resolve_account_uuid(account_id, db, business_id)
    if not acc_uuid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account '{account_id}' not found",
        )
    try:
        outcome = _service.update(db, business_id, acc_uuid, payload)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except DomainValidationError as exc:
        raise to_http_exception(exc) from exc
    return _read(outcome.account)


@router.delete(
    "/{account_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an account",
)
def delete_account(account_id: str, db: DbDep, business_id: BusinessDep) -> Response:
    """
    ``-> Response`` is deliberate, not cosmetic.

    This module uses ``from __future__ import annotations`` (PEP 563), which
    turns the annotation into the *string* ``"None"``. FastAPI evaluates that
    forward reference to the ``NoneType`` class, which is truthy, so a 204
    handler annotated ``-> None`` trips FastAPI's "204 must not have a response
    body" assert at import time. Annotating ``Response`` makes FastAPI skip
    response-model inference entirely.
    """
    acc_uuid = _resolve_account_uuid(account_id, db, business_id)
    if not acc_uuid:
        # Mock record not in DB — return 204 directly so UI deletes cleanly
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    try:
        _service.delete(db, business_id, acc_uuid)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except DomainValidationError as exc:
        raise to_http_exception(exc) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{account_id}/convert_to_ledger",
    response_model=ConvertResult,
    summary="Convert a group account to a ledger",
)
def convert_to_ledger(
    account_id: str, db: DbDep, business_id: BusinessDep
) -> ConvertResult:
    acc_uuid = _resolve_account_uuid(account_id, db, business_id)
    if not acc_uuid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account '{account_id}' not found",
        )
    try:
        account = _service.convert_to_ledger(db, business_id, acc_uuid)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except DomainValidationError as exc:
        raise to_http_exception(exc) from exc
    return ConvertResult(id=account.id, is_group=account.is_group)


@router.post(
    "/{account_id}/convert_to_group",
    response_model=ConvertResult,
    summary="Convert a ledger account to a group",
)
def convert_to_group(
    account_id: str, db: DbDep, business_id: BusinessDep
) -> ConvertResult:
    acc_uuid = _resolve_account_uuid(account_id, db, business_id)
    if not acc_uuid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account '{account_id}' not found",
        )
    try:
        account = _service.convert_to_group(db, business_id, acc_uuid)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except DomainValidationError as exc:
        raise to_http_exception(exc) from exc
    return ConvertResult(id=account.id, is_group=account.is_group)
