"""HTTP surface for Bank Transaction Rule."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.bank_transaction_rule_domain.schemas.bank_transaction_rule import (

    BankTransactionRuleCreate,

    BankTransactionRuleListResponse,

    BankTransactionRuleRead,

    BankTransactionRuleUpdate,

)

from app.accounts.bank_transaction_rule_domain.services.bank_transaction_rule_service import (

    BankTransactionRuleService,

)

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = BankTransactionRuleService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





def _read(row: object) -> BankTransactionRuleRead:

    return BankTransactionRuleRead.model_validate(row)





@router.post(

    "",

    response_model=BankTransactionRuleRead,

    status_code=status.HTTP_201_CREATED,

    summary="Create a bank transaction rule",

)

def create_rule(payload: BankTransactionRuleCreate, db: DbDep, business_id: BusinessDep) -> BankTransactionRuleRead:

    try:

        return _read(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=BankTransactionRuleListResponse, summary="List rules")

def list_rules(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    search: Optional[str] = Query(default=None, max_length=140),

) -> BankTransactionRuleListResponse:

    page = _service.list(db, business_id, offset=offset, limit=limit, search=search)

    return BankTransactionRuleListResponse.from_result(page, [_read(r) for r in page.items])





@router.get("/{rule_id}", response_model=BankTransactionRuleRead, summary="Get one rule")

def get_rule(rule_id: uuid.UUID, db: DbDep, business_id: BusinessDep) -> BankTransactionRuleRead:

    try:

        return _read(_service.get(db, business_id, rule_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{rule_id}", response_model=BankTransactionRuleRead, summary="Update a rule")

def update_rule(

    rule_id: uuid.UUID, payload: BankTransactionRuleUpdate, db: DbDep, business_id: BusinessDep

) -> BankTransactionRuleRead:

    try:

        return _read(_service.update(db, business_id, rule_id, payload))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete(

    "/{rule_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a rule"

)

def delete_rule(rule_id: uuid.UUID, db: DbDep, business_id: BusinessDep) -> Response:

    # `-> Response` not `-> None`: under PEP 563 the annotation becomes the

    # string "None", which FastAPI resolves to the truthy NoneType class and

    # then rejects for a 204 at import time.

    try:

        _service.delete(db, business_id, rule_id)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
