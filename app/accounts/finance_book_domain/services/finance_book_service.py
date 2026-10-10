"""

Business logic for Finance Book.



The upstream controller is empty -- ERPNext enforces everything through the

doctype JSON (``reqd=1`` and ``autoname: field:finance_book_name``). Those framework rules

are reimplemented here rather than assumed away: the label is mandatory, and it

is unique per tenant.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.finance_book_domain.models.finance_book import FinanceBook

from app.accounts.finance_book_domain.repositories.finance_book_repository import FinanceBookRepository

from app.accounts.finance_book_domain.schemas.finance_book import FinanceBookCreate, FinanceBookUpdate

from app.core.errors import ConflictError, DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["FinanceBookService"]





class FinanceBookService:

    def __init__(self, repository: Optional[FinanceBookRepository] = None) -> None:

        self.repository = repository or FinanceBookRepository()



    def _get_or_404(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> FinanceBook:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Finance Book", row_id)

        return row



    def _assert_name_free(

        self, db: Session, business_id: uuid.UUID, name: str,

        *, exclude_id: Optional[uuid.UUID] = None,

    ) -> None:

        existing = self.repository.get_by_name(db, business_id, name)

        if existing is not None and existing.id != exclude_id:

            raise ConflictError(

                f"Finance Book '{name}' already exists",

                code="finance_book_duplicate",

            )



    def get(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> FinanceBook:

        return self._get_or_404(db, business_id, row_id)



    def list(self, db: Session, business_id: uuid.UUID, **filters: object) -> ResultPage[FinanceBook]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[FinanceBook].build(

            rows, total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def create(self, db: Session, business_id: uuid.UUID, payload: FinanceBookCreate) -> FinanceBook:

        name = getattr(payload, "finance_book_name")

        if not name or not name.strip():

            raise DomainValidationError(

                "Finance Book is mandatory", code="finance_book_name_mandatory"

            )

        self._assert_name_free(db, business_id, name)



        row = FinanceBook(business_id=business_id, name=name, **{"finance_book_name": name})

        self.repository.add(db, row)

        db.commit()

        db.refresh(row)

        return row



    def update(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID, payload: FinanceBookUpdate) -> FinanceBook:

        row = self._get_or_404(db, business_id, row_id)

        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        new_name = changes.get("finance_book_name")

        if new_name is not None:

            if not new_name.strip():

                raise DomainValidationError(

                    "Finance Book is mandatory", code="finance_book_name_mandatory"

                )

            self._assert_name_free(db, business_id, new_name, exclude_id=row.id)

            setattr(row, "finance_book_name", new_name)

            row.name = new_name



        db.commit()

        db.refresh(row)

        return row



    def delete(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> None:

        row = self._get_or_404(db, business_id, row_id)

        self.repository.delete(db, row)

        db.commit()
