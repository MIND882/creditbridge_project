"""Business logic for ClosedDocument.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.closed_document_domain.models.closed_document import ClosedDocument

from app.accounts.closed_document_domain.repositories.closed_document_repository import (

    ClosedDocumentRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ClosedDocumentService"]





class ClosedDocumentService:

    def __init__(self, repository: Optional[ClosedDocumentRepository] = None) -> None:

        self.repository = repository or ClosedDocumentRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ClosedDocument:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Closed Document", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ClosedDocument]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ClosedDocument].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
