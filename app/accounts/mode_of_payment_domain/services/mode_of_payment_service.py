"""

Business logic for Mode of Payment -- port of

``erpnext/accounts/doctype/mode_of_payment/mode_of_payment.py``.



Upstream hook -> here

-------------------

``autoname`` (``field:mode_of_payment``)  :meth:`create`

``validate``                              :meth:`_validate`

  ``validate_accounts``                     :meth:`_validate_accounts`

  ``validate_repeating_companies``          :meth:`_validate_repeating_companies`

  ``validate_pos_mode_of_payment``          :meth:`_validate_pos_mode_of_payment`



Upstream ``validate_accounts`` compares ``Account.company`` with the row's

``company``. ``Account.company`` collapsed into ``business_id`` in this

conversion, so there is no company string left to compare. What survives is the

intent -- a row may not point at an account that does not belong here -- and

that is enforced by resolving each account and rejecting a missing or foreign

one. The row's ``company`` value is still stored and still checked for

repetition, because that check is about the rows, not about accounts.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.account_domain.models.account import Account

from app.accounts.mode_of_payment_account_domain.models.mode_of_payment_account import (

    ModeOfPaymentAccount,

)

from app.accounts.mode_of_payment_domain.models.mode_of_payment import ModeOfPayment

from app.accounts.mode_of_payment_domain.repositories.mode_of_payment_repository import (

    ModeOfPaymentRepository,

)

from app.accounts.mode_of_payment_domain.schemas.mode_of_payment import (

    ModeOfPaymentCreate,

    ModeOfPaymentUpdate,

)

from app.core.errors import ConflictError, DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ModeOfPaymentService"]





class ModeOfPaymentService:

    def __init__(self, repository: Optional[ModeOfPaymentRepository] = None) -> None:

        self.repository = repository or ModeOfPaymentRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ModeOfPayment:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Mode of Payment", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate_accounts(

        self, db: Session, business_id: uuid.UUID, row: ModeOfPayment

    ) -> None:

        """

        Port of ``validate_accounts``.



        Upstream: ``Account.company`` must equal the row's ``company``. Here the

        account is resolved inside the tenant, so a foreign or missing account

        fails -- the same outcome, reached through tenancy rather than a company

        column that no longer exists.

        """

        for entry in row.accounts:

            if entry.default_account_id is None:

                continue

            account = db.get(Account, entry.default_account_id)

            if account is None or account.business_id != business_id:

                raise DomainValidationError(

                    f"Account {entry.default_account_id} does not match with Company "

                    f"{entry.company} in Mode of Payment: {row.name}",

                    code="mode_of_payment_account_mismatch",

                )



    @staticmethod

    def _validate_repeating_companies(row: ModeOfPayment) -> None:

        """Port of ``validate_repeating_companies`` -- verbatim duplicate check."""

        companies = [entry.company for entry in row.accounts]

        if len(companies) != len(set(companies)):

            raise DomainValidationError(

                "Same Company is entered more than once",

                code="mode_of_payment_repeating_companies",

            )



    @staticmethod

    def _validate_pos_mode_of_payment(row: ModeOfPayment) -> None:

        """

        Port of ``validate_pos_mode_of_payment`` -- **stub, fails open**.



        Upstream refuses to disable a mode of payment that a POS Profile still

        references, reading ``Sales Invoice Payment`` rows whose ``parenttype``

        is ``POS Profile``. Neither doctype is converted yet.



        TODO(POS): once ``pos_profile`` and ``sales_invoice_payment`` land,

        re-implement this as a query for profiles referencing ``row.name`` and

        raise ``DomainValidationError`` with code

        ``mode_of_payment_in_pos_profile`` when disabling.

        """

        return None



    def _validate(

        self, db: Session, business_id: uuid.UUID, row: ModeOfPayment

    ) -> None:

        # Upstream order preserved.

        self._validate_accounts(db, business_id, row)

        self._validate_repeating_companies(row)

        self._validate_pos_mode_of_payment(row)



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ModeOfPayment:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ModeOfPayment]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ModeOfPayment].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_accounts(

        self, business_id: uuid.UUID, row: ModeOfPayment, accounts: list[dict]

    ) -> None:

        row.accounts.clear()

        for idx, item in enumerate(accounts, start=1):

            row.accounts.append(

                ModeOfPaymentAccount(

                    business_id=business_id,

                    idx=idx,

                    company=item.get("company"),

                    default_account_id=item.get("default_account_id"),

                )

            )



    def create(

        self, db: Session, business_id: uuid.UUID, payload: ModeOfPaymentCreate

    ) -> ModeOfPayment:

        name = payload.mode_of_payment.strip()

        if not name:

            raise DomainValidationError(

                "Mode of Payment is mandatory", code="mode_of_payment_name_mandatory"

            )

        if self.repository.get_by_name(db, business_id, name) is not None:

            raise ConflictError(

                f"Mode of Payment '{name}' already exists",

                code="mode_of_payment_duplicate",

            )



        row = ModeOfPayment(

            business_id=business_id,

            name=name,

            mode_of_payment=name,

            type=payload.type,

            # Upstream's Check has no default, which Frappe reads as unchecked.

            # The Create schema defaults it to True; honour whatever arrived.

            enabled=bool(payload.enabled),

        )

        self._replace_accounts(

            business_id, row, [a.model_dump() for a in payload.accounts]

        )



        try:

            db.flush()  # children need ids before validation reads them

            self._validate(db, business_id, row)

            self.repository.add(db, row)

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

        row_id: uuid.UUID,

        payload: ModeOfPaymentUpdate,

    ) -> ModeOfPayment:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "accounts":

                    self._replace_accounts(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

            db.flush()

            self._validate(db, business_id, row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def delete(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> None:

        row = self._get_or_404(db, business_id, row_id)

        self.repository.delete(db, row)

        db.commit()
