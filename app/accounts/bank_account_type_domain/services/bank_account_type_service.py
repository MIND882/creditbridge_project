"""

Business logic for Bank Account Type.



The upstream controller is empty -- ERPNext enforces everything through the

doctype JSON (``reqd=1`` and ``autoname: field:account_type``). Those framework rules

are reimplemented here rather than assumed away: the label is mandatory, and it

is unique per tenant.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.bank_account_type_domain.models.bank_account_type import BankAccountType

from app.accounts.bank_account_type_domain.repositories.bank_account_type_repository import BankAccountTypeRepository

from app.accounts.bank_account_type_domain.schemas.bank_account_type import BankAccountTypeCreate, BankAccountTypeUpdate

from app.core.errors import ConflictError, DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BankAccountTypeService"]





class BankAccountTypeService:

    def __init__(self, repository: Optional[BankAccountTypeRepository] = None) -> None:

        self.repository = repository or BankAccountTypeRepository()



    def _get_or_404(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> BankAccountType:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Bank Account Type", row_id)

        return row



    def _assert_name_free(

        self, db: Session, business_id: uuid.UUID, name: str,

        *, exclude_id: Optional[uuid.UUID] = None,

    ) -> None:

        existing = self.repository.get_by_name(db, business_id, name)

        if existing is not None and existing.id != exclude_id:

            raise ConflictError(

                f"Bank Account Type '{name}' already exists",

                code="bank_account_type_duplicate",

            )



    def get(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> BankAccountType:

        return self._get_or_404(db, business_id, row_id)



    def list(self, db: Session, business_id: uuid.UUID, **filters: object) -> ResultPage[BankAccountType]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[BankAccountType].build(

            rows, total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def create(self, db: Session, business_id: uuid.UUID, payload: BankAccountTypeCreate) -> BankAccountType:

        name = getattr(payload, "account_type")

        if not name or not name.strip():

            raise DomainValidationError(

                "Bank Account Type is mandatory", code="bank_account_type_name_mandatory"

            )

        self._assert_name_free(db, business_id, name)



        row = BankAccountType(business_id=business_id, name=name, **{"account_type": name})

        self.repository.add(db, row)

        db.commit()

        db.refresh(row)

        return row



    def update(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID, payload: BankAccountTypeUpdate) -> BankAccountType:

        row = self._get_or_404(db, business_id, row_id)

        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        new_name = changes.get("account_type")

        if new_name is not None:

            if not new_name.strip():

                raise DomainValidationError(

                    "Bank Account Type is mandatory", code="bank_account_type_name_mandatory"

                )

            self._assert_name_free(db, business_id, new_name, exclude_id=row.id)

            setattr(row, "account_type", new_name)

            row.name = new_name



        db.commit()

        db.refresh(row)

        return row



    def delete(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> None:

        row = self._get_or_404(db, business_id, row_id)

        self.repository.delete(db, row)

        db.commit()
