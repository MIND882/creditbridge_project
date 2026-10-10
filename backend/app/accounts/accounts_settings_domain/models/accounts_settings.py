"""

Accounts Settings -- converted from

``erpnext/accounts/doctype/accounts_settings``.



**This is a Frappe Single (``issingle: 1``), not a collection.** Upstream there

is exactly one ``Accounts Settings`` document per site. Here there is exactly one

row per ``business_id``, which is what makes that API different from every other

converted doctype: there is no ``POST /``, no ``GET /{id}`` and no ``DELETE /{id}``

-- just ``GET /`` (fetch, creating defaults on first read) and ``PATCH /``.

Enforced by a unique constraint on ``business_id`` alone.



Ported from ``validate()``:



    validate_auto_tax_settings()             -> the two "automatically add taxes"

                                                switches are mutually exclusive

    validate_stale_days()                    -> stale days must start at 1

    validate_and_sync_auto_reconcile_config() -> cron interval 1..59, queue size

                                                5..100



Not ported, because every one of them writes Frappe desk metadata rather than

application state: ``enable_payment_schedule_in_print``,

``toggle_accounting_dimension_sections``, ``toggle_sales_discount_section``,

``toggle_loyalty_point_program_section``, ``toggle_subscription_sections``,

``toggle_overdue_billing_threshold_field``,

``set_allow_on_submit_for_dimension_fields``, ``update_property_for_accounting_dimension``

and the ``frappe.db.set_default`` / ``frappe.clear_cache`` calls. They flip

``Property Setter`` rows and Custom Field flags -- concepts this conversion does

not have. The switches themselves are stored; only their desk side-effects are

absent.



``repost_allowed_types`` (a Table of ``Repost Allowed Types``) is not wired yet:

that child doctype has not been converted. It is read only by

``update_property_for_accounting_dimension``, which is itself not ported.

"""



from __future__ import annotations



import enum

from decimal import Decimal

from typing import Optional



from sqlalchemy import Boolean, Integer, Numeric, String, UniqueConstraint

from sqlalchemy import Enum as SAEnum

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = [

    "AccountsSettings",

    "AddressTaxCategorySource",

    "DeferredEntryBasis",

    "ExchangeGainLossPostingDate",

    "FetchMethod",

    "SameRateAction",

]





class AddressTaxCategorySource(str, enum.Enum):

    BILLING = "Billing Address"

    SHIPPING = "Shipping Address"





class DeferredEntryBasis(str, enum.Enum):

    DAYS = "Days"

    MONTHS = "Months"





class ExchangeGainLossPostingDate(str, enum.Enum):

    INVOICE = "Invoice"

    PAYMENT = "Payment"

    RECONCILIATION_DATE = "Reconciliation Date"





class FetchMethod(str, enum.Enum):

    BUFFERED = "Buffered Cursor"

    UNBUFFERED = "UnBuffered Cursor"





class SameRateAction(str, enum.Enum):

    STOP = "Stop"

    WARN = "Warn"





