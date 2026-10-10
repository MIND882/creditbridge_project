"""

Pydantic v2 schemas for AccountsSettings.



**A Frappe Single has no collection shape.** Upstream there is exactly one

``Accounts Settings`` document per site; here there is exactly one row per

``business_id``. So there is no ``Create`` schema and no ``ListResponse`` --

the row is created with defaults on first read, and the only writes are partial

updates.

"""



from __future__ import annotations



import uuid

from decimal import Decimal

from typing import Optional



from app.accounts.accounts_settings_domain.models.accounts_settings import (

    AddressTaxCategorySource,

    DeferredEntryBasis,

    ExchangeGainLossPostingDate,

    FetchMethod,

    SameRateAction,

)

from app.core.base_schema import InputSchema, ReadSchema



__all__ = ["AccountsSettingsUpdate", "AccountsSettingsRead"]





class AccountsSettingsUpdate(InputSchema):

    """

    A partial update of the tenant's single settings row.



    Every field is optional: this is a patch, and anything omitted keeps its

    current value. There is no create counterpart -- the row is materialised with

    upstream's defaults the first time it is read.

    """



    determine_address_tax_category_from: Optional[AddressTaxCategorySource] = None

    add_taxes_from_item_tax_template: Optional[bool] = None

    add_taxes_from_taxes_and_charges_template: Optional[bool] = None

    show_inclusive_tax_in_print: Optional[bool] = None

    show_taxes_as_table_in_print: Optional[bool] = None

    round_row_wise_tax: Optional[bool] = None

    book_tax_discount_loss: Optional[bool] = None

    merge_similar_account_heads: Optional[bool] = None

    allow_pegged_currencies_exchange_rates: Optional[bool] = None



    allow_stale: Optional[bool] = None

    stale_days: Optional[int] = None

    maintain_same_internal_transaction_rate: Optional[bool] = None

    maintain_same_rate_action: Optional[SameRateAction] = None

    exchange_gain_loss_posting_date: Optional[ExchangeGainLossPostingDate] = None

    fetch_valuation_rate_for_internal_transaction: Optional[bool] = None



    make_payment_via_journal_entry: Optional[bool] = None

    unlink_payment_on_cancellation_of_invoice: Optional[bool] = None

    unlink_advance_payment_on_cancelation_of_order: Optional[bool] = None

    auto_reconcile_payments: Optional[bool] = None

    auto_reconciliation_job_trigger: Optional[int] = None

    reconciliation_queue_size: Optional[int] = None

    automatically_run_rules_on_unreconciled_transactions: Optional[bool] = None

    enable_party_matching: Optional[bool] = None

    enable_fuzzy_matching: Optional[bool] = None

    transfer_match_days: Optional[int] = None

    automatically_fetch_payment_terms: Optional[bool] = None

    fetch_payment_schedule_in_payment_request: Optional[bool] = None

    receivable_payable_fetch_method: Optional[FetchMethod] = None

    receivable_payable_remarks_length: Optional[int] = None

    general_ledger_remarks_length: Optional[int] = None

    delete_linked_ledger_entries: Optional[bool] = None

    enable_immutable_ledger: Optional[bool] = None

    ignore_account_closing_balance: Optional[bool] = None

    ignore_is_opening_check_for_reporting: Optional[bool] = None

    book_stock_expense_gl_entries: Optional[bool] = None



    check_supplier_invoice_uniqueness: Optional[bool] = None

    over_billing_allowance: Optional[Decimal] = None

    enable_overdue_billing_threshold: Optional[bool] = None

    enable_common_party_accounting: Optional[bool] = None

    allow_multi_currency_invoices_against_single_party_account: Optional[bool] = None

    confirm_before_resetting_posting_date: Optional[bool] = None

    default_ageing_range: Optional[str] = None



    automatically_process_deferred_accounting_entry: Optional[bool] = None

    book_deferred_entries_via_journal_entry: Optional[bool] = None

    book_deferred_entries_based_on: Optional[DeferredEntryBasis] = None

    submit_journal_entries: Optional[bool] = None

    book_asset_depreciation_entry_automatically: Optional[bool] = None

    calculate_depr_using_total_days: Optional[bool] = None

    create_pr_in_draft_status: Optional[bool] = None

    pcv_job_timeout: Optional[int] = None

    use_legacy_budget_controller: Optional[bool] = None

    use_legacy_controller_for_pcv: Optional[bool] = None



    enable_discounts_and_margin: Optional[bool] = None

    enable_loyalty_point_program: Optional[bool] = None

    enable_accounting_dimensions: Optional[bool] = None

    enable_subscription: Optional[bool] = None

    show_balance_in_coa: Optional[bool] = None

    show_payment_schedule_in_print: Optional[bool] = None

    preview_mode: Optional[bool] = None



    credit_controller: Optional[str] = None

    role_allowed_to_over_bill: Optional[str] = None

    role_allowed_to_bypass_overdue_billing: Optional[str] = None

    role_to_override_stop_action: Optional[str] = None

    role_to_notify_on_depreciation_failure: Optional[str] = None





