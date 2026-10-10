"""

Business logic for Bank Transaction -- port of

``erpnext/accounts/doctype/bank_transaction/bank_transaction.py``.



Upstream hook -> here

-------------------

``naming_series``            :meth:`BankTransactionRepository.next_name`

``before_validate``          :meth:`_before_validate`

``validate``                 :meth:`_validate`

``validate_included_fee``    :meth:`_validate_included_fee`

``validate_duplicate_references``  :meth:`_validate_duplicate_references`

``validate_currency``        :meth:`_validate_currency`

``handle_excluded_fee``      :meth:`_handle_excluded_fee`

``update_allocated_amount``  :meth:`_update_allocated_amount`

``set_status``               :meth:`_set_status`

``before_submit``            :meth:`submit`

``on_cancel``                :meth:`cancel`



Hook ordering matters and is preserved: ``before_validate`` runs first, so

``_handle_excluded_fee`` folds ``excluded_fee`` into

``deposit``/``withdrawal``/``included_fee`` *before* ``_validate_included_fee``

tests the fee against the withdrawal. Reversing them would change which value

the guard sees.



TODO(accounts-conversion): ``allocate_payment_entries``,

``delink_payment_entry`` and ``clear_linked_payment_entry`` write to Payment

Entry and GL Entry. Neither doctype is converted yet, so

:meth:`sync_linked_payment_entries` is a fail-open no-op -- reconciliation

allocations are stored on the child table but the linked vouchers are not

touched.

"""



from __future__ import annotations



import uuid

from datetime import date

from decimal import Decimal

from typing import Optional



from sqlalchemy import select

from sqlalchemy.orm import Session



from app.accounts.bank_transaction_domain.models.bank_transaction import (

    BankTransaction,

    BankTransactionStatus,

)

from app.accounts.bank_transaction_domain.repositories.bank_transaction_repository import (

    BankTransactionRepository,

)

from app.accounts.bank_transaction_domain.schemas.bank_transaction import (

    BankTransactionCreate,

    BankTransactionUpdate,

)

from app.accounts.bank_transaction_payments_domain.models.bank_transaction_payments import (

    BankTransactionPayment,

)

from app.core.docstatus import DocStatus, assert_can_cancel, assert_can_submit

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BankTransactionService"]



ZERO = Decimal("0")





def _dec(value: object) -> Decimal:

    """``flt()`` equivalent: None/blank behaves as zero."""

    if value is None or value == "":

        return ZERO

    return Decimal(str(value))





