# HAND-WRITTEN

"""

Business logic for Exchange Rate Revaluation -- port of

``erpnext/accounts/doctype/exchange_rate_revaluation/exchange_rate_revaluation.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream hooks:

    validate

    validate_rounding_loss_allowance

    set_total_gain_loss

    validate_mandatory

    before_submit

    remove_accounts_without_gain_loss

    on_cancel

    check_journal_and_reversal

    fetch_and_calculate_accounts_data

    get_accounts_data

    get_account_balance_from_gle

    calculate_new_account_balance

    throw_invalid_response_message

    get_for_unrealized_gain_loss_account

    make_jv_entries

    make_jv_for_zero_balance

    make_jv_for_revaluation

    make_reverse_journal



The two save-time rules -- ``validate_rounding_loss_allowance`` and

``set_total_gain_loss`` -- plus ``before_submit``'s

``remove_accounts_without_gain_loss`` are ported. The remaining throws sit in

the currency-fetching and GL-posting helpers, which need the live exchange

rate source; see :meth:`_validate`.

"""



from __future__ import annotations



import uuid

from decimal import Decimal

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.exchange_rate_revaluation_domain.models.exchange_rate_revaluation import ExchangeRateRevaluation

from app.accounts.exchange_rate_revaluation_account_domain.models.exchange_rate_revaluation_account import ExchangeRateRevaluationAccount

from app.accounts.exchange_rate_revaluation_domain.repositories.exchange_rate_revaluation_repository import (

    ExchangeRateRevaluationRepository,

)

from app.accounts.exchange_rate_revaluation_domain.schemas.exchange_rate_revaluation import (

    ExchangeRateRevaluationCreate,

    ExchangeRateRevaluationUpdate,

)

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ExchangeRateRevaluationService"]





def _dec(value) -> Decimal:

    """Coerce a possibly-None Numeric column to Decimal."""

    return Decimal(str(value if value is not None else 0))





