"""

Business logic for Bank Account -- port of

``erpnext/accounts/doctype/bank_account/bank_account.py``.



Upstream hook -> here

-------------------

``autoname`` (account_name - bank)   :meth:`_build_name`

``validate``                         :meth:`_validate` (same order)

``validate_is_company_account``      :meth:`_validate_is_company_account`

``validate_account``                 :meth:`_validate_gl_account_unique`

``update_default_bank_account``      ``repository.clear_other_defaults``

``on_trash``                         :meth:`delete`



``onload`` / the ``delete_contact_and_address`` half of ``on_trash`` are

omitted: they drive Frappe's generic Address/Contact linkage, which is not part

of this conversion.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.bank_account_balance_domain.models.bank_account_balance import (

    BankAccountBalance,

)

from app.accounts.bank_account_domain.models.bank_account import BankAccount

from app.accounts.bank_account_domain.repositories.bank_account_repository import (

    BankAccountRepository,

)

from app.accounts.bank_account_domain.schemas.bank_account import (

    BankAccountCreate,

    BankAccountUpdate,

)

from app.core.errors import ConflictError, DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BankAccountService"]





class BankAccountService:

    def __init__(self, repository: Optional[BankAccountRepository] = None) -> None:

        self.repository = repository or BankAccountRepository()



    # ── helpers ──────────────────────────────────────────────────────────────

    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, bank_account_id: uuid.UUID

    ) -> BankAccount:

        row = self.repository.get_by_id(db, business_id, bank_account_id)

        if row is None:

            raise NotFoundError("Bank Account", bank_account_id)

        return row



    def _build_name(self, db: Session, business_id: uuid.UUID, account_name: str, bank_id: uuid.UUID) -> str:

        """

        Port of ``autoname``: ``account_name + " - " + bank``.



        The bank's name is resolved through the repository rather than passed

        in, so the label cannot drift from the linked row.

        """

        from app.accounts.bank_domain.repositories.bank_repository import BankRepository



        bank = BankRepository().get_by_id(db, business_id, bank_id)

        bank_label = bank.bank_name if bank else str(bank_id)

        return f"{account_name.strip()} - {bank_label}"



    def _assert_bank_exists(self, db: Session, business_id: uuid.UUID, bank_id: uuid.UUID) -> None:

        from app.accounts.bank_domain.repositories.bank_repository import BankRepository



        if BankRepository().get_by_id(db, business_id, bank_id) is None:

            raise DomainValidationError(

                f"Bank {bank_id} does not exist", code="bank_not_found"

            )



    def _assert_account_exists(

        self, db: Session, business_id: uuid.UUID, account_id: uuid.UUID

    ) -> None:

        from app.accounts.account_domain.repositories.account_repository import AccountRepository



        if AccountRepository().get_by_id(db, business_id, account_id) is None:

            raise DomainValidationError(

                f"Account {account_id} does not exist", code="account_not_found"

            )



    # ── ported validators ────────────────────────────────────────────────────

    def _validate_is_company_account(

        self, db: Session, business_id: uuid.UUID, row: BankAccount

    ) -> None:

        """

        Port of ``validate_is_company_account``.



        Three checks in upstream order: company mandatory, GL account

        mandatory, then the GL account must be free. ``company`` is the tenant

        here, so it is always present by construction -- the check is kept so

        the rule stays visible if a Company doctype is added later.

        """

        if not row.is_company_account:

            return



        if not row.account_id:

            raise DomainValidationError(

                "Company Account is mandatory", code="bank_account_gl_mandatory"

            )

        self._validate_gl_account_unique(db, business_id, row)



    def _validate_gl_account_unique(

        self, db: Session, business_id: uuid.UUID, row: BankAccount

    ) -> None:

        """

        Port of ``validate_account``.



        One GL account may back only one bank account; otherwise postings would

        be ambiguous about which bank they cleared against.

        """

        if row.account_id is None:

            return



        clashes = self.repository.find_by_gl_account(

            db, business_id, row.account_id, exclude_id=row.id

        )

        if clashes:

            names = ", ".join(c.account_name for c in clashes)

            raise ConflictError(

                f"'{row.account_id}' account is already used by {names}. Use another account.",

                code="bank_account_gl_in_use",

            )



    def _update_default(self, db: Session, business_id: uuid.UUID, row: BankAccount) -> None:

        """Port of ``update_default_bank_account`` -- at most one default per scope."""

        if row.is_default and not row.disabled:

            self.repository.clear_other_defaults(

                db,

                business_id,

                party_type=row.party_type,

                party=row.party,

                is_company_account=row.is_company_account,

                exclude_id=row.id,

            )



    def _validate(

        self, db: Session, business_id: uuid.UUID, row: BankAccount

    ) -> None:

        """Port of ``validate``, preserving upstream call order."""

        self._validate_is_company_account(db, business_id, row)

        self._update_default(db, business_id, row)



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, bank_account_id: uuid.UUID

    ) -> BankAccount:

        return self._get_or_404(db, business_id, bank_account_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[BankAccount]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[BankAccount].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def get_default_for_party(

        self, db: Session, business_id: uuid.UUID, party_type: str, party: str

    ) -> Optional[BankAccount]:

        """Port of the module-level ``get_party_bank_account`` helper."""

        return self.repository.get_default_for_party(db, business_id, party_type, party)



    def create(

        self, db: Session, business_id: uuid.UUID, payload: BankAccountCreate

    ) -> BankAccount:

        self._assert_bank_exists(db, business_id, payload.bank_id)

        if payload.account_id is not None:

            self._assert_account_exists(db, business_id, payload.account_id)



        row = BankAccount(

            business_id=business_id,

            name=self._build_name(db, business_id, payload.account_name, payload.bank_id),

            account_name=payload.account_name,

            bank_id=payload.bank_id,

            account_id=payload.account_id,

            account_type=payload.account_type,

            account_subtype=payload.account_subtype,

            is_default=payload.is_default,

            is_company_account=payload.is_company_account,

            is_credit_card=payload.is_credit_card,

            disabled=payload.disabled,

            party_type=payload.party_type,

            party=payload.party,

            iban=payload.iban,

            bank_account_no=payload.bank_account_no,

            mask=payload.mask,

            branch_code=payload.branch_code,

        )

        for idx, bal in enumerate(payload.balances, start=1):

            row.balances.append(

                BankAccountBalance(

                    business_id=business_id,

                    idx=idx,

                    date=bal.date,

                    balance=bal.balance,

                    currency=bal.currency,

                )

            )



        try:

            self.repository.add(db, row)

            self._validate(db, business_id, row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def update(

        self,

        db: Session,

        business_id: uuid.UUID,

        bank_account_id: uuid.UUID,

        payload: BankAccountUpdate,

    ) -> BankAccount:

        row = self._get_or_404(db, business_id, bank_account_id)

        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            if changes.get("account_id") is not None:

                self._assert_account_exists(db, business_id, changes["account_id"])



            for field_name in (

                "account_name", "account_id", "account_type", "account_subtype",

                "is_default", "is_company_account", "is_credit_card", "disabled",

                "party_type", "party", "iban", "bank_account_no", "mask", "branch_code",

            ):

                if field_name in changes:

                    setattr(row, field_name, changes[field_name])



            if "account_name" in changes:

                row.name = self._build_name(db, business_id, row.account_name, row.bank_id)



            if "balances" in changes:

                row.balances.clear()

                for idx, bal in enumerate(changes["balances"] or [], start=1):

                    row.balances.append(

                        BankAccountBalance(

                            business_id=business_id,

                            idx=idx,

                            date=bal["date"],

                            balance=bal["balance"],

                            currency=bal.get("currency"),

                        )

                    )



            self._validate(db, business_id, row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def delete(self, db: Session, business_id: uuid.UUID, bank_account_id: uuid.UUID) -> None:

        """

        Port of ``on_trash``.



        Upstream also deletes the linked Bank Account Balance rows; here they

        cascade from the ORM relationship, so the delete covers both.

        """

        row = self._get_or_404(db, business_id, bank_account_id)

        self.repository.delete(db, row)

        db.commit()
