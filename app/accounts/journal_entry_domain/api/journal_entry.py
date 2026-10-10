"""HTTP surface for Journal Entry. Submittable: /submit and /cancel."""



from __future__ import annotations



import uuid

from datetime import date

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.journal_entry_domain.models.journal_entry import JournalVoucherType

from app.accounts.journal_entry_domain.schemas.journal_entry import (

    JournalEntryCreate,

    JournalEntryListResponse,

    JournalEntryRead,

    JournalEntryStatusResult,

    JournalEntryUpdate,

)

from app.accounts.journal_entry_domain.services.journal_entry_service import JournalEntryService

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = JournalEntryService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





def _read(row: object) -> JournalEntryRead:

    return JournalEntryRead.model_validate(row)





def _status(row: object) -> JournalEntryStatusResult:

    return JournalEntryStatusResult(

        id=row.id,  # type: ignore[attr-defined]

        name=row.name,  # type: ignore[attr-defined]

        docstatus=int(row.docstatus),  # type: ignore[attr-defined]

        total_debit=row.total_debit,  # type: ignore[attr-defined]

        total_credit=row.total_credit,  # type: ignore[attr-defined]

    )





@router.post(

    "",

    response_model=JournalEntryRead,

    status_code=status.HTTP_201_CREATED,

    summary="Create a journal entry (draft)",

)

def create_journal_entry(

    payload: JournalEntryCreate, db: DbDep, business_id: BusinessDep

) -> JournalEntryRead:

    try:

        return _read(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=JournalEntryListResponse, summary="List journal entries")

def list_journal_entries(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    voucher_type: Optional[JournalVoucherType] = Query(default=None),

    from_date: Optional[date] = Query(default=None),

    to_date: Optional[date] = Query(default=None),

    search: Optional[str] = Query(default=None, max_length=140),

    docstatus: Optional[int] = Query(default=None, ge=0, le=2),

    include_cancelled: bool = Query(default=False),

) -> JournalEntryListResponse:

    page = _service.list(

        db,

        business_id,

        offset=offset,

        limit=limit,

        voucher_type=voucher_type.value if voucher_type else None,

        from_date=from_date,

        to_date=to_date,

        search=search,

        docstatus=docstatus,

        include_cancelled=include_cancelled,

    )

    return JournalEntryListResponse.from_result(page, [_read(r) for r in page.items])






def _resolve_journal_entry_uuid(
    entry_id: str, db: Session, business_id: uuid.UUID
) -> Optional[uuid.UUID]:
    try:
        return uuid.UUID(entry_id)
    except ValueError:
        e = _service.repository.get_by_name(db, business_id, entry_id)
        return e.id if e else None


@router.get("/{entry_id}", response_model=JournalEntryRead, summary="Get one journal entry")

def get_journal_entry(entry_id: str, db: DbDep, business_id: BusinessDep) -> JournalEntryRead:

    try:

        uid = _resolve_journal_entry_uuid(entry_id, db, business_id)
        if not uid:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Journal Entry '{entry_id}' not found")
        return _read(_service.get(db, business_id, uid))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{entry_id}", response_model=JournalEntryRead, summary="Update a draft entry")

def update_journal_entry(

    entry_id: str, payload: JournalEntryUpdate, db: DbDep, business_id: BusinessDep

) -> JournalEntryRead:

    try:

        uid = _resolve_journal_entry_uuid(entry_id, db, business_id)
        if not uid:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Journal Entry '{entry_id}' not found")
        return _read(_service.update(db, business_id, uid, payload))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete(

    "/{entry_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a draft entry"

)

def delete_journal_entry(entry_id: str, db: DbDep, business_id: BusinessDep) -> Response:

    # `-> Response` not `-> None`: under PEP 563 the annotation becomes the

    # string "None", which FastAPI resolves to the truthy NoneType class and

    # then rejects for a 204 at import time.

    try:

        uid = _resolve_journal_entry_uuid(entry_id, db, business_id)
        if not uid:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        _service.delete(db, business_id, uid)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)





@router.post(

    "/{entry_id}/submit",

    response_model=JournalEntryStatusResult,

    summary="Submit (draft -> submitted) and post the GL entries",

)

def submit_journal_entry(

    entry_id: str, db: DbDep, business_id: BusinessDep

) -> JournalEntryStatusResult:

    try:

        uid = _resolve_journal_entry_uuid(entry_id, db, business_id)
        if not uid:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Journal Entry '{entry_id}' not found")
        return _status(_service.submit(db, business_id, uid))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.post(

    "/{entry_id}/cancel",

    response_model=JournalEntryStatusResult,

    summary="Cancel (submitted -> cancelled) and reverse the GL entries",

)

def cancel_journal_entry(

    entry_id: str, db: DbDep, business_id: BusinessDep

) -> JournalEntryStatusResult:

    try:

        uid = _resolve_journal_entry_uuid(entry_id, db, business_id)
        if not uid:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Journal Entry '{entry_id}' not found")
        return _status(_service.cancel(db, business_id, uid))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc
