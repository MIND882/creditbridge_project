"""

Business logic for Payment Ledger Entry -- port of

``erpnext/accounts/doctype/payment_ledger_entry/payment_ledger_entry.py``.



Upstream hook -> here

-------------------

``validate`` / ``validate_account``      :meth:`_validate_account`

``on_update``                            :meth:`_on_write`

  ``validate_frozen_account``            :meth:`_validate_frozen_account`

  ``validate_account_details``           :meth:`_validate_account_details`

  ``validate_allowed_dimensions``        :meth:`_validate_allowed_dimensions`

  ``validate_balance_type``              :meth:`_validate_balance_type`

  ``update_voucher_outstanding``         :meth:`sync_voucher_outstanding` (stub)



Upstream splits the work between ``validate`` (account type only) and

``on_update`` (everything else), and ``on_update`` skips most of it for a

``delinked`` row. That split is preserved: a row is checked lightly on the way

in, then fully once it is being written, and a delinked row only has to pass the

frozen-account rule.



``validate_dimensions_for_pl_and_bs`` is not ported here for the same reason it

is not ported in GL Entry -- it iterates ``get_checks_for_pl_and_bs_accounts()``

and reads attributes by dynamic name, which has no static equivalent. The

concrete cost-centre case is covered by :meth:`_validate_allowed_dimensions`.

"""



from __future__ import annotations



import uuid

from decimal import Decimal

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.account_domain.models.account import Account

from app.accounts.accounting_dimension_filter_domain.services.accounting_dimension_filter_service import (

    AccountingDimensionFilterService,

    DimensionValueNotAllowedError,

)

from app.accounts.gl_entry_domain.services.gl_entry_service import GLEntryService

from app.accounts.payment_ledger_entry_domain.models.payment_ledger_entry import (

    PLEAccountType,

    PaymentLedgerEntry,

)

from app.accounts.payment_ledger_entry_domain.repositories.payment_ledger_entry_repository import (

    PaymentLedgerEntryRepository,

)

from app.accounts.payment_ledger_entry_domain.schemas.payment_ledger_entry import (

    OutstandingRead,

    PaymentLedgerEntryCreate,

    PaymentLedgerEntryUpdate,

)

from app.core.docstatus import DocStatus, assert_can_cancel, assert_can_submit

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PaymentLedgerEntryService"]



ZERO = Decimal("0")





def _dec(value: object) -> Decimal:

    if value is None or value == "":

        return ZERO

    return Decimal(str(value))





class PaymentLedgerEntryService:

    def __init__(

        self,

        repository: Optional[PaymentLedgerEntryRepository] = None,

        *,

        dimension_filters: Optional[AccountingDimensionFilterService] = None,

        gl_service: Optional[GLEntryService] = None,

    ) -> None:

        self.repository = repository or PaymentLedgerEntryRepository()

        self.dimension_filters = dimension_filters or AccountingDimensionFilterService()

        self.gl = gl_service or GLEntryService()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, entry_id: uuid.UUID

    ) -> PaymentLedgerEntry:

        row = self.repository.get_by_id(db, business_id, entry_id)

        if row is None:

            raise NotFoundError("Payment Ledger Entry", entry_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _account_or_400(self, db: Session, business_id: uuid.UUID, row: PaymentLedgerEntry) -> Account:

        if row.account_id is None:

            raise DomainValidationError(

                "Account is mandatory", code="payment_ledger_entry_account_mandatory"

            )

        account = db.get(Account, row.account_id)

        # Upstream's "{0} account is not of company {1}" -- tenancy is business_id

        # here, so an account belonging to another business simply does not exist.

        if account is None or account.business_id != business_id:

            raise DomainValidationError(

                f"{row.account_id} account is not of company {business_id}",

                code="payment_ledger_entry_account_not_found",

            )

        return account



    def _validate_account(

        self, db: Session, business_id: uuid.UUID, row: PaymentLedgerEntry

    ) -> Account:

        """

        Port of ``validate_account``.



        The account's own type must agree with the row's ``account_type``: a

        Receivable row has to sit on a Receivable account.

        """

        account = self._account_or_400(db, business_id, row)



        if row.account_type is None:

            raise DomainValidationError(

                "Account Type is mandatory", code="payment_ledger_entry_account_type_mandatory"

            )



        if account.account_type is None or account.account_type.value != row.account_type.value:

            raise DomainValidationError(

                f"{account.name} account is not of type {row.account_type.value}",

                code="payment_ledger_entry_account_type_mismatch",

            )

        return account



    @staticmethod

    def _validate_account_details(account: Account, row: PaymentLedgerEntry) -> None:

        """

        Port of ``validate_account_details``: "Account must be ledger, active and

        not freezed". The company check is folded into the tenant-scoped lookup.

        """

        if account.is_group:

            raise DomainValidationError(

                f"{row.voucher_type} {row.voucher_no}: Account {account.name} is a Group "

                f"Account and group accounts cannot be used in transactions",

                code="payment_ledger_entry_account_is_group",

            )

        # Upstream reads `docstatus == 2`; the converted Account models that as

        # the `disabled` flag.

        if account.disabled:

            raise DomainValidationError(

                f"{row.voucher_type} {row.voucher_no}: Account {account.name} is inactive",

                code="payment_ledger_entry_account_inactive",

            )



    @staticmethod

    def _validate_frozen_account(account: Account) -> None:

        """

        Port of ``validate_frozen_account``.



        Upstream lets privileged roles post to a frozen account; that escape

        hatch depends on Frappe's permission system and is not carried over.

        """

        if account.freeze_account is not None and account.freeze_account.value == "Yes":

            raise DomainValidationError(

                f"{account.name} is frozen for entries",

                code="payment_ledger_entry_account_frozen",

            )



    def _validate_allowed_dimensions(

        self, db: Session, business_id: uuid.UUID, row: PaymentLedgerEntry

    ) -> None:

        """

        Port of ``validate_allowed_dimensions``, for the cost-centre dimension.



        Upstream loops every dimension and reads the value by dynamic attribute

        name; cost centre is the one dimension this doctype actually carries.

        """

        if row.cost_center_id is None:

            if self.dimension_filters.is_mandatory_for_account(

                db, business_id, row.account_id, "Cost Center"

            ):

                raise DomainValidationError(

                    f"Cost Center is mandatory for account {row.account_id}",

                    code="payment_ledger_entry_dimension_mandatory",

                )

            return



        try:

            self.dimension_filters.assert_value_allowed(

                db,

                business_id,

                account_id=row.account_id,

                dimension_label="Cost Center",

                dimension_value=str(row.cost_center_id),

            )

        except DimensionValueNotAllowedError as exc:

            raise DomainValidationError(str(exc), code="payment_ledger_entry_dimension_not_allowed")



    def _validate_balance_type(

        self, db: Session, business_id: uuid.UUID, row: PaymentLedgerEntry

    ) -> None:

        """

        Port of ``validate_balance_type``.



        An account that must not go negative cannot end up negative once this row

        lands, so the balance is read *after* the row is flushed.

        """

        account = db.get(Account, row.account_id)

        if account is None or account.balance_must_be is None:

            return



        balance = self.gl.account_balance(db, business_id, row.account_id)

        must_be = account.balance_must_be.value

        if must_be == "Debit" and balance < 0:

            raise DomainValidationError(

                f"{account.name} cannot have a negative balance",

                code="payment_ledger_entry_negative_balance",

            )

        if must_be == "Credit" and balance > 0:

            raise DomainValidationError(

                f"{account.name} cannot have a positive balance",

                code="payment_ledger_entry_negative_balance",

            )



    def _on_write(self, db: Session, business_id: uuid.UUID, row: PaymentLedgerEntry) -> None:

        """

        Port of ``on_update``, minus the outstanding sync.



        A ``delinked`` row is written off, so upstream only checks that the

        account is not frozen and then leaves it alone.

        """

        account = self._account_or_400(db, business_id, row)

        self._validate_frozen_account(account)



        if not row.delinked:

            self._validate_account_details(account, row)

            self._validate_allowed_dimensions(db, business_id, row)

            self._validate_balance_type(db, business_id, row)



    def sync_voucher_outstanding(

        self, db: Session, business_id: uuid.UUID, row: PaymentLedgerEntry

    ) -> None:

        """

        Port of ``update_voucher_outstanding`` -- STUB.



        TODO(accounts-conversion): upstream recomputes and writes

        ``outstanding_amount`` back onto the Sales/Purchase Invoice named by

        ``against_voucher_no``. Those doctypes are not converted, so nothing is

        written back. The outstanding is still answerable on demand through

        :meth:`outstanding`, which sums the open rows -- so reads are correct,

        only the denormalised copy on the invoice is missing.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(self, db: Session, business_id: uuid.UUID, entry_id: uuid.UUID) -> PaymentLedgerEntry:

        return self._get_or_404(db, business_id, entry_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PaymentLedgerEntry]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PaymentLedgerEntry].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def outstanding(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        account_id: Optional[uuid.UUID] = None,

        party_type: Optional[str] = None,

        party: Optional[str] = None,

        against_voucher_no: Optional[str] = None,

    ) -> OutstandingRead:

        """

        The running balance this doctype exists to answer.



        Both figures come from the same open rows; ``invoice_outstanding`` just

        narrows to one document.

        """

        invoice = self.repository.invoice_outstanding(

            db,

            business_id,

            account_id=account_id,

            party_type=party_type,

            party=party,

            against_voucher_no=against_voucher_no,

        )

        party_total = self.repository.party_outstanding(

            db, business_id, account_id=account_id, party_type=party_type, party=party

        )

        return OutstandingRead(

            party_type=party_type,

            party=party,

            against_voucher_no=against_voucher_no,

            invoice_outstanding=invoice,

            party_outstanding=party_total,

        )



    def create(

        self, db: Session, business_id: uuid.UUID, payload: PaymentLedgerEntryCreate

    ) -> PaymentLedgerEntry:

        row = PaymentLedgerEntry(

            business_id=business_id,

            name=self.repository.next_name(db, business_id),

            posting_date=payload.posting_date,

            account_type=payload.account_type,

            account_id=payload.account_id,

            party_type=payload.party_type,

            party=payload.party,

            voucher_type=payload.voucher_type,

            voucher_no=payload.voucher_no,

            against_voucher_type=payload.against_voucher_type,

            against_voucher_no=payload.against_voucher_no,

            amount=payload.amount,

            account_currency=payload.account_currency,

            amount_in_account_currency=payload.amount_in_account_currency,

            cost_center_id=payload.cost_center_id,

            finance_book_id=payload.finance_book_id,

            project=payload.project,

            due_date=payload.due_date,

            voucher_detail_no=payload.voucher_detail_no,

            remarks=payload.remarks,

            # Rows arrive submitted: a ledger row only means something once the

            # voucher behind it is final.

            docstatus=DocStatus.SUBMITTED.value,

        )



        try:

            account = self._validate_account(db, business_id, row)

            self._validate_frozen_account(account)

            db.flush()

            self._on_write(db, business_id, row)

            self.repository.add(db, row)

            self.sync_voucher_outstanding(db, business_id, row)

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

        entry_id: uuid.UUID,

        payload: PaymentLedgerEntryUpdate,

    ) -> PaymentLedgerEntry:

        """

        Only ``delinked`` moves after a row is written.



        Upstream writes rows off by flipping this flag, which drops them out of

        every outstanding read.

        """

        row = self._get_or_404(db, business_id, entry_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                setattr(row, field_name, value)

            db.flush()

            self._on_write(db, business_id, row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def delete(self, db: Session, business_id: uuid.UUID, entry_id: uuid.UUID) -> None:

        row = self._get_or_404(db, business_id, entry_id)

        if not row.is_draft:

            raise DomainValidationError(

                "Only a draft Payment Ledger Entry can be deleted. Cancel it first.",

                code="payment_ledger_entry_not_deletable",

            )

        self.repository.delete(db, row)

        db.commit()



    # ── lifecycle ────────────────────────────────────────────────────────────

    def submit(self, db: Session, business_id: uuid.UUID, entry_id: uuid.UUID) -> PaymentLedgerEntry:

        row = self._get_or_404(db, business_id, entry_id)

        assert_can_submit(row, "Payment Ledger Entry")



        try:

            account = self._validate_account(db, business_id, row)

            self._validate_frozen_account(account)

            self._on_write(db, business_id, row)

            row.docstatus = DocStatus.SUBMITTED.value

            self.sync_voucher_outstanding(db, business_id, row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def cancel(self, db: Session, business_id: uuid.UUID, entry_id: uuid.UUID) -> PaymentLedgerEntry:

        """Cancelling drops the row out of every outstanding read."""

        row = self._get_or_404(db, business_id, entry_id)

        assert_can_cancel(row, "Payment Ledger Entry")



        try:

            row.docstatus = DocStatus.CANCELLED.value

            self.sync_voucher_outstanding(db, business_id, row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row
