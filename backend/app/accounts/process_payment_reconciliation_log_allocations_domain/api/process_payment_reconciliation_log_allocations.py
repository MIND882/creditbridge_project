"""HTTP surface for Process Payment Reconciliation Log Allocations -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.process_payment_reconciliation_log_allocations_domain.schemas.process_payment_reconciliation_log_allocations import (

    ProcessPaymentReconciliationLogAllocationsListResponse,

    ProcessPaymentReconciliationLogAllocationsRead,

)

from app.accounts.process_payment_reconciliation_log_allocations_domain.services.process_payment_reconciliation_log_allocations_service import ProcessPaymentReconciliationLogAllocationsService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = ProcessPaymentReconciliationLogAllocationsService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=ProcessPaymentReconciliationLogAllocationsListResponse, summary="List process payment reconciliation log allocations rows")

def list_process_payment_reconciliation_log_allocations(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> ProcessPaymentReconciliationLogAllocationsListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return ProcessPaymentReconciliationLogAllocationsListResponse.from_result(

        page, [ProcessPaymentReconciliationLogAllocationsRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=ProcessPaymentReconciliationLogAllocationsRead, summary="Get one process payment reconciliation log allocations row")

def get_process_payment_reconciliation_log_allocations(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> ProcessPaymentReconciliationLogAllocationsRead:

    try:

        return ProcessPaymentReconciliationLogAllocationsRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
