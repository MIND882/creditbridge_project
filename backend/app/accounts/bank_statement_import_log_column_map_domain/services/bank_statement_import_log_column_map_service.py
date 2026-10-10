"""Business logic for BankStatementImportLogColumnMap.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.bank_statement_import_log_column_map_domain.models.bank_statement_import_log_column_map import BankStatementImportLogColumnMap

from app.accounts.bank_statement_import_log_column_map_domain.repositories.bank_statement_import_log_column_map_repository import (

    BankStatementImportLogColumnMapRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BankStatementImportLogColumnMapService"]





class BankStatementImportLogColumnMapService:

    def __init__(self, repository: Optional[BankStatementImportLogColumnMapRepository] = None) -> None:

        self.repository = repository or BankStatementImportLogColumnMapRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> BankStatementImportLogColumnMap:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Bank Statement Import Log Column Map", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[BankStatementImportLogColumnMap]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[BankStatementImportLogColumnMap].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
