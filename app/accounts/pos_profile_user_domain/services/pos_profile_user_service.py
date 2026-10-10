"""Business logic for POSProfileUser.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.pos_profile_user_domain.models.pos_profile_user import POSProfileUser

from app.accounts.pos_profile_user_domain.repositories.pos_profile_user_repository import (

    POSProfileUserRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["POSProfileUserService"]





class POSProfileUserService:

    def __init__(self, repository: Optional[POSProfileUserRepository] = None) -> None:

        self.repository = repository or POSProfileUserRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> POSProfileUser:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("POS Profile User", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[POSProfileUser]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[POSProfileUser].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
