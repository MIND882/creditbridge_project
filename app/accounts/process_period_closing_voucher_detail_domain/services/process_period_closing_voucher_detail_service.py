"""Business logic for ProcessPeriodClosingVoucherDetail.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.process_period_closing_voucher_detail_domain.models.process_period_closing_voucher_detail import ProcessPeriodClosingVoucherDetail

from app.accounts.process_period_closing_voucher_detail_domain.repositories.process_period_closing_voucher_detail_repository import (

    ProcessPeriodClosingVoucherDetailRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ProcessPeriodClosingVoucherDetailService"]





class ProcessPeriodClosingVoucherDetailService:

    def __init__(self, repository: Optional[ProcessPeriodClosingVoucherDetailRepository] = None) -> None:

        self.repository = repository or ProcessPeriodClosingVoucherDetailRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProcessPeriodClosingVoucherDetail:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Process Period Closing Voucher Detail", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ProcessPeriodClosingVoucherDetail]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ProcessPeriodClosingVoucherDetail].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