class ExchangeRateRevaluationService:

    def __init__(self, repository: Optional[ExchangeRateRevaluationRepository] = None) -> None:

        self.repository = repository or ExchangeRateRevaluationRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ExchangeRateRevaluation:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Exchange Rate Revaluation", row_id)

        return row



    # ══════════════════════════════════════════════════════════════════════

    # ported validators

    # ══════════════════════════════════════════════════════════════════════

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: ExchangeRateRevaluation

    ) -> None:

        """

        Port of upstream ``validate``:



            validate_rounding_loss_allowance  -> ported

            set_total_gain_loss               -> ported



        Upstream also defines ``validate_mandatory`` (Company and Posting Date),

        but it is called from the whitelisted "get entries" action rather than

        from ``validate``, so it is not a save-time rule. Company is the tenant

        here and the Create schema already requires ``posting_date``, which is

        the only half of that check that applies.



        The remaining upstream ``frappe.throw`` sites live in the currency

        fetching and GL-posting helpers (``get_account_balances``,

        ``make_gl_entries``), which need the live exchange-rate source and the

        tax engine -- not ported.

        """

        self._validate_rounding_loss_allowance(row)

        self._set_total_gain_loss(row)



    # ── validate_rounding_loss_allowance ──────────────────────────────────

    def _validate_rounding_loss_allowance(self, row: ExchangeRateRevaluation) -> None:

        """

        The allowance is a fraction of the movement, so it must satisfy

        ``0 <= x < 1``. Upstream's bound is ``>= 1``, so exactly 1.0 is out of

        range.

        """

        allowance = _dec(row.rounding_loss_allowance)

        if allowance < 0 or allowance >= 1:

            raise DomainValidationError(

                "Rounding Loss Allowance should be between 0 and 1",

                code="exchange_rate_revaluation_rounding_allowance_out_of_range",

                details={"rounding_loss_allowance": str(allowance)},

            )



    # ── set_total_gain_loss ───────────────────────────────────────────────

    def _set_total_gain_loss(self, row: ExchangeRateRevaluation) -> None:

        """

        Derive each row's movement and roll it up.



        A row that is *not* zero-balance has its ``gain_loss`` recomputed from

        the two base-currency balances, so a client-supplied figure cannot

        survive. A zero-balance row has already been settled and keeps the

        figure it was booked at, and counts towards ``gain_loss_booked`` rather

        than ``gain_loss_unbooked``.

        """

        booked = Decimal(0)

        unbooked = Decimal(0)

        total = Decimal(0)



        for child in row.accounts:

            if not child.zero_balance:

                child.gain_loss = _dec(child.new_balance_in_base_currency) - _dec(

                    child.balance_in_base_currency

                )



            movement = _dec(child.gain_loss)

            if child.zero_balance:

                booked += movement

            else:

                unbooked += movement

            total += movement



        row.gain_loss_booked = booked

        row.gain_loss_unbooked = unbooked

        row.total_gain_loss = total



    # ── before_submit -> remove_accounts_without_gain_loss ────────────────

    def _before_submit(

        self, db: Session, business_id: uuid.UUID, row: ExchangeRateRevaluation

    ) -> None:

        """

        Drop rows whose rate did not move -- they would post a zero line. If

        nothing is left the voucher has nothing to book and cannot submit.



        The filter runs before the guard, so callers must roll back on failure

        or the rejection would silently empty the voucher.

        """

        moving = [c for c in row.accounts if _dec(c.gain_loss)]

        for child in list(row.accounts):

            if child not in moving:

                row.accounts.remove(child)



        if not moving:

            raise DomainValidationError(

                "At least one account with exchange gain or loss is required",

                code="exchange_rate_revaluation_no_gain_loss",

            )



        for idx, child in enumerate(moving, start=1):

            child.idx = idx

        db.flush()





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ExchangeRateRevaluation:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ExchangeRateRevaluation]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ExchangeRateRevaluation].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_accounts(

        self, business_id: uuid.UUID, row: ExchangeRateRevaluation, items: list[dict]

    ) -> None:

        row.accounts.clear()

        for idx, item in enumerate(items, start=1):

            row.accounts.append(

                ExchangeRateRevaluationAccount(

                    business_id=business_id,

                    idx=idx,

                    account_id=item.get('account_id'),

                    party_type=item.get('party_type'),

                    party=item.get('party'),

                    account_currency=item.get('account_currency'),

                    balance_in_account_currency=item.get('balance_in_account_currency'),

                    current_exchange_rate=item.get('current_exchange_rate'),

                    balance_in_base_currency=item.get('balance_in_base_currency'),

                    new_exchange_rate=item.get('new_exchange_rate'),

                    new_balance_in_base_currency=item.get('new_balance_in_base_currency'),

                    gain_loss=item.get('gain_loss'),

                    zero_balance=item.get('zero_balance'),

                    new_balance_in_account_currency=item.get('new_balance_in_account_currency'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(ExchangeRateRevaluation).where(

                    ExchangeRateRevaluation.business_id == business_id

                )

            )

            or 0

        )

        return f"EXC-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: ExchangeRateRevaluationCreate

    ) -> ExchangeRateRevaluation:

        row = ExchangeRateRevaluation(

            business_id=business_id,

            name=self.next_name(db, business_id),

            posting_date=payload.posting_date,

            amended_from=payload.amended_from,

            gain_loss_unbooked=payload.gain_loss_unbooked,

            gain_loss_booked=payload.gain_loss_booked,

            total_gain_loss=payload.total_gain_loss,

            rounding_loss_allowance=payload.rounding_loss_allowance,

        )

        self._replace_accounts(business_id, row, [x.model_dump() for x in payload.accounts])



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

        payload: ExchangeRateRevaluationUpdate,

    ) -> ExchangeRateRevaluation:

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



    def submit(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ExchangeRateRevaluation:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Exchange Rate Revaluation")

        try:

            self._before_submit(db, business_id, row)

            row.docstatus = DocStatus.SUBMITTED.value

        except Exception:

            db.rollback()

            raise

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ExchangeRateRevaluation:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Exchange Rate Revaluation")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row