class BankTransactionService:

    def __init__(self, repository: Optional[BankTransactionRepository] = None) -> None:

        self.repository = repository or BankTransactionRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, transaction_id: uuid.UUID

    ) -> BankTransaction:

        row = self.repository.get_by_id(db, business_id, transaction_id)

        if row is None:

            raise NotFoundError("Bank Transaction", transaction_id)

        return row



    # ── ported hooks ─────────────────────────────────────────────────────────

    @staticmethod

    def _handle_excluded_fee(row: BankTransaction) -> None:

        """

        Port of ``handle_excluded_fee``.



        The excluded fee is folded into the transaction so every later step sees

        one shape: the fee is added to ``included_fee``, and either subtracted

        from the deposit or added to the withdrawal. ``excluded_fee`` is then

        zeroed.

        """

        excluded_fee = _dec(row.excluded_fee)

        if excluded_fee <= 0:

            return



        deposit = _dec(row.deposit)

        withdrawal = _dec(row.withdrawal)



        # A fee larger than the deposit would flip it into a withdrawal.

        if deposit > 0 and (deposit - excluded_fee) < 0:

            raise DomainValidationError(

                "The Excluded Fee is bigger than the Deposit it is deducted from.",

                code="bank_transaction_excluded_fee_too_large",

            )



        # Directionality: the fee cannot be applied to both sides at once.

        if deposit > 0 and withdrawal > 0:

            raise DomainValidationError(

                "Only one of Deposit or Withdrawal should be non-zero when applying "

                "an Excluded Fee.",

                code="bank_transaction_excluded_fee_ambiguous",

            )



        if deposit > 0:

            row.deposit = deposit - excluded_fee

        elif withdrawal >= 0:

            # Includes the both-zero case: a fee on nothing becomes a withdrawal.

            row.withdrawal = withdrawal + excluded_fee



        row.included_fee = _dec(row.included_fee) + excluded_fee

        row.excluded_fee = ZERO



    @staticmethod

    def _update_allocated_amount(row: BankTransaction) -> None:

        """Port of ``update_allocated_amount``."""

        allocated = sum(

            (_dec(p.allocated_amount) for p in row.payment_entries), ZERO

        )

        row.allocated_amount = allocated

        row.unallocated_amount = abs(_dec(row.withdrawal) - _dec(row.deposit)) - allocated



    @staticmethod

    def _validate_included_fee(row: BankTransaction) -> None:

        """

        Port of ``validate_included_fee``.



        Only withdrawals are guarded: an included fee on a deposit is not

        credited to the account, so it sits outside the deposit value and may

        legitimately exceed it.

        """

        included_fee = _dec(row.included_fee)

        withdrawal = _dec(row.withdrawal)

        if included_fee and withdrawal and included_fee > withdrawal:

            raise DomainValidationError(

                "Included fee is bigger than the withdrawal itself.",

                code="bank_transaction_included_fee_too_large",

            )



    @staticmethod

    def _validate_duplicate_references(row: BankTransaction) -> None:

        """Port of ``validate_duplicate_references``: no voucher allocated twice."""

        seen: set[tuple[Optional[str], Optional[str]]] = set()

        for child in row.payment_entries:

            reference = (child.payment_document, child.payment_entry)

            if reference in seen:

                raise DomainValidationError(

                    f"{child.payment_document} {child.payment_entry} is allocated twice "

                    f"in this Bank Transaction",

                    code="bank_transaction_duplicate_reference",

                )

            seen.add(reference)



    def _validate_currency(self, db: Session, business_id: uuid.UUID, row: BankTransaction) -> None:

        """

        Port of ``validate_currency``.



        A transaction must be in the same currency as the GL account behind its

        bank account. Skipped when either side is unknown, exactly as upstream's

        walrus guard skips when the bank account has no account set.

        """

        if not row.currency or row.bank_account_id is None:

            return



        from app.accounts.account_domain.models.account import Account

        from app.accounts.bank_account_domain.models.bank_account import BankAccount



        bank_account = db.scalar(

            select(BankAccount).where(

                BankAccount.business_id == business_id,

                BankAccount.id == row.bank_account_id,

            )

        )

        if bank_account is None or bank_account.account_id is None:

            return



        account_currency = db.scalar(

            select(Account.account_currency).where(

                Account.business_id == business_id, Account.id == bank_account.account_id

            )

        )

        if account_currency and row.currency != account_currency:

            raise DomainValidationError(

                f"Transaction currency: {row.currency} cannot be different from "

                f"Bank Account({bank_account.name}) currency: {account_currency}",

                code="bank_transaction_currency_mismatch",

            )



    def _validate(self, db: Session, business_id: uuid.UUID, row: BankTransaction) -> None:

        self._validate_included_fee(row)

        self._validate_duplicate_references(row)

        self._validate_currency(db, business_id, row)



    def _before_validate(self, row: BankTransaction) -> None:

        """``before_validate``: fee handling, then the derived amounts."""

        self._handle_excluded_fee(row)

        self._update_allocated_amount(row)



    @staticmethod

    def _set_status(row: BankTransaction) -> None:

        """Port of ``set_status``."""

        if row.docstatus == DocStatus.CANCELLED.value:

            row.status = BankTransactionStatus.CANCELLED

        elif row.docstatus == DocStatus.SUBMITTED.value:

            row.status = (

                BankTransactionStatus.UNRECONCILED

                if _dec(row.unallocated_amount) > 0

                else BankTransactionStatus.RECONCILED

            )



    def sync_linked_payment_entries(

        self,

        db: Session,

        business_id: uuid.UUID,

        row: BankTransaction,

        *,

        removed: Optional[list[BankTransactionPayment]] = None,

    ) -> None:

        """

        Port of ``allocate_payment_entries`` / ``delink_payment_entry`` -- STUB.



        TODO(accounts-conversion): upstream sets ``clearance_date``,

        ``reference_no`` and outstanding amounts on each linked Payment Entry /

        Journal Entry, and writes GL Entry rows. Neither Payment Entry nor GL

        Entry is converted yet, so this fails open: the allocation rows are

        stored on the child table and the totals are recomputed, but no voucher

        is updated. Fail-open is deliberate -- refusing to save a reconciliation

        because an unconverted doctype is missing would make the endpoint

        unusable.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, transaction_id: uuid.UUID

    ) -> BankTransaction:

        return self._get_or_404(db, business_id, transaction_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[BankTransaction]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[BankTransaction].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_children(

        self,

        business_id: uuid.UUID,

        row: BankTransaction,

        entries: Optional[list[dict]],

    ) -> None:

        if entries is None:

            return

        row.payment_entries.clear()

        for idx, item in enumerate(entries, start=1):

            row.payment_entries.append(

                BankTransactionPayment(

                    business_id=business_id,

                    idx=idx,

                    payment_document=item["payment_document"],

                    payment_entry=item["payment_entry"],

                    allocated_amount=item["allocated_amount"],

                    clearance_date=item.get("clearance_date"),

                    reconciliation_type=item.get("reconciliation_type") or "Matched",

                )

            )



    def create(

        self, db: Session, business_id: uuid.UUID, payload: BankTransactionCreate

    ) -> BankTransaction:

        row = BankTransaction(

            business_id=business_id,

            name=self.repository.next_name(db, business_id, payload.date or date.today()),

            naming_series=payload.naming_series,

            date=payload.date,

            status=BankTransactionStatus.PENDING,

            bank_account_id=payload.bank_account_id,

            currency=payload.currency,

            deposit=_dec(payload.deposit),

            withdrawal=_dec(payload.withdrawal),

            included_fee=_dec(payload.included_fee),

            excluded_fee=_dec(payload.excluded_fee),

            description=payload.description,

            reference_number=payload.reference_number,

            transaction_id=payload.transaction_id,

            transaction_type=payload.transaction_type,

            party_type=payload.party_type,

            party=payload.party,

            bank_party_name=payload.bank_party_name,

            bank_party_iban=payload.bank_party_iban,

            bank_party_account_number=payload.bank_party_account_number,

            docstatus=DocStatus.DRAFT.value,

        )

        self._replace_children(

            business_id, row, [p.model_dump() for p in payload.payment_entries]

        )



        try:

            self._before_validate(row)

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

        transaction_id: uuid.UUID,

        payload: BankTransactionUpdate,

    ) -> BankTransaction:

        """

        Mirrors ``before_update_after_submit`` as well as the draft path: the

        duplicate-reference and allocated-amount steps re-run, and allocations

        may change after submit.

        """

        row = self._get_or_404(db, business_id, transaction_id)

        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "payment_entries":

                    self._replace_children(business_id, row, value)

                elif field_name in ("deposit", "withdrawal", "included_fee", "excluded_fee"):

                    setattr(row, field_name, _dec(value))

                else:

                    setattr(row, field_name, value)



            self._before_validate(row)

            self._validate(db, business_id, row)

            self._set_status(row)

            self.sync_linked_payment_entries(db, business_id, row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def delete(self, db: Session, business_id: uuid.UUID, transaction_id: uuid.UUID) -> None:

        row = self._get_or_404(db, business_id, transaction_id)

        if not row.is_draft:

            raise DomainValidationError(

                "Only a draft Bank Transaction can be deleted. Cancel it first.",

                code="bank_transaction_not_deletable",

            )

        self.repository.delete(db, row)

        db.commit()



    # ── lifecycle ────────────────────────────────────────────────────────────

    def submit(

        self, db: Session, business_id: uuid.UUID, transaction_id: uuid.UUID

    ) -> BankTransaction:

        """

        Port of ``before_submit``: allocate, then derive the status.



        ``auto_set_party`` (gated on the ``enable_party_matching`` setting) is

        not ported -- it is a party-matching heuristic, not a validation, and

        the settings doctype is not converted.

        """

        row = self._get_or_404(db, business_id, transaction_id)

        assert_can_submit(row, "Bank Transaction")



        try:

            self._update_allocated_amount(row)

            row.docstatus = DocStatus.SUBMITTED.value

            self._set_status(row)

            self.sync_linked_payment_entries(db, business_id, row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, transaction_id: uuid.UUID

    ) -> BankTransaction:

        """Port of ``on_cancel``: delink the vouchers, then set the status."""

        row = self._get_or_404(db, business_id, transaction_id)

        assert_can_cancel(row, "Bank Transaction")



        try:

            removed = list(row.payment_entries)

            row.docstatus = DocStatus.CANCELLED.value

            self._set_status(row)

            self.sync_linked_payment_entries(db, business_id, row, removed=removed)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def discard(

        self, db: Session, business_id: uuid.UUID, transaction_id: uuid.UUID

    ) -> BankTransaction:

        """

        Port of ``on_discard``: an unreconciled transaction can be dropped,

        which marks it Cancelled without going through the submit/cancel pair.

        """

        row = self._get_or_404(db, business_id, transaction_id)

        row.status = BankTransactionStatus.CANCELLED

        db.commit()

        db.refresh(row)

        return row


