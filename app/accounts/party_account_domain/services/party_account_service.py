"""Read-only service for PartyAccount; writes go through its owner."""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.party_account_domain.models.party_account import PartyAccount

from app.accounts.party_account_domain.repositories.party_account_repository import PartyAccountRepository

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PartyAccountService"]





class PartyAccountService:

    def __init__(self, repository: Optional[PartyAccountRepository] = None) -> None:

        self.repository = repository or PartyAccountRepository()



    def get(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> PartyAccount:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("PartyAccount", row_id)

        return row



    def list(self, db: Session, business_id: uuid.UUID, **filters: object) -> ResultPage[PartyAccount]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PartyAccount].build(

            rows, total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