class AccountsSettingsRead(ReadSchema):

    id: uuid.UUID

    business_id: uuid.UUID



    determine_address_tax_category_from: AddressTaxCategorySource

    add_taxes_from_item_tax_template: bool

    add_taxes_from_taxes_and_charges_template: bool

    show_inclusive_tax_in_print: bool

    show_taxes_as_table_in_print: bool

    round_row_wise_tax: bool

    book_tax_discount_loss: bool

    merge_similar_account_heads: bool

    allow_pegged_currencies_exchange_rates: bool



    allow_stale: bool

    stale_days: int

    maintain_same_internal_transaction_rate: bool

    maintain_same_rate_action: SameRateAction

    exchange_gain_loss_posting_date: ExchangeGainLossPostingDate

    fetch_valuation_rate_for_internal_transaction: bool



    make_payment_via_journal_entry: bool

    unlink_payment_on_cancellation_of_invoice: bool

    unlink_advance_payment_on_cancelation_of_order: bool

    auto_reconcile_payments: bool

    auto_reconciliation_job_trigger: int

    reconciliation_queue_size: int

    automatically_run_rules_on_unreconciled_transactions: bool

    enable_party_matching: bool

    enable_fuzzy_matching: bool

    transfer_match_days: int

    automatically_fetch_payment_terms: bool

    fetch_payment_schedule_in_payment_request: bool

    receivable_payable_fetch_method: FetchMethod

    receivable_payable_remarks_length: int

    general_ledger_remarks_length: int

    delete_linked_ledger_entries: bool

    enable_immutable_ledger: bool

    ignore_account_closing_balance: bool

    ignore_is_opening_check_for_reporting: bool

    book_stock_expense_gl_entries: bool



    check_supplier_invoice_uniqueness: bool

    over_billing_allowance: Optional[Decimal] = None

    enable_overdue_billing_threshold: bool

    enable_common_party_accounting: bool

    allow_multi_currency_invoices_against_single_party_account: bool

    confirm_before_resetting_posting_date: bool

    default_ageing_range: Optional[str] = None



    automatically_process_deferred_accounting_entry: bool

    book_deferred_entries_via_journal_entry: bool

    book_deferred_entries_based_on: DeferredEntryBasis

    submit_journal_entries: bool

    book_asset_depreciation_entry_automatically: bool

    calculate_depr_using_total_days: bool

    create_pr_in_draft_status: bool

    pcv_job_timeout: int

    use_legacy_budget_controller: bool

    use_legacy_controller_for_pcv: bool



    enable_discounts_and_margin: bool

    enable_loyalty_point_program: bool

    enable_accounting_dimensions: bool

    enable_subscription: bool

    show_balance_in_coa: bool

    show_payment_schedule_in_print: bool

    preview_mode: bool



    credit_controller: Optional[str] = None

    role_allowed_to_over_bill: Optional[str] = None

    role_allowed_to_bypass_overdue_billing: Optional[str] = None

    role_to_override_stop_action: Optional[str] = None

    role_to_notify_on_depreciation_failure: Optional[str] = None
