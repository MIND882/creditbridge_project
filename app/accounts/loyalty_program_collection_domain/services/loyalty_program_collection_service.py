"""Business logic for LoyaltyProgramCollection.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.loyalty_program_collection_domain.models.loyalty_program_collection import LoyaltyProgramCollection

from app.accounts.loyalty_program_collection_domain.repositories.loyalty_program_collection_repository import (

    LoyaltyProgramCollectionRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["LoyaltyProgramCollectionService"]





class LoyaltyProgramCollectionService:

    def __init__(self, repository: Optional[LoyaltyProgramCollectionRepository] = None) -> None:

        self.repository = repository or LoyaltyProgramCollectionRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> LoyaltyProgramCollection:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Loyalty Program Collection", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[LoyaltyProgramCollection]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[LoyaltyProgramCollection].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
