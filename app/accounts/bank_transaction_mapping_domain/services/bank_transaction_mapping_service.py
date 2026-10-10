"""

Business logic for Bank Transaction Mapping.



Rows are owned by a Bank, so the write path lives in that service. This one

covers the read side.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.bank_transaction_mapping_domain.repositories.bank_transaction_mapping_repository import BankTransactionMappingRepository

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BankTransactionMappingService"]





class BankTransactionMappingService:

    def __init__(self, repository: Optional[BankTransactionMappingRepository] = None) -> None:

        self.repository = repository or BankTransactionMappingRepository()



    def get(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID):

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Bank Transaction Mapping", row_id)

        return row



    def list_by_parent(self, db: Session, business_id: uuid.UUID, parent_id: uuid.UUID) -> list:

        return self.repository.list_by_parent(db, business_id, parent_id)



    def list(self, db: Session, business_id: uuid.UUID, **filters: object):

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage.build(

            rows, total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
