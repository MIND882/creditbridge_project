"""Read-only service for DunningLetterText; writes go through the parent doctype."""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.dunning_letter_text_domain.models.dunning_letter_text import DunningLetterText

from app.accounts.dunning_letter_text_domain.repositories.dunning_letter_text_repository import DunningLetterTextRepository

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["DunningLetterTextService"]





class DunningLetterTextService:

    def __init__(self, repository: Optional[DunningLetterTextRepository] = None) -> None:

        self.repository = repository or DunningLetterTextRepository()



    def get(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> DunningLetterText:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("DunningLetterText", row_id)

        return row



    def list(self, db: Session, business_id: uuid.UUID, **filters: object) -> ResultPage[DunningLetterText]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[DunningLetterText].build(

            rows, total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
