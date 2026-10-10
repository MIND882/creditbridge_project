"""

Business logic for Bank Account Subtype.



The upstream controller is empty -- ERPNext enforces everything through the

doctype JSON (``reqd=1`` and ``autoname: field:account_subtype``). Those framework rules

are reimplemented here rather than assumed away: the label is mandatory, and it

is unique per tenant.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.bank_account_subtype_domain.models.bank_account_subtype import BankAccountSubtype

from app.accounts.bank_account_subtype_domain.repositories.bank_account_subtype_repository import BankAccountSubtypeRepository

from app.accounts.bank_account_subtype_domain.schemas.bank_account_subtype import BankAccountSubtypeCreate, BankAccountSubtypeUpdate

from app.core.errors import ConflictError, DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BankAccountSubtypeService"]





class BankAccountSubtypeService:

    def __init__(self, repository: Optional[BankAccountSubtypeRepository] = None) -> None:

        self.repository = repository or BankAccountSubtypeRepository()



    def _get_or_404(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> BankAccountSubtype:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Bank Account Subtype", row_id)

        return row



    def _assert_name_free(

        self, db: Session, business_id: uuid.UUID, name: str,

        *, exclude_id: Optional[uuid.UUID] = None,

    ) -> None:

        existing = self.repository.get_by_name(db, business_id, name)

        if existing is not None and existing.id != exclude_id:

            raise ConflictError(

                f"Bank Account Subtype '{name}' already exists",

                code="bank_account_subtype_duplicate",

            )



    def get(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> BankAccountSubtype:

        return self._get_or_404(db, business_id, row_id)



    def list(self, db: Session, business_id: uuid.UUID, **filters: object) -> ResultPage[BankAccountSubtype]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[BankAccountSubtype].build(

            rows, total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def create(self, db: Session, business_id: uuid.UUID, payload: BankAccountSubtypeCreate) -> BankAccountSubtype:

        name = getattr(payload, "account_subtype")

        if not name or not name.strip():

            raise DomainValidationError(

                "Bank Account Subtype is mandatory", code="bank_account_subtype_name_mandatory"

            )

        self._assert_name_free(db, business_id, name)



        row = BankAccountSubtype(business_id=business_id, name=name, **{"account_subtype": name})

        self.repository.add(db, row)

        db.commit()

        db.refresh(row)

        return row



    def update(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID, payload: BankAccountSubtypeUpdate) -> BankAccountSubtype:

        row = self._get_or_404(db, business_id, row_id)

        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        new_name = changes.get("account_subtype")

        if new_name is not None:

            if not new_name.strip():

                raise DomainValidationError(

                    "Bank Account Subtype is mandatory", code="bank_account_subtype_name_mandatory"

                )

            self._assert_name_free(db, business_id, new_name, exclude_id=row.id)

            setattr(row, "account_subtype", new_name)

            row.name = new_name



        db.commit()

        db.refresh(row)

        return row



    def delete(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> None:

        row = self._get_or_404(db, business_id, row_id)

        self.repository.delete(db, row)

        db.commit()
