"""Business logic for POSInvoiceReference.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.pos_invoice_reference_domain.models.pos_invoice_reference import POSInvoiceReference

from app.accounts.pos_invoice_reference_domain.repositories.pos_invoice_reference_repository import (

    POSInvoiceReferenceRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["POSInvoiceReferenceService"]





class POSInvoiceReferenceService:

    def __init__(self, repository: Optional[POSInvoiceReferenceRepository] = None) -> None:

        self.repository = repository or POSInvoiceReferenceRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> POSInvoiceReference:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("POS Invoice Reference", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[POSInvoiceReference]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[POSInvoiceReference].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
