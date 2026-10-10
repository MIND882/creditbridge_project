"""Data access for Bank Account. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select, update

from sqlalchemy.orm import Session, selectinload



from app.accounts.bank_account_domain.models.bank_account import BankAccount

from app.core.pagination import normalise_paging



__all__ = ["BankAccountRepository"]





class BankAccountRepository:

    model = BankAccount



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, bank_account_id: uuid.UUID

    ) -> Optional[BankAccount]:

        return db.scalar(

            select(BankAccount)

            .options(selectinload(BankAccount.balances))

            .where(

                BankAccount.business_id == business_id,

                BankAccount.id == bank_account_id,

            )

        )



    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[BankAccount]:

        return db.scalar(

            select(BankAccount)

            .options(selectinload(BankAccount.balances))

            .where(BankAccount.business_id == business_id, BankAccount.name == name)

        )



    def find_by_gl_account(

        self,

        db: Session,

        business_id: uuid.UUID,

        account_id: uuid.UUID,

        *,

        exclude_id: Optional[uuid.UUID] = None,

    ) -> list[BankAccount]:

        """

        Port of ``validate_account``'s lookup.



        Upstream: ``frappe.db.get_all("Bank Account", filters={"account":

        self.account, "name": ["!=", self.name]})`` -- every *other* bank

        account already bound to this GL account.

        """

        conditions = [

            BankAccount.business_id == business_id,

            BankAccount.account_id == account_id,

        ]

        if exclude_id is not None:

            conditions.append(BankAccount.id != exclude_id)

        return list(db.scalars(select(BankAccount).where(*conditions)))



    def clear_other_defaults(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        party_type: Optional[str],

        party: Optional[str],

        is_company_account: bool,

        exclude_id: uuid.UUID,

    ) -> int:

        """

        Port of ``update_default_bank_account``.



        Upstream runs a single ``set_value`` against every row matching the same

        party/company scope with ``is_default = 1`` and ``disabled = 0``, so at

        most one default survives. Same predicate here.

        """

        conditions = [

            BankAccount.business_id == business_id,

            BankAccount.is_company_account.is_(is_company_account),

            BankAccount.is_default.is_(True),

            BankAccount.disabled.is_(False),

            BankAccount.id != exclude_id,

        ]

        # NULL-safe comparison: party_type/party may legitimately be NULL.

        conditions.append(

            BankAccount.party_type.is_(None) if party_type is None

            else BankAccount.party_type == party_type

        )

        conditions.append(

            BankAccount.party.is_(None) if party is None

            else BankAccount.party == party

        )



        result = db.execute(

            update(BankAccount).where(*conditions).values(is_default=False)

        )

        db.flush()

        return int(result.rowcount or 0)



    def get_default_for_party(

        self, db: Session, business_id: uuid.UUID, party_type: str, party: str

    ) -> Optional[BankAccount]:

        """Port of the module-level ``get_party_bank_account``."""

        return db.scalar(

            select(BankAccount).where(

                BankAccount.business_id == business_id,

                BankAccount.party_type == party_type,

                BankAccount.party == party,

                BankAccount.is_default.is_(True),

                BankAccount.disabled.is_(False),

            )

        )



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        search: Optional[str] = None,

        bank_id: Optional[uuid.UUID] = None,

        is_company_account: Optional[bool] = None,

        include_disabled: bool = True,

    ) -> tuple[Sequence[BankAccount], int]:

        offset, limit = normalise_paging(offset, limit)



        conditions = [BankAccount.business_id == business_id]

        if search:

            pattern = f"%{search}%"

            conditions.append(

                BankAccount.account_name.ilike(pattern) | BankAccount.name.ilike(pattern)

            )

        if bank_id is not None:

            conditions.append(BankAccount.bank_id == bank_id)

        if is_company_account is not None:

            conditions.append(BankAccount.is_company_account.is_(is_company_account))

        if not include_disabled:

            conditions.append(BankAccount.disabled.is_(False))



        total = int(

            db.scalar(select(func.count()).select_from(BankAccount).where(*conditions)) or 0

        )

        rows = db.scalars(

            select(BankAccount)

            .options(selectinload(BankAccount.balances))

            .where(*conditions)

            .order_by(BankAccount.account_name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



    def add(self, db: Session, bank_account: BankAccount) -> BankAccount:

        db.add(bank_account)

        db.flush()

        return bank_account



    def delete(self, db: Session, bank_account: BankAccount) -> None:

        db.delete(bank_account)

        db.flush()
