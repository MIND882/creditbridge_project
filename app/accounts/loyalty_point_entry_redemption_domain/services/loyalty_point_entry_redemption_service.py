"""Business logic for LoyaltyPointEntryRedemption.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.loyalty_point_entry_redemption_domain.models.loyalty_point_entry_redemption import LoyaltyPointEntryRedemption

from app.accounts.loyalty_point_entry_redemption_domain.repositories.loyalty_point_entry_redemption_repository import (

    LoyaltyPointEntryRedemptionRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["LoyaltyPointEntryRedemptionService"]





class LoyaltyPointEntryRedemptionService:

    def __init__(self, repository: Optional[LoyaltyPointEntryRedemptionRepository] = None) -> None:

        self.repository = repository or LoyaltyPointEntryRedemptionRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> LoyaltyPointEntryRedemption:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Loyalty Point Entry Redemption", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[LoyaltyPointEntryRedemption]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[LoyaltyPointEntryRedemption].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
