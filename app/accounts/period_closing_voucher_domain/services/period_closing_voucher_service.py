# HAND-WRITTEN

"""

Business logic for Period Closing Voucher -- port of

``erpnext/accounts/doctype/period_closing_voucher/period_closing_voucher.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream hooks:

    validate

    validate_accounts_not_frozen

    validate_start_and_end_date

    check_if_previous_year_closed

    block_if_future_closing_voucher_exists

    get_future_closing_voucher

    check_closing_account_type

    check_closing_account_currency

    on_submit

    on_cancel

    cancel_process_pcv_docs

    on_trash

    make_gl_entries

    get_pcv_gl_entries

    get_gle_for_pl_account

    get_gle_for_closing_account

    update_default_dimensions

    get_account_balances_based_on_dimensions

    get_accounting_dimension_fields

    get_gl_entries_for_current_period

    set_account_balance_dict

    get_key

    get_account_closing_balances

    get_closing_entries_for_pl_accounts

    get_closing_entries_for_balance_sheet_accounts

    get_closing_entry

    get_closing_entries_for_closing_account

    is_first_period_closing_voucher

    cancel_gl_entries

    get_gle_count_against_current_pcv



Five of the seven upstream ``frappe.throw`` sites are ported. The two that

are not -- ``check_closing_account_currency`` and ``validate_accounts_not_frozen``

-- need Company.default_currency and an Accounts Settings freeze date that the

converted schemas do not carry; both are named in :meth:`_validate`.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



import datetime as dt



from app.accounts.account_domain.models.account import Account

from app.accounts.fiscal_year_domain.models.fiscal_year import FiscalYear

from app.accounts.gl_entry_domain.models.gl_entry import GLEntry

from app.accounts.period_closing_voucher_domain.models.period_closing_voucher import PeriodClosingVoucher

from app.accounts.period_closing_voucher_domain.repositories.period_closing_voucher_repository import (

    PeriodClosingVoucherRepository,

)

from app.accounts.period_closing_voucher_domain.schemas.period_closing_voucher import (

    PeriodClosingVoucherCreate,

    PeriodClosingVoucherUpdate,

)

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PeriodClosingVoucherService"]





class PeriodClosingVoucherService:

    def __init__(self, repository: Optional[PeriodClosingVoucherRepository] = None) -> None:

        self.repository = repository or PeriodClosingVoucherRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PeriodClosingVoucher:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Period Closing Voucher", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    # ══════════════════════════════════════════════════════════════════════

    # ported validators

    # ══════════════════════════════════════════════════════════════════════

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: PeriodClosingVoucher

    ) -> None:

        """

        Port of upstream ``validate``. Order is preserved because the checks

        depend on each other: ``_validate_start_and_end_date`` loads the fiscal

        year bounds that the later date comparisons rely on.



            validate_start_and_end_date              -> ported

            check_if_previous_year_closed            -> ported

            block_if_future_closing_voucher_exists   -> ported

            check_closing_account_type               -> ported

            check_closing_account_currency           -> NOT ported (see below)

            validate_accounts_not_frozen             -> NOT ported (see below)



        TODO(PORT-VALIDATION): two upstream rules are missing.



          * ``check_closing_account_currency`` compares the closing account's

            currency against ``Company.default_currency``. ``Company`` is not

            converted -- the tenant is ``business_id`` and carries no default

            currency -- so the comparison has nothing to compare against.

          * ``validate_accounts_not_frozen`` calls ``check_freezing_date``

            against the Accounts Settings freeze date. The converted

            ``AccountsSettings`` model does not carry that column.



        Both fail open: a voucher whose closing account is in a foreign

        currency, or which posts before the freeze date, is accepted here.

        """

        self._validate_start_and_end_date(db, business_id, row)

        self._check_if_previous_year_closed(db, business_id, row)

        self._block_if_future_closing_voucher_exists(db, business_id, row)

        self._check_closing_account_type(db, business_id, row)



    # ── validate_start_and_end_date ───────────────────────────────────────

    def _validate_start_and_end_date(

        self, db: Session, business_id: uuid.UUID, row: PeriodClosingVoucher

    ) -> None:

        """

        Periods must tile the fiscal year with no gap and no overlap: the next

        voucher starts the day after the last *submitted* one ended, or at the

        fiscal year start when there is none.

        """

        fy = self._fiscal_year_or_fail(db, business_id, row)



        prev_end = db.scalar(

            select(func.max(PeriodClosingVoucher.period_end_date)).where(

                PeriodClosingVoucher.business_id == business_id,

                PeriodClosingVoucher.fiscal_year_id == row.fiscal_year_id,

                PeriodClosingVoucher.docstatus == DocStatus.SUBMITTED.value,

                PeriodClosingVoucher.id != row.id,

            )

        )

        valid_start = (

            prev_end + dt.timedelta(days=1) if prev_end else fy.year_start_date

        )



        if row.period_start_date != valid_start:

            raise DomainValidationError(

                f"Period Start Date must be {valid_start.isoformat()}",

                code="period_closing_voucher_bad_start_date",

                details={

                    "period_start_date": row.period_start_date.isoformat(),

                    "expected": valid_start.isoformat(),

                },

            )



        if row.period_start_date > row.period_end_date:

            raise DomainValidationError(

                "Period Start Date cannot be greater than Period End Date",

                code="period_closing_voucher_start_after_end",

                details={

                    "period_start_date": row.period_start_date.isoformat(),

                    "period_end_date": row.period_end_date.isoformat(),

                },

            )



        if row.period_end_date > fy.year_end_date:

            raise DomainValidationError(

                "Period End Date cannot be greater than Fiscal Year End Date",

                code="period_closing_voucher_end_after_fiscal_year",

                details={

                    "period_end_date": row.period_end_date.isoformat(),

                    "fiscal_year_end": fy.year_end_date.isoformat(),

                },

            )



    # ── check_if_previous_year_closed ─────────────────────────────────────

    def _check_if_previous_year_closed(

        self, db: Session, business_id: uuid.UUID, row: PeriodClosingVoucher

    ) -> None:

        """

        If the year before this fiscal year has posted GL activity and was never

        closed, this voucher is blocked -- otherwise those balances would be

        carried silently and the ledger would not reconcile.



        A previous year with no GL activity is skipped, matching upstream's

        early return.

        """

        fy = self._fiscal_year_or_fail(db, business_id, row)

        last_year_closing = fy.year_start_date - dt.timedelta(days=1)



        prev_fy = db.scalar(

            select(FiscalYear).where(

                FiscalYear.business_id == business_id,

                FiscalYear.year_start_date <= last_year_closing,

                FiscalYear.year_end_date >= last_year_closing,

                FiscalYear.disabled.is_(False),

            )

        )

        if prev_fy is None:

            return



        already_closed = db.scalar(

            select(PeriodClosingVoucher.id).where(

                PeriodClosingVoucher.business_id == business_id,

                PeriodClosingVoucher.docstatus == DocStatus.SUBMITTED.value,

                PeriodClosingVoucher.period_end_date >= prev_fy.year_start_date,

                PeriodClosingVoucher.period_end_date <= last_year_closing,

            )

        )

        if already_closed is not None:

            return



        gle_exists = db.scalar(

            select(GLEntry.id).where(

                GLEntry.business_id == business_id,

                GLEntry.posting_date >= prev_fy.year_start_date,

                GLEntry.posting_date <= last_year_closing,

                GLEntry.is_cancelled.is_(False),

            )

        )

        if gle_exists is None:

            return



        raise DomainValidationError(

            "Previous Year is not closed, please close it first",

            code="period_closing_voucher_previous_year_not_closed",

            details={"previous_fiscal_year": prev_fy.year},

        )



    # ── block_if_future_closing_voucher_exists ────────────────────────────

    def _block_if_future_closing_voucher_exists(

        self, db: Session, business_id: uuid.UUID, row: PeriodClosingVoucher

    ) -> None:

        """

        A submitted voucher for a *later* period blocks this one, since closing

        out of order would leave the later close based on stale balances.

        """

        future = db.scalar(

            select(PeriodClosingVoucher.name).where(

                PeriodClosingVoucher.business_id == business_id,

                PeriodClosingVoucher.docstatus == DocStatus.SUBMITTED.value,

                PeriodClosingVoucher.period_end_date > row.period_end_date,

                PeriodClosingVoucher.id != row.id,

            )

        )

        if future is not None:

            action = "cancel" if row.docstatus == DocStatus.CANCELLED.value else "create"

            raise DomainValidationError(

                f"You cannot {action} this document because another Period "

                f"Closing Entry {future} exists after {row.period_end_date.isoformat()}",

                code="period_closing_voucher_future_voucher_exists",

                details={"future_voucher": future},

            )



    # ── check_closing_account_type ────────────────────────────────────────

    def _check_closing_account_type(

        self, db: Session, business_id: uuid.UUID, row: PeriodClosingVoucher

    ) -> None:

        """

        The closing head receives every P&L balance, so it must sit on the

        balance sheet. A tenant-scoped lookup also rejects an account owned

        elsewhere, which upstream would not even resolve.

        """

        account = db.scalar(

            select(Account).where(

                Account.id == row.closing_account_head_id,

                Account.business_id == business_id,

            )

        )

        root_type = getattr(

            account.root_type if account else None, "value",

            account.root_type if account else None,

        )

        if root_type not in ("Liability", "Equity"):

            label = account.name if account else str(row.closing_account_head_id)

            raise DomainValidationError(

                f"Closing Account {label} must be of type Liability / Equity",

                code="period_closing_voucher_bad_closing_account_type",

                details={"closing_account_head": label, "root_type": str(root_type)},

            )



    # ── lookups ───────────────────────────────────────────────────────────

    def _fiscal_year_or_fail(

        self, db: Session, business_id: uuid.UUID, row: PeriodClosingVoucher

    ) -> FiscalYear:

        fy = db.scalar(

            select(FiscalYear).where(

                FiscalYear.id == row.fiscal_year_id,

                FiscalYear.business_id == business_id,

            )

        )

        if fy is None:

            raise DomainValidationError(

                "Fiscal Year does not exist for this business",

                code="period_closing_voucher_fiscal_year_not_found",

                details={"fiscal_year_id": str(row.fiscal_year_id)},

            )

        return fy



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PeriodClosingVoucher:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PeriodClosingVoucher]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PeriodClosingVoucher].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(PeriodClosingVoucher).where(

                    PeriodClosingVoucher.business_id == business_id

                )

            )

            or 0

        )

        return f"PER-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: PeriodClosingVoucherCreate

    ) -> PeriodClosingVoucher:

        row = PeriodClosingVoucher(

            business_id=business_id,

            name=self.next_name(db, business_id),

            transaction_date=payload.transaction_date,

            fiscal_year_id=payload.fiscal_year_id,

            amended_from=payload.amended_from,

            closing_account_head_id=payload.closing_account_head_id,

            remarks=payload.remarks,

            gle_processing_status=payload.gle_processing_status,

            error_message=payload.error_message,

            period_end_date=payload.period_end_date,

            period_start_date=payload.period_start_date,

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

        payload: PeriodClosingVoucherUpdate,

    ) -> PeriodClosingVoucher:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

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



    def submit(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PeriodClosingVoucher:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Period Closing Voucher")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PeriodClosingVoucher:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Period Closing Voucher")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row
