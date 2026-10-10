"""

Business logic for Bank.



The upstream controller only manages Frappe's generic Address/Contact links

(``onload`` / ``on_trash``); its uniqueness comes from ``autoname:

field:bank_name``. So the real rules to preserve are: the name is mandatory,

and it is unique per tenant.



Upstream ``on_trash`` deletes linked Bank Account Balance rows. Here the

balances hang off Bank Account, not Bank, and cascade from it -- so nothing

extra is needed, and a Bank with accounts is refused instead of silently

orphaning them.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.bank_domain.models.bank import Bank

from app.accounts.bank_domain.repositories.bank_repository import BankRepository

from app.accounts.bank_domain.schemas.bank import BankCreate, BankUpdate

from app.accounts.bank_transaction_mapping_domain.models.bank_transaction_mapping import (

    BankTransactionMapping,

)

from app.core.errors import ConflictError, DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BankService"]





class BankService:

    def __init__(self, repository: Optional[BankRepository] = None) -> None:

        self.repository = repository or BankRepository()



    def _get_or_404(self, db: Session, business_id: uuid.UUID, bank_id: uuid.UUID) -> Bank:

        bank = self.repository.get_by_id(db, business_id, bank_id)

        if bank is None:

            raise NotFoundError("Bank", bank_id)

        return bank



    def _assert_name_free(

        self,

        db: Session,

        business_id: uuid.UUID,

        bank_name: str,

        *,

        exclude_id: Optional[uuid.UUID] = None,

    ) -> None:

        existing = self.repository.get_by_name(db, business_id, bank_name)

        if existing is not None and existing.id != exclude_id:

            raise ConflictError(

                f"Bank '{bank_name}' already exists",

                code="bank_duplicate",

            )



    @staticmethod

    def _assert_name_present(bank_name: Optional[str]) -> None:

        if not bank_name or not bank_name.strip():

            raise DomainValidationError("Bank Name is mandatory", code="bank_name_mandatory")



    def get(self, db: Session, business_id: uuid.UUID, bank_id: uuid.UUID) -> Bank:

        return self._get_or_404(db, business_id, bank_id)



    def list(self, db: Session, business_id: uuid.UUID, **filters: object) -> ResultPage[Bank]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[Bank].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def create(self, db: Session, business_id: uuid.UUID, payload: BankCreate) -> Bank:

        self._assert_name_present(payload.bank_name)

        self._assert_name_free(db, business_id, payload.bank_name)



        bank = Bank(

            business_id=business_id,

            name=payload.bank_name,

            bank_name=payload.bank_name,

            swift_number=payload.swift_number,

            website=payload.website,

            plaid_access_token=payload.plaid_access_token,

        )

        for idx, row in enumerate(payload.bank_transaction_mapping, start=1):

            bank.bank_transaction_mapping.append(

                BankTransactionMapping(

                    business_id=business_id,

                    idx=idx,

                    bank_transaction_field=row.bank_transaction_field,

                    file_field=row.file_field,

                )

            )



        try:

            self.repository.add(db, bank)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(bank)

        return bank



    def update(

        self, db: Session, business_id: uuid.UUID, bank_id: uuid.UUID, payload: BankUpdate

    ) -> Bank:

        bank = self._get_or_404(db, business_id, bank_id)

        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return bank



        try:

            for field_name in ("bank_name", "swift_number", "website", "plaid_access_token"):

                if field_name in changes:

                    setattr(bank, field_name, changes[field_name])



            if "bank_name" in changes:

                self._assert_name_present(bank.bank_name)

                self._assert_name_free(db, business_id, bank.bank_name, exclude_id=bank.id)

                bank.name = bank.bank_name



            if "bank_transaction_mapping" in changes:

                bank.bank_transaction_mapping.clear()

                for idx, row in enumerate(changes["bank_transaction_mapping"] or [], start=1):

                    bank.bank_transaction_mapping.append(

                        BankTransactionMapping(

                            business_id=business_id,

                            idx=idx,

                            bank_transaction_field=row["bank_transaction_field"],

                            file_field=row["file_field"],

                        )

                    )

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(bank)

        return bank



    def delete(self, db: Session, business_id: uuid.UUID, bank_id: uuid.UUID) -> None:

        bank = self._get_or_404(db, business_id, bank_id)



        from sqlalchemy import func, select



        from app.accounts.bank_account_domain.models.bank_account import BankAccount



        in_use = int(

            db.scalar(

                select(func.count())

                .select_from(BankAccount)

                .where(

                    BankAccount.business_id == business_id,

                    BankAccount.bank_id == bank.id,

                )

            )

            or 0

        )

        if in_use:

            raise DomainValidationError(

                f"Cannot delete Bank '{bank.bank_name}': {in_use} Bank Account(s) still "

                "reference it",

                code="bank_in_use",

                details={"bank_account_count": in_use},

            )



        self.repository.delete(db, bank)

        db.commit()