class AccountsSettings(TenantModel):

    """One row per tenant. There is no ``name`` -- a Single has no identity."""



    __tablename__ = "accounts_settings"

    __table_args__ = (

        UniqueConstraint("business_id", name="uq_accounts_settings_business_id"),

    )



    # ── tax behaviour ────────────────────────────────────────────────────────

    determine_address_tax_category_from: Mapped[AddressTaxCategorySource] = mapped_column(

        SAEnum(AddressTaxCategorySource, native_enum=False, length=20, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=False,

        default=AddressTaxCategorySource.BILLING,

    )

    #: Mutually exclusive with ``add_taxes_from_taxes_and_charges_template``.

    add_taxes_from_item_tax_template: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=True

    )

    add_taxes_from_taxes_and_charges_template: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    show_inclusive_tax_in_print: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    show_taxes_as_table_in_print: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    round_row_wise_tax: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    book_tax_discount_loss: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    merge_similar_account_heads: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    allow_pegged_currencies_exchange_rates: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )



    # ── exchange rates ───────────────────────────────────────────────────────

    allow_stale: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    #: Must be >= 1 when ``allow_stale`` is off.

    stale_days: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    maintain_same_internal_transaction_rate: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    maintain_same_rate_action: Mapped[SameRateAction] = mapped_column(

        SAEnum(SameRateAction, native_enum=False, length=10, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=False,

        default=SameRateAction.STOP,

    )

    exchange_gain_loss_posting_date: Mapped[ExchangeGainLossPostingDate] = mapped_column(

        SAEnum(

            ExchangeGainLossPostingDate, native_enum=False, length=25, validate_strings=True

        , values_callable=lambda e: [m.value for m in e]),

        nullable=False,

        default=ExchangeGainLossPostingDate.PAYMENT,

    )

    fetch_valuation_rate_for_internal_transaction: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )



    # ── payments and reconciliation ──────────────────────────────────────────

    make_payment_via_journal_entry: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    unlink_payment_on_cancellation_of_invoice: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    unlink_advance_payment_on_cancelation_of_order: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    auto_reconcile_payments: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    #: Minutes between auto-reconciliation runs; 1..59.

    auto_reconciliation_job_trigger: Mapped[int] = mapped_column(

        Integer, nullable=False, default=15

    )

    #: 5..100.

    reconciliation_queue_size: Mapped[int] = mapped_column(Integer, nullable=False, default=5)

    automatically_run_rules_on_unreconciled_transactions: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    enable_party_matching: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    enable_fuzzy_matching: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    transfer_match_days: Mapped[int] = mapped_column(Integer, nullable=False, default=3)

    automatically_fetch_payment_terms: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    fetch_payment_schedule_in_payment_request: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    receivable_payable_fetch_method: Mapped[FetchMethod] = mapped_column(

        SAEnum(FetchMethod, native_enum=False, length=20, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=False,

        default=FetchMethod.BUFFERED,

    )

    receivable_payable_remarks_length: Mapped[int] = mapped_column(

        Integer, nullable=False, default=0

    )

    general_ledger_remarks_length: Mapped[int] = mapped_column(

        Integer, nullable=False, default=0

    )

    delete_linked_ledger_entries: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    enable_immutable_ledger: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    ignore_account_closing_balance: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    ignore_is_opening_check_for_reporting: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    book_stock_expense_gl_entries: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )



    # ── billing controls ─────────────────────────────────────────────────────

    check_supplier_invoice_uniqueness: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    over_billing_allowance: Mapped[Optional[Decimal]] = mapped_column(

        Numeric(21, 9), nullable=True

    )

    enable_overdue_billing_threshold: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    enable_common_party_accounting: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    allow_multi_currency_invoices_against_single_party_account: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    confirm_before_resetting_posting_date: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    default_ageing_range: Mapped[Optional[str]] = mapped_column(

        String(140), nullable=True, default="30, 60, 90, 120"

    )



    # ── deferred accounting, assets, depreciation ────────────────────────────

    automatically_process_deferred_accounting_entry: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    book_deferred_entries_via_journal_entry: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    book_deferred_entries_based_on: Mapped[DeferredEntryBasis] = mapped_column(

        SAEnum(DeferredEntryBasis, native_enum=False, length=10, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=False,

        default=DeferredEntryBasis.DAYS,

    )

    submit_journal_entries: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    book_asset_depreciation_entry_automatically: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    calculate_depr_using_total_days: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    create_pr_in_draft_status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    pcv_job_timeout: Mapped[int] = mapped_column(Integer, nullable=False, default=3600)

    use_legacy_budget_controller: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    use_legacy_controller_for_pcv: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )



    # ── feature switches ─────────────────────────────────────────────────────

    enable_discounts_and_margin: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    enable_loyalty_point_program: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    enable_accounting_dimensions: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    enable_subscription: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    show_balance_in_coa: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    show_payment_schedule_in_print: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    preview_mode: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    # ── role names (upstream Links to Role; roles are not converted) ─────────

    credit_controller: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    role_allowed_to_over_bill: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    role_allowed_to_bypass_overdue_billing: Mapped[Optional[str]] = mapped_column(

        String(140), nullable=True

    )

    role_to_override_stop_action: Mapped[Optional[str]] = mapped_column(

        String(140), nullable=True

    )

    role_to_notify_on_depreciation_failure: Mapped[Optional[str]] = mapped_column(

        String(140), nullable=True

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<AccountsSettings id={self.id} business_id={self.business_id}>"
