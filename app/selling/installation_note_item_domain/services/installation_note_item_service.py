"""Business logic for InstallationNoteItem.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.selling.installation_note_item_domain.models.installation_note_item import InstallationNoteItem

from app.selling.installation_note_item_domain.repositories.installation_note_item_repository import (

    InstallationNoteItemRepository,

)

from app.selling.installation_note_item_domain.schemas.installation_note_item import (

    InstallationNoteItemCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["InstallationNoteItemService"]





class InstallationNoteItemService:

    def __init__(self, repository: Optional[InstallationNoteItemRepository] = None) -> None:

        self.repository = repository or InstallationNoteItemRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> InstallationNoteItem:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Installation Note Item", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[InstallationNoteItem]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[InstallationNoteItem].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
