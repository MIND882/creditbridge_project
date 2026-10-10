import asyncio
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, business, consent, data, intelligence, lender, loans, invoices, upload, payments, documents, kyc
from app.crm.lead_domain.api.leads import router as lead_router
from app.crm.opportunity_domain.api.opportunity import router as opportunity_router
from app.customers.api.customer import router as msme_customer_router
from app.db.session import engine
from app.models import Base
from app.agents.event_stream import EventStreamConsumer, retry_pending_events
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Register all 191 accounts domain models so SQLAlchemy creates their tables
import app.accounts.all_models  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MSME Credit Intelligence Platform",
    version="1.0.0",
    docs_url="/docs"
)

origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://localhost:5174").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,          prefix="/v1/auth",          tags=["auth"])
app.include_router(consent.router,       prefix="/v1/consent",       tags=["consent"])
app.include_router(data.router,          prefix="/v1/data",           tags=["data"])
app.include_router(intelligence.router,  prefix="/v1/intelligence",   tags=["intelligence"])
app.include_router(lender.router,        prefix="/v1/lenders",        tags=["lenders"])
app.include_router(loans.router,         prefix="/v1/loans",          tags=["loans"])
app.include_router(business.router,      prefix="/v1/businesses",      tags=["businesses"])
app.include_router(invoices.router,      prefix="/v1/invoices",       tags=["invoices"])
app.include_router(upload.router,        prefix="/v1/upload",         tags=["upload"])
app.include_router(kyc.router,           prefix="/v1/kyc",            tags=["kyc"])
app.include_router(payments.router,      prefix="/v1/payments",       tags=["payments"])
app.include_router(documents.router,     prefix="/v1/documents",      tags=["documents"])
app.include_router(lead_router, prefix="/v1/leads", tags=["CRM - LEADS"])
app.include_router(opportunity_router, prefix="/v1/opportunities", tags=["CRM - OPPORTUNITIES"])
app.include_router(msme_customer_router, prefix="/v1/customers", tags=["CUSTOMERS"])


# ─── ERPNext 358 Modules (191 Accounts + 80 Stock + 19 Buying + 20 Selling + 48 Manufacturing) ───

# ACCOUNTS 191 imports
from app.accounts.account_domain.api.account import router as account_router
from app.accounts.account_category_domain.api.account_category import router as account_category_router
from app.accounts.cost_center_domain.api.cost_center import router as cost_center_router
from app.accounts.cost_center_allocation_domain.api.cost_center_allocation import router as cost_center_allocation_router
from app.accounts.cost_center_allocation_percentage_domain.api.cost_center_allocation_percentage import router as cc_alloc_pct_router
from app.accounts.accounting_period_domain.api.accounting_period import router as accounting_period_router
from app.accounts.finance_book_domain.api.finance_book import router as finance_book_router
from app.accounts.bank_account_type_domain.api.bank_account_type import router as bank_account_type_router
from app.accounts.bank_account_subtype_domain.api.bank_account_subtype import router as bank_account_subtype_router
from app.accounts.accounting_dimension_domain.api.accounting_dimension import router as accounting_dimension_router
from app.accounts.accounting_dimension_detail_domain.api.accounting_dimension_detail import router as accounting_dimension_detail_router
from app.accounts.applicable_on_account_domain.api.applicable_on_account import router as applicable_on_account_router
from app.accounts.allowed_dimension_domain.api.allowed_dimension import router as allowed_dimension_router
from app.accounts.bank_domain.api.bank import router as bank_router
from app.accounts.bank_transaction_mapping_domain.api.bank_transaction_mapping import router as bank_transaction_mapping_router
from app.accounts.bank_account_domain.api.bank_account import router as bank_account_router
from app.accounts.bank_account_balance_domain.api.bank_account_balance import router as bank_account_balance_router
from app.accounts.bank_guarantee_domain.api.bank_guarantee import router as bank_guarantee_router
from app.accounts.accounting_dimension_filter_domain.api.accounting_dimension_filter import router as accounting_dimension_filter_router
from app.accounts.bank_transaction_domain.api.bank_transaction import router as bank_transaction_router
from app.accounts.bank_transaction_payments_domain.api.bank_transaction_payments import router as bank_transaction_payments_router
from app.accounts.bank_transaction_rule_domain.api.bank_transaction_rule import router as bank_transaction_rule_router
from app.accounts.bank_transaction_rule_accounts_domain.api.bank_transaction_rule_accounts import router as bank_transaction_rule_accounts_router
from app.accounts.bank_transaction_rule_description_conditions_domain.api.bank_transaction_rule_description_conditions import router as bank_transaction_rule_description_conditions_router
from app.accounts.bank_clearance_domain.api.bank_clearance import router as bank_clearance_router
from app.accounts.bank_clearance_detail_domain.api.bank_clearance_detail import router as bank_clearance_detail_router
from app.accounts.gl_entry_domain.api.gl_entry import router as gl_entry_router
from app.accounts.journal_entry_domain.api.journal_entry import router as journal_entry_router
from app.accounts.payment_entry_domain.api.payment_entry import router as payment_entry_router
from app.accounts.payment_ledger_entry_domain.api.payment_ledger_entry import router as payment_ledger_entry_router
from app.accounts.payment_term_domain.api.payment_term import router as payment_term_router
from app.accounts.payment_terms_template_domain.api.payment_terms_template import router as payment_terms_template_router
from app.accounts.payment_terms_template_detail_domain.api.payment_terms_template_detail import router as payment_terms_template_detail_router
from app.accounts.payment_schedule_domain.api.payment_schedule import router as payment_schedule_router
from app.accounts.tax_withholding_category_domain.api.tax_withholding_category import router as tax_withholding_category_router
from app.accounts.tax_withholding_rate_domain.api.tax_withholding_rate import router as tax_withholding_rate_router
from app.accounts.tax_withholding_account_domain.api.tax_withholding_account import router as tax_withholding_account_router
from app.accounts.dunning_type_domain.api.dunning_type import router as dunning_type_router
from app.accounts.tax_category_domain.api.tax_category import router as tax_category_router
from app.accounts.sales_taxes_and_charges_template_domain.api.sales_taxes_and_charges_template import router as sales_taxes_and_charges_template_router
from app.accounts.purchase_taxes_and_charges_template_domain.api.purchase_taxes_and_charges_template import router as purchase_taxes_and_charges_template_router
from app.accounts.sales_taxes_and_charges_domain.api.sales_taxes_and_charges import router as sales_taxes_and_charges_router
from app.accounts.purchase_taxes_and_charges_domain.api.purchase_taxes_and_charges import router as purchase_taxes_and_charges_router
from app.accounts.advance_taxes_and_charges_domain.api.advance_taxes_and_charges import router as advance_taxes_and_charges_router
from app.accounts.item_tax_template_domain.api.item_tax_template import router as item_tax_template_router
from app.accounts.item_tax_template_detail_domain.api.item_tax_template_detail import router as item_tax_template_detail_router
from app.accounts.item_wise_tax_detail_domain.api.item_wise_tax_detail import router as item_wise_tax_detail_router
from app.accounts.tax_rule_domain.api.tax_rule import router as tax_rule_router
from app.accounts.share_type_domain.api.share_type import router as share_type_router
from app.accounts.shareholder_domain.api.shareholder import router as shareholder_router
from app.accounts.share_balance_domain.api.share_balance import router as share_balance_router
from app.accounts.mode_of_payment_domain.api.mode_of_payment import router as mode_of_payment_router
from app.accounts.mode_of_payment_account_domain.api.mode_of_payment_account import router as mode_of_payment_account_router
from app.accounts.journal_entry_template_domain.api.journal_entry_template import router as journal_entry_template_router
from app.accounts.journal_entry_template_account_domain.api.journal_entry_template_account import router as journal_entry_template_account_router
from app.accounts.fiscal_year_domain.api.fiscal_year import router as fiscal_year_router
from app.accounts.fiscal_year_company_domain.api.fiscal_year_company import router as fiscal_year_company_router
from app.accounts.accounts_settings_domain.api.accounts_settings import router as accounts_settings_router
from app.accounts.dunning_letter_text_domain.api.dunning_letter_text import router as dunning_letter_text_router
from app.accounts.journal_entry_account_domain.api.journal_entry_account import router as journal_entry_account_router
from app.accounts.payment_entry_deduction_domain.api.payment_entry_deduction import router as payment_entry_deduction_router
from app.accounts.payment_entry_reference_domain.api.payment_entry_reference import router as payment_entry_reference_router
from app.accounts.party_account_domain.api.party_account import router as party_account_router
from app.accounts.advance_payment_ledger_entry_domain.api.advance_payment_ledger_entry import router as advance_payment_ledger_entry_router
from app.accounts.allowed_to_transact_with_domain.api.allowed_to_transact_with import router as allowed_to_transact_with_router
from app.accounts.bisect_accounting_statements_domain.api.bisect_accounting_statements import router as bisect_accounting_statements_router
from app.accounts.bisect_nodes_domain.api.bisect_nodes import router as bisect_nodes_router
from app.accounts.cashier_closing_domain.api.cashier_closing import router as cashier_closing_router
from app.accounts.chart_of_accounts_importer_domain.api.chart_of_accounts_importer import router as chart_of_accounts_importer_router
from app.accounts.cheque_print_template_domain.api.cheque_print_template import router as cheque_print_template_router
from app.accounts.coupon_code_domain.api.coupon_code import router as coupon_code_router
from app.accounts.currency_exchange_settings_domain.api.currency_exchange_settings import router as currency_exchange_settings_router
from app.accounts.exchange_rate_revaluation_domain.api.exchange_rate_revaluation import router as exchange_rate_revaluation_router
from app.accounts.financial_report_template_domain.api.financial_report_template import router as financial_report_template_router
from app.accounts.loyalty_point_entry_domain.api.loyalty_point_entry import router as loyalty_point_entry_router
from app.accounts.loyalty_point_entry_redemption_domain.api.loyalty_point_entry_redemption import router as loyalty_point_entry_redemption_router
from app.accounts.party_link_domain.api.party_link import router as party_link_router
from app.accounts.pos_closing_entry_domain.api.pos_closing_entry import router as pos_closing_entry_router
from app.accounts.pos_invoice_merge_log_domain.api.pos_invoice_merge_log import router as pos_invoice_merge_log_router
from app.accounts.pos_invoice_reference_domain.api.pos_invoice_reference import router as pos_invoice_reference_router
from app.accounts.pos_opening_entry_domain.api.pos_opening_entry import router as pos_opening_entry_router
from app.accounts.pos_settings_domain.api.pos_settings import router as pos_settings_router
from app.accounts.pricing_rule_brand_domain.api.pricing_rule_brand import router as pricing_rule_brand_router
from app.accounts.pricing_rule_detail_domain.api.pricing_rule_detail import router as pricing_rule_detail_router
from app.accounts.pricing_rule_item_code_domain.api.pricing_rule_item_code import router as pricing_rule_item_code_router
from app.accounts.pricing_rule_item_group_domain.api.pricing_rule_item_group import router as pricing_rule_item_group_router
from app.accounts.pricing_rule_domain.api.pricing_rule import router as pricing_rule_router
from app.accounts.process_payment_reconciliation_log_domain.api.process_payment_reconciliation_log import router as process_payment_reconciliation_log_router
from app.accounts.process_period_closing_voucher_detail_domain.api.process_period_closing_voucher_detail import router as process_period_closing_voucher_detail_router
from app.accounts.process_period_closing_voucher_domain.api.process_period_closing_voucher import router as process_period_closing_voucher_router
from app.accounts.process_subscription_domain.api.process_subscription import router as process_subscription_router
from app.accounts.promotional_scheme_domain.api.promotional_scheme import router as promotional_scheme_router
from app.accounts.repost_accounting_ledger_domain.api.repost_accounting_ledger import router as repost_accounting_ledger_router
from app.accounts.repost_allowed_types_domain.api.repost_allowed_types import router as repost_allowed_types_router
from app.accounts.repost_payment_ledger_domain.api.repost_payment_ledger import router as repost_payment_ledger_router
from app.accounts.sales_invoice_advance_domain.api.sales_invoice_advance import router as sales_invoice_advance_router
from app.accounts.sales_invoice_timesheet_domain.api.sales_invoice_timesheet import router as sales_invoice_timesheet_router
from app.accounts.subscription_invoice_domain.api.subscription_invoice import router as subscription_invoice_router
from app.accounts.subscription_plan_detail_domain.api.subscription_plan_detail import router as subscription_plan_detail_router
from app.accounts.subscription_settings_domain.api.subscription_settings import router as subscription_settings_router
from app.accounts.transaction_deletion_record_details_domain.api.transaction_deletion_record_details import router as transaction_deletion_record_details_router
from app.accounts.unreconcile_payment_domain.api.unreconcile_payment import router as unreconcile_payment_router
from app.accounts.account_closing_balance_domain.api.account_closing_balance import router as account_closing_balance_router
from app.accounts.budget_account_domain.api.budget_account import router as budget_account_router
from app.accounts.budget_domain.api.budget import router as budget_router
from app.accounts.campaign_item_domain.api.campaign_item import router as campaign_item_router
from app.accounts.cashier_closing_payments_domain.api.cashier_closing_payments import router as cashier_closing_payments_router
from app.accounts.currency_exchange_settings_details_domain.api.currency_exchange_settings_details import router as currency_exchange_settings_details_router
from app.accounts.currency_exchange_settings_result_domain.api.currency_exchange_settings_result import router as currency_exchange_settings_result_router
from app.accounts.customer_group_item_domain.api.customer_group_item import router as customer_group_item_router
from app.accounts.customer_item_domain.api.customer_item import router as customer_item_router
from app.accounts.exchange_rate_revaluation_account_domain.api.exchange_rate_revaluation_account import router as exchange_rate_revaluation_account_router
from app.accounts.financial_report_row_domain.api.financial_report_row import router as financial_report_row_router
from app.accounts.invoice_discounting_domain.api.invoice_discounting import router as invoice_discounting_router
from app.accounts.ledger_merge_domain.api.ledger_merge import router as ledger_merge_router
from app.accounts.loyalty_program_domain.api.loyalty_program import router as loyalty_program_router
from app.accounts.monthly_distribution_domain.api.monthly_distribution import router as monthly_distribution_router
from app.accounts.opening_invoice_creation_tool_domain.api.opening_invoice_creation_tool import router as opening_invoice_creation_tool_router
from app.accounts.payment_gateway_account_domain.api.payment_gateway_account import router as payment_gateway_account_router
from app.accounts.payment_reconciliation_domain.api.payment_reconciliation import router as payment_reconciliation_router
from app.accounts.period_closing_voucher_domain.api.period_closing_voucher import router as period_closing_voucher_router
from app.accounts.pos_closing_entry_detail_domain.api.pos_closing_entry_detail import router as pos_closing_entry_detail_router
from app.accounts.pos_closing_entry_taxes_domain.api.pos_closing_entry_taxes import router as pos_closing_entry_taxes_router
from app.accounts.pos_field_domain.api.pos_field import router as pos_field_router
from app.accounts.pos_invoice_domain.api.pos_invoice import router as pos_invoice_router
from app.accounts.pos_opening_entry_detail_domain.api.pos_opening_entry_detail import router as pos_opening_entry_detail_router
from app.accounts.pos_profile_domain.api.pos_profile import router as pos_profile_router
from app.accounts.pos_search_fields_domain.api.pos_search_fields import router as pos_search_fields_router
from app.accounts.process_deferred_accounting_domain.api.process_deferred_accounting import router as process_deferred_accounting_router
from app.accounts.process_payment_reconciliation_log_allocations_domain.api.process_payment_reconciliation_log_allocations import router as process_payment_reconciliation_log_allocations_router
from app.accounts.process_payment_reconciliation_domain.api.process_payment_reconciliation import router as process_payment_reconciliation_router
from app.accounts.process_statement_of_accounts_domain.api.process_statement_of_accounts import router as process_statement_of_accounts_router
from app.accounts.promotional_scheme_price_discount_domain.api.promotional_scheme_price_discount import router as promotional_scheme_price_discount_router
from app.accounts.promotional_scheme_product_discount_domain.api.promotional_scheme_product_discount import router as promotional_scheme_product_discount_router
from app.accounts.purchase_invoice_domain.api.purchase_invoice import router as purchase_invoice_router
from app.accounts.repost_accounting_ledger_items_domain.api.repost_accounting_ledger_items import router as repost_accounting_ledger_items_router
from app.accounts.repost_payment_ledger_items_domain.api.repost_payment_ledger_items import router as repost_payment_ledger_items_router
from app.accounts.sales_invoice_payment_domain.api.sales_invoice_payment import router as sales_invoice_payment_router
from app.accounts.sales_invoice_reference_domain.api.sales_invoice_reference import router as sales_invoice_reference_router
from app.accounts.sales_invoice_domain.api.sales_invoice import router as sales_invoice_router
from app.accounts.sales_partner_item_domain.api.sales_partner_item import router as sales_partner_item_router
from app.accounts.share_transfer_domain.api.share_transfer import router as share_transfer_router
from app.accounts.ledger_health_domain.api.ledger_health import router as ledger_health_router
from app.accounts.ledger_health_monitor_domain.api.ledger_health_monitor import router as ledger_health_monitor_router
from app.accounts.ledger_health_monitor_company_domain.api.ledger_health_monitor_company import router as ledger_health_monitor_company_router
from app.accounts.pegged_currencies_domain.api.pegged_currencies import router as pegged_currencies_router
from app.accounts.pegged_currency_details_domain.api.pegged_currency_details import router as pegged_currency_details_router
from app.accounts.tax_withholding_group_domain.api.tax_withholding_group import router as tax_withholding_group_router
from app.accounts.shipping_rule_domain.api.shipping_rule import router as shipping_rule_router
from app.accounts.south_africa_vat_account_domain.api.south_africa_vat_account import router as south_africa_vat_account_router
from app.accounts.subscription_plan_domain.api.subscription_plan import router as subscription_plan_router
from app.accounts.subscription_domain.api.subscription import router as subscription_router
from app.accounts.supplier_group_item_domain.api.supplier_group_item import router as supplier_group_item_router
from app.accounts.supplier_item_domain.api.supplier_item import router as supplier_item_router
from app.accounts.tax_withholding_entry_domain.api.tax_withholding_entry import router as tax_withholding_entry_router
from app.accounts.territory_item_domain.api.territory_item import router as territory_item_router
from app.accounts.unreconcile_payment_entries_domain.api.unreconcile_payment_entries import router as unreconcile_payment_entries_router
from app.accounts.bank_reconciliation_tool_domain.api.bank_reconciliation_tool import router as bank_reconciliation_tool_router
from app.accounts.bank_statement_import_log_domain.api.bank_statement_import_log import router as bank_statement_import_log_router
from app.accounts.bank_statement_import_domain.api.bank_statement_import import router as bank_statement_import_router
from app.accounts.budget_distribution_domain.api.budget_distribution import router as budget_distribution_router
from app.accounts.discounted_invoice_domain.api.discounted_invoice import router as discounted_invoice_router
from app.accounts.dunning_domain.api.dunning import router as dunning_router
from app.accounts.ledger_merge_accounts_domain.api.ledger_merge_accounts import router as ledger_merge_accounts_router
from app.accounts.loyalty_program_collection_domain.api.loyalty_program_collection import router as loyalty_program_collection_router
from app.accounts.monthly_distribution_percentage_domain.api.monthly_distribution_percentage import router as monthly_distribution_percentage_router
from app.accounts.opening_invoice_creation_tool_item_domain.api.opening_invoice_creation_tool_item import router as opening_invoice_creation_tool_item_router
from app.accounts.payment_order_domain.api.payment_order import router as payment_order_router
from app.accounts.payment_reconciliation_allocation_domain.api.payment_reconciliation_allocation import router as payment_reconciliation_allocation_router
from app.accounts.payment_reconciliation_invoice_domain.api.payment_reconciliation_invoice import router as payment_reconciliation_invoice_router
from app.accounts.payment_reconciliation_payment_domain.api.payment_reconciliation_payment import router as payment_reconciliation_payment_router
from app.accounts.payment_request_domain.api.payment_request import router as payment_request_router
from app.accounts.pos_customer_group_domain.api.pos_customer_group import router as pos_customer_group_router
from app.accounts.pos_invoice_item_domain.api.pos_invoice_item import router as pos_invoice_item_router
from app.accounts.pos_item_group_domain.api.pos_item_group import router as pos_item_group_router
from app.accounts.pos_payment_method_domain.api.pos_payment_method import router as pos_payment_method_router
from app.accounts.pos_profile_user_domain.api.pos_profile_user import router as pos_profile_user_router
from app.accounts.process_statement_of_accounts_cc_domain.api.process_statement_of_accounts_cc import router as process_statement_of_accounts_cc_router
from app.accounts.process_statement_of_accounts_customer_domain.api.process_statement_of_accounts_customer import router as process_statement_of_accounts_customer_router
from app.accounts.psoa_cost_center_domain.api.psoa_cost_center import router as psoa_cost_center_router
from app.accounts.psoa_project_domain.api.psoa_project import router as psoa_project_router
from app.accounts.purchase_invoice_advance_domain.api.purchase_invoice_advance import router as purchase_invoice_advance_router
from app.accounts.purchase_invoice_item_domain.api.purchase_invoice_item import router as purchase_invoice_item_router
from app.accounts.sales_invoice_item_domain.api.sales_invoice_item import router as sales_invoice_item_router
from app.accounts.shipping_rule_condition_domain.api.shipping_rule_condition import router as shipping_rule_condition_router
from app.accounts.shipping_rule_country_domain.api.shipping_rule_country import router as shipping_rule_country_router
from app.accounts.bank_statement_import_log_column_map_domain.api.bank_statement_import_log_column_map import router as bank_statement_import_log_column_map_router
from app.accounts.overdue_payment_domain.api.overdue_payment import router as overdue_payment_router
from app.accounts.payment_order_reference_domain.api.payment_order_reference import router as payment_order_reference_router
from app.accounts.payment_reference_domain.api.payment_reference import router as payment_reference_router
from app.accounts.closed_document_domain.api.closed_document import router as closed_document_router

# STOCK 80 + BUYING 19 + SELLING 20 + MFG 48 = 167 imports
from app.stock.batch_domain.api.batch import router as batch_router
from app.stock.bin_domain.api.bin import router as bin_router
from app.stock.brand_domain.api.brand import router as brand_router
from app.stock.company_restriction_domain.api.company_restriction import router as company_restriction_router
from app.stock.customs_tariff_number_domain.api.customs_tariff_number import router as customs_tariff_number_router
from app.stock.delivery_note_domain.api.delivery_note import router as delivery_note_router
from app.stock.delivery_note_item_domain.api.delivery_note_item import router as delivery_note_item_router
from app.stock.delivery_settings_domain.api.delivery_settings import router as delivery_settings_router
from app.stock.delivery_stop_domain.api.delivery_stop import router as delivery_stop_router
from app.stock.delivery_trip_domain.api.delivery_trip import router as delivery_trip_router
from app.stock.inventory_dimension_domain.api.inventory_dimension import router as inventory_dimension_router
from app.stock.item_domain.api.item import router as item_router
from app.stock.item_alternative_domain.api.item_alternative import router as item_alternative_router
from app.stock.item_attribute_domain.api.item_attribute import router as item_attribute_router
from app.stock.item_attribute_value_domain.api.item_attribute_value import router as item_attribute_value_router
from app.stock.item_barcode_domain.api.item_barcode import router as item_barcode_router
from app.stock.item_customer_detail_domain.api.item_customer_detail import router as item_customer_detail_router
from app.stock.item_default_domain.api.item_default import router as item_default_router
from app.stock.item_group_domain.api.item_group import router as item_group_router
from app.stock.item_lead_time_domain.api.item_lead_time import router as item_lead_time_router
from app.stock.item_manufacturer_domain.api.item_manufacturer import router as item_manufacturer_router
from app.stock.item_price_domain.api.item_price import router as item_price_router
from app.stock.item_quality_inspection_parameter_domain.api.item_quality_inspection_parameter import router as item_quality_inspection_parameter_router
from app.stock.item_reorder_domain.api.item_reorder import router as item_reorder_router
from app.stock.item_standard_cost_domain.api.item_standard_cost import router as item_standard_cost_router
from app.stock.item_supplier_domain.api.item_supplier import router as item_supplier_router
from app.stock.item_tax_domain.api.item_tax import router as item_tax_router
from app.stock.item_variant_domain.api.item_variant import router as item_variant_router
from app.stock.item_variant_attribute_domain.api.item_variant_attribute import router as item_variant_attribute_router
from app.stock.item_variant_settings_domain.api.item_variant_settings import router as item_variant_settings_router
from app.stock.item_website_specification_domain.api.item_website_specification import router as item_website_specification_router
from app.stock.landed_cost_item_domain.api.landed_cost_item import router as landed_cost_item_router
from app.stock.landed_cost_purchase_receipt_domain.api.landed_cost_purchase_receipt import router as landed_cost_purchase_receipt_router
from app.stock.landed_cost_taxes_and_charges_domain.api.landed_cost_taxes_and_charges import router as landed_cost_taxes_and_charges_router
from app.stock.landed_cost_vendor_invoice_domain.api.landed_cost_vendor_invoice import router as landed_cost_vendor_invoice_router
from app.stock.landed_cost_voucher_domain.api.landed_cost_voucher import router as landed_cost_voucher_router
from app.stock.manufacturer_domain.api.manufacturer import router as manufacturer_router
from app.stock.material_request_domain.api.material_request import router as material_request_router
from app.stock.material_request_item_domain.api.material_request_item import router as material_request_item_router
from app.stock.packed_item_domain.api.packed_item import router as packed_item_router
from app.stock.packing_slip_domain.api.packing_slip import router as packing_slip_router
from app.stock.packing_slip_item_domain.api.packing_slip_item import router as packing_slip_item_router
from app.stock.pick_list_domain.api.pick_list import router as pick_list_router
from app.stock.pick_list_item_domain.api.pick_list_item import router as pick_list_item_router
from app.stock.price_list_domain.api.price_list import router as price_list_router
from app.stock.price_list_country_domain.api.price_list_country import router as price_list_country_router
from app.stock.purchase_receipt_domain.api.purchase_receipt import router as purchase_receipt_router
from app.stock.purchase_receipt_item_domain.api.purchase_receipt_item import router as purchase_receipt_item_router
from app.stock.putaway_rule_domain.api.putaway_rule import router as putaway_rule_router
from app.stock.quality_inspection_domain.api.quality_inspection import router as quality_inspection_router
from app.stock.quality_inspection_parameter_domain.api.quality_inspection_parameter import router as quality_inspection_parameter_router
from app.stock.quality_inspection_parameter_group_domain.api.quality_inspection_parameter_group import router as quality_inspection_parameter_group_router
from app.stock.quality_inspection_reading_domain.api.quality_inspection_reading import router as quality_inspection_reading_router
from app.stock.quality_inspection_template_domain.api.quality_inspection_template import router as quality_inspection_template_router
from app.stock.quick_stock_balance_domain.api.quick_stock_balance import router as quick_stock_balance_router
from app.stock.repost_item_valuation_domain.api.repost_item_valuation import router as repost_item_valuation_router
from app.stock.serial_and_batch_bundle_domain.api.serial_and_batch_bundle import router as serial_and_batch_bundle_router
from app.stock.serial_and_batch_entry_domain.api.serial_and_batch_entry import router as serial_and_batch_entry_router
from app.stock.serial_no_domain.api.serial_no import router as serial_no_router
from app.stock.shipment_domain.api.shipment import router as shipment_router
from app.stock.shipment_delivery_note_domain.api.shipment_delivery_note import router as shipment_delivery_note_router
from app.stock.shipment_parcel_domain.api.shipment_parcel import router as shipment_parcel_router
from app.stock.shipment_parcel_template_domain.api.shipment_parcel_template import router as shipment_parcel_template_router
from app.stock.stock_closing_balance_domain.api.stock_closing_balance import router as stock_closing_balance_router
from app.stock.stock_closing_entry_domain.api.stock_closing_entry import router as stock_closing_entry_router
from app.stock.stock_entry_domain.api.stock_entry import router as stock_entry_router
from app.stock.stock_entry_detail_domain.api.stock_entry_detail import router as stock_entry_detail_router
from app.stock.stock_entry_type_domain.api.stock_entry_type import router as stock_entry_type_router
from app.stock.stock_ledger_entry_domain.api.stock_ledger_entry import router as stock_ledger_entry_router
from app.stock.stock_reconciliation_domain.api.stock_reconciliation import router as stock_reconciliation_router
from app.stock.stock_reconciliation_item_domain.api.stock_reconciliation_item import router as stock_reconciliation_item_router
from app.stock.stock_reposting_settings_domain.api.stock_reposting_settings import router as stock_reposting_settings_router
from app.stock.stock_reservation_entry_domain.api.stock_reservation_entry import router as stock_reservation_entry_router
from app.stock.stock_settings_domain.api.stock_settings import router as stock_settings_router
from app.stock.uom_domain.api.uom import router as uom_router
from app.stock.uom_category_domain.api.uom_category import router as uom_category_router
from app.stock.uom_conversion_detail_domain.api.uom_conversion_detail import router as uom_conversion_detail_router
from app.stock.variant_field_domain.api.variant_field import router as variant_field_router
from app.stock.warehouse_domain.api.warehouse import router as warehouse_router
from app.stock.warehouse_type_domain.api.warehouse_type import router as warehouse_type_router
from app.buying.buying_settings_domain.api.buying_settings import router as buying_settings_router
from app.buying.customer_number_at_supplier_domain.api.customer_number_at_supplier import router as customer_number_at_supplier_router
from app.buying.purchase_order_domain.api.purchase_order import router as purchase_order_router
from app.buying.purchase_order_item_domain.api.purchase_order_item import router as purchase_order_item_router
from app.buying.purchase_receipt_item_supplied_domain.api.purchase_receipt_item_supplied import router as purchase_receipt_item_supplied_router
from app.buying.request_for_quotation_domain.api.request_for_quotation import router as request_for_quotation_router
from app.buying.request_for_quotation_item_domain.api.request_for_quotation_item import router as request_for_quotation_item_router
from app.buying.request_for_quotation_supplier_domain.api.request_for_quotation_supplier import router as request_for_quotation_supplier_router
from app.buying.supplier_domain.api.supplier import router as supplier_router
from app.buying.supplier_quotation_domain.api.supplier_quotation import router as supplier_quotation_router
from app.buying.supplier_quotation_item_domain.api.supplier_quotation_item import router as supplier_quotation_item_router
from app.buying.supplier_scorecard_domain.api.supplier_scorecard import router as supplier_scorecard_router
from app.buying.supplier_scorecard_criteria_domain.api.supplier_scorecard_criteria import router as supplier_scorecard_criteria_router
from app.buying.supplier_scorecard_period_domain.api.supplier_scorecard_period import router as supplier_scorecard_period_router
from app.buying.supplier_scorecard_scoring_criteria_domain.api.supplier_scorecard_scoring_criteria import router as supplier_scorecard_scoring_criteria_router
from app.buying.supplier_scorecard_scoring_standing_domain.api.supplier_scorecard_scoring_standing import router as supplier_scorecard_scoring_standing_router
from app.buying.supplier_scorecard_scoring_variable_domain.api.supplier_scorecard_scoring_variable import router as supplier_scorecard_scoring_variable_router
from app.buying.supplier_scorecard_standing_domain.api.supplier_scorecard_standing import router as supplier_scorecard_standing_router
from app.buying.supplier_scorecard_variable_domain.api.supplier_scorecard_variable import router as supplier_scorecard_variable_router
from app.selling.customer_domain.api.customer import router as erpnext_customer_router
from app.selling.customer_credit_limit_domain.api.customer_credit_limit import router as customer_credit_limit_router
from app.selling.delivery_schedule_item_domain.api.delivery_schedule_item import router as delivery_schedule_item_router
from app.selling.industry_type_domain.api.industry_type import router as industry_type_router
from app.selling.installation_note_domain.api.installation_note import router as installation_note_router
from app.selling.installation_note_item_domain.api.installation_note_item import router as installation_note_item_router
from app.selling.party_specific_item_domain.api.party_specific_item import router as party_specific_item_router
from app.selling.product_bundle_domain.api.product_bundle import router as product_bundle_router
from app.selling.product_bundle_item_domain.api.product_bundle_item import router as product_bundle_item_router
from app.selling.proforma_invoice_domain.api.proforma_invoice import router as proforma_invoice_router
from app.selling.proforma_invoice_item_domain.api.proforma_invoice_item import router as proforma_invoice_item_router
from app.selling.quotation_domain.api.quotation import router as quotation_router
from app.selling.quotation_item_domain.api.quotation_item import router as quotation_item_router
from app.selling.sales_order_domain.api.sales_order import router as sales_order_router
from app.selling.sales_order_item_domain.api.sales_order_item import router as sales_order_item_router
from app.selling.sales_partner_type_domain.api.sales_partner_type import router as sales_partner_type_router
from app.selling.sales_team_domain.api.sales_team import router as sales_team_router
from app.selling.selling_settings_domain.api.selling_settings import router as selling_settings_router
from app.selling.sms_center_domain.api.sms_center import router as sms_center_router
from app.selling.supplier_number_at_customer_domain.api.supplier_number_at_customer import router as supplier_number_at_customer_router
from app.manufacturing.blanket_order_domain.api.blanket_order import router as blanket_order_router
from app.manufacturing.blanket_order_item_domain.api.blanket_order_item import router as blanket_order_item_router
from app.manufacturing.bom_domain.api.bom import router as bom_router
from app.manufacturing.bom_creator_domain.api.bom_creator import router as bom_creator_router
from app.manufacturing.bom_creator_item_domain.api.bom_creator_item import router as bom_creator_item_router
from app.manufacturing.bom_explosion_item_domain.api.bom_explosion_item import router as bom_explosion_item_router
from app.manufacturing.bom_item_domain.api.bom_item import router as bom_item_router
from app.manufacturing.bom_operation_domain.api.bom_operation import router as bom_operation_router
from app.manufacturing.bom_secondary_item_domain.api.bom_secondary_item import router as bom_secondary_item_router
from app.manufacturing.bom_update_batch_domain.api.bom_update_batch import router as bom_update_batch_router
from app.manufacturing.bom_update_log_domain.api.bom_update_log import router as bom_update_log_router
from app.manufacturing.bom_update_tool_domain.api.bom_update_tool import router as bom_update_tool_router
from app.manufacturing.bom_website_item_domain.api.bom_website_item import router as bom_website_item_router
from app.manufacturing.bom_website_operation_domain.api.bom_website_operation import router as bom_website_operation_router
from app.manufacturing.downtime_entry_domain.api.downtime_entry import router as downtime_entry_router
from app.manufacturing.job_card_domain.api.job_card import router as job_card_router
from app.manufacturing.job_card_item_domain.api.job_card_item import router as job_card_item_router
from app.manufacturing.job_card_operation_domain.api.job_card_operation import router as job_card_operation_router
from app.manufacturing.job_card_scheduled_time_domain.api.job_card_scheduled_time import router as job_card_scheduled_time_router
from app.manufacturing.job_card_secondary_item_domain.api.job_card_secondary_item import router as job_card_secondary_item_router
from app.manufacturing.job_card_time_log_domain.api.job_card_time_log import router as job_card_time_log_router
from app.manufacturing.manufacturing_settings_domain.api.manufacturing_settings import router as manufacturing_settings_router
from app.manufacturing.master_production_schedule_domain.api.master_production_schedule import router as master_production_schedule_router
from app.manufacturing.master_production_schedule_item_domain.api.master_production_schedule_item import router as master_production_schedule_item_router
from app.manufacturing.material_request_plan_item_domain.api.material_request_plan_item import router as material_request_plan_item_router
from app.manufacturing.operation_domain.api.operation import router as operation_router
from app.manufacturing.plant_floor_domain.api.plant_floor import router as plant_floor_router
from app.manufacturing.production_plan_domain.api.production_plan import router as production_plan_router
from app.manufacturing.production_plan_item_domain.api.production_plan_item import router as production_plan_item_router
from app.manufacturing.production_plan_item_reference_domain.api.production_plan_item_reference import router as production_plan_item_reference_router
from app.manufacturing.production_plan_material_request_domain.api.production_plan_material_request import router as production_plan_material_request_router
from app.manufacturing.production_plan_material_request_warehouse_domain.api.production_plan_material_request_warehouse import router as production_plan_material_request_warehouse_router
from app.manufacturing.production_plan_sales_order_domain.api.production_plan_sales_order import router as production_plan_sales_order_router
from app.manufacturing.production_plan_sub_assembly_item_domain.api.production_plan_sub_assembly_item import router as production_plan_sub_assembly_item_router
from app.manufacturing.routing_domain.api.routing import router as routing_router
from app.manufacturing.sales_forecast_domain.api.sales_forecast import router as sales_forecast_router
from app.manufacturing.sales_forecast_item_domain.api.sales_forecast_item import router as sales_forecast_item_router
from app.manufacturing.sub_operation_domain.api.sub_operation import router as sub_operation_router
from app.manufacturing.work_order_domain.api.work_order import router as work_order_router
from app.manufacturing.work_order_additional_item_domain.api.work_order_additional_item import router as work_order_additional_item_router
from app.manufacturing.work_order_item_domain.api.work_order_item import router as work_order_item_router
from app.manufacturing.work_order_operation_domain.api.work_order_operation import router as work_order_operation_router
from app.manufacturing.workstation_domain.api.workstation import router as workstation_router
from app.manufacturing.workstation_cost_domain.api.workstation_cost import router as workstation_cost_router
from app.manufacturing.workstation_operating_component_domain.api.workstation_operating_component import router as workstation_operating_component_router
from app.manufacturing.workstation_operating_component_account_domain.api.workstation_operating_component_account import router as workstation_operating_component_account_router
from app.manufacturing.workstation_type_domain.api.workstation_type import router as workstation_type_router
from app.manufacturing.workstation_working_hour_domain.api.workstation_working_hour import router as workstation_working_hour_router


# ─── ROUTER INCLUDES ───
# ACCOUNTS 191
app.include_router(account_router,           prefix="/v1/accounts",           tags=["ACCOUNTS"])
app.include_router(account_category_router,  prefix="/v1/account-categories", tags=["ACCOUNTS"])
app.include_router(cost_center_router,       prefix="/v1/cost-centers",       tags=["ACCOUNTS"])
app.include_router(cost_center_allocation_router, prefix="/v1/cost-center-allocations", tags=["ACCOUNTS"])
app.include_router(cc_alloc_pct_router,      prefix="/v1/cost-center-allocation-percentages", tags=["ACCOUNTS"])
app.include_router(accounting_period_router, prefix="/v1/accounting-periods", tags=["ACCOUNTS"])
app.include_router(finance_book_router,      prefix="/v1/finance-books",      tags=["ACCOUNTS"])
app.include_router(bank_account_type_router, prefix="/v1/bank-account-types", tags=["ACCOUNTS"])
app.include_router(bank_account_subtype_router, prefix="/v1/bank-account-subtypes", tags=["ACCOUNTS"])
app.include_router(accounting_dimension_router, prefix="/v1/accounting-dimensions", tags=["ACCOUNTS"])
app.include_router(accounting_dimension_detail_router, prefix="/v1/accounting-dimension-details", tags=["ACCOUNTS"])
app.include_router(applicable_on_account_router, prefix="/v1/applicable-on-accounts", tags=["ACCOUNTS"])
app.include_router(allowed_dimension_router, prefix="/v1/allowed-dimensions", tags=["ACCOUNTS"])
app.include_router(bank_router, prefix="/v1/banks", tags=["ACCOUNTS"])
app.include_router(bank_transaction_mapping_router, prefix="/v1/bank-transaction-mappings", tags=["ACCOUNTS"])
app.include_router(bank_account_router, prefix="/v1/bank-accounts", tags=["ACCOUNTS"])
app.include_router(bank_account_balance_router, prefix="/v1/bank-account-balances", tags=["ACCOUNTS"])
app.include_router(bank_guarantee_router, prefix="/v1/bank-guarantees", tags=["ACCOUNTS"])
app.include_router(accounting_dimension_filter_router, prefix="/v1/accounting-dimension-filters", tags=["ACCOUNTS"])
app.include_router(bank_transaction_router, prefix="/v1/bank-transactions", tags=["ACCOUNTS"])
app.include_router(bank_transaction_payments_router, prefix="/v1/bank-transaction-payments", tags=["ACCOUNTS"])
app.include_router(bank_transaction_rule_router, prefix="/v1/bank-transaction-rules", tags=["ACCOUNTS"])
app.include_router(bank_transaction_rule_accounts_router, prefix="/v1/bank-transaction-rule-accounts", tags=["ACCOUNTS"])
app.include_router(bank_transaction_rule_description_conditions_router, prefix="/v1/bank-transaction-rule-description-conditions", tags=["ACCOUNTS"])
app.include_router(bank_clearance_router, prefix="/v1/bank-clearances", tags=["ACCOUNTS"])
app.include_router(bank_clearance_detail_router, prefix="/v1/bank-clearance-details", tags=["ACCOUNTS"])
app.include_router(gl_entry_router, prefix="/v1/gl-entries", tags=["ACCOUNTS"])
app.include_router(journal_entry_router, prefix="/v1/journal-entries", tags=["ACCOUNTS"])
app.include_router(payment_entry_router, prefix="/v1/payment-entries", tags=["ACCOUNTS"])
app.include_router(payment_ledger_entry_router, prefix="/v1/payment-ledger-entries", tags=["ACCOUNTS"])
app.include_router(payment_term_router, prefix="/v1/payment-terms", tags=["ACCOUNTS"])
app.include_router(payment_terms_template_router, prefix="/v1/payment-terms-templates", tags=["ACCOUNTS"])
app.include_router(payment_terms_template_detail_router, prefix="/v1/payment-terms-template-details", tags=["ACCOUNTS"])
app.include_router(payment_schedule_router, prefix="/v1/payment-schedules", tags=["ACCOUNTS"])
app.include_router(tax_withholding_category_router, prefix="/v1/tax-withholding-categories", tags=["ACCOUNTS"])
app.include_router(tax_withholding_rate_router, prefix="/v1/tax-withholding-rates", tags=["ACCOUNTS"])
app.include_router(tax_withholding_account_router, prefix="/v1/tax-withholding-accounts", tags=["ACCOUNTS"])
app.include_router(dunning_type_router, prefix="/v1/dunning-types", tags=["ACCOUNTS"])
app.include_router(tax_category_router, prefix="/v1/tax-categories", tags=["ACCOUNTS"])
app.include_router(sales_taxes_and_charges_template_router, prefix="/v1/sales-taxes-and-charges-templates", tags=["ACCOUNTS"])
app.include_router(purchase_taxes_and_charges_template_router, prefix="/v1/purchase-taxes-and-charges-templates", tags=["ACCOUNTS"])
app.include_router(sales_taxes_and_charges_router, prefix="/v1/sales-taxes-and-charges", tags=["ACCOUNTS"])
app.include_router(purchase_taxes_and_charges_router, prefix="/v1/purchase-taxes-and-charges", tags=["ACCOUNTS"])
app.include_router(advance_taxes_and_charges_router, prefix="/v1/advance-taxes-and-charges", tags=["ACCOUNTS"])
app.include_router(item_tax_template_router, prefix="/v1/item-tax-templates", tags=["ACCOUNTS"])
app.include_router(item_tax_template_detail_router, prefix="/v1/item-tax-template-details", tags=["ACCOUNTS"])
app.include_router(item_wise_tax_detail_router, prefix="/v1/item-wise-tax-details", tags=["ACCOUNTS"])
app.include_router(tax_rule_router, prefix="/v1/tax-rules", tags=["ACCOUNTS"])
app.include_router(share_type_router, prefix="/v1/share-types", tags=["ACCOUNTS"])
app.include_router(shareholder_router, prefix="/v1/shareholders", tags=["ACCOUNTS"])
app.include_router(share_balance_router, prefix="/v1/share-balances", tags=["ACCOUNTS"])
app.include_router(mode_of_payment_router, prefix="/v1/mode-of-payments", tags=["ACCOUNTS"])
app.include_router(mode_of_payment_account_router, prefix="/v1/mode-of-payment-accounts", tags=["ACCOUNTS"])
app.include_router(journal_entry_template_router, prefix="/v1/journal-entry-templates", tags=["ACCOUNTS"])
app.include_router(journal_entry_template_account_router, prefix="/v1/journal-entry-template-accounts", tags=["ACCOUNTS"])
app.include_router(fiscal_year_router, prefix="/v1/fiscal-years", tags=["ACCOUNTS"])
app.include_router(fiscal_year_company_router, prefix="/v1/fiscal-year-companies", tags=["ACCOUNTS"])
app.include_router(accounts_settings_router, prefix="/v1/accounts-settings", tags=["ACCOUNTS"])
app.include_router(dunning_letter_text_router, prefix="/v1/dunning-letter-texts", tags=["ACCOUNTS"])
app.include_router(journal_entry_account_router, prefix="/v1/journal-entry-accounts", tags=["ACCOUNTS"])
app.include_router(payment_entry_deduction_router, prefix="/v1/payment-entry-deductions", tags=["ACCOUNTS"])
app.include_router(payment_entry_reference_router, prefix="/v1/payment-entry-references", tags=["ACCOUNTS"])
app.include_router(party_account_router, prefix="/v1/party-accounts", tags=["ACCOUNTS"])
app.include_router(advance_payment_ledger_entry_router, prefix="/v1/advance-payment-ledger-entry", tags=["ACCOUNTS"])
app.include_router(allowed_to_transact_with_router, prefix="/v1/allowed-to-transact-with", tags=["ACCOUNTS"])
app.include_router(bisect_accounting_statements_router, prefix="/v1/bisect-accounting-statements", tags=["ACCOUNTS"])
app.include_router(bisect_nodes_router, prefix="/v1/bisect-nodes", tags=["ACCOUNTS"])
app.include_router(cashier_closing_router, prefix="/v1/cashier-closing", tags=["ACCOUNTS"])
app.include_router(chart_of_accounts_importer_router, prefix="/v1/chart-of-accounts-importer", tags=["ACCOUNTS"])
app.include_router(cheque_print_template_router, prefix="/v1/cheque-print-template", tags=["ACCOUNTS"])
app.include_router(coupon_code_router, prefix="/v1/coupon-code", tags=["ACCOUNTS"])
app.include_router(currency_exchange_settings_router, prefix="/v1/currency-exchange-settings", tags=["ACCOUNTS"])
app.include_router(exchange_rate_revaluation_router, prefix="/v1/exchange-rate-revaluation", tags=["ACCOUNTS"])
app.include_router(financial_report_template_router, prefix="/v1/financial-report-template", tags=["ACCOUNTS"])
app.include_router(loyalty_point_entry_router, prefix="/v1/loyalty-point-entry", tags=["ACCOUNTS"])
app.include_router(loyalty_point_entry_redemption_router, prefix="/v1/loyalty-point-entry-redemption", tags=["ACCOUNTS"])
app.include_router(party_link_router, prefix="/v1/party-link", tags=["ACCOUNTS"])
app.include_router(pos_closing_entry_router, prefix="/v1/pos-closing-entry", tags=["ACCOUNTS"])
app.include_router(pos_invoice_merge_log_router, prefix="/v1/pos-invoice-merge-log", tags=["ACCOUNTS"])
app.include_router(pos_invoice_reference_router, prefix="/v1/pos-invoice-reference", tags=["ACCOUNTS"])
app.include_router(pos_opening_entry_router, prefix="/v1/pos-opening-entry", tags=["ACCOUNTS"])
app.include_router(pos_settings_router, prefix="/v1/pos-settings", tags=["ACCOUNTS"])
app.include_router(pricing_rule_brand_router, prefix="/v1/pricing-rule-brand", tags=["ACCOUNTS"])
app.include_router(pricing_rule_detail_router, prefix="/v1/pricing-rule-detail", tags=["ACCOUNTS"])
app.include_router(pricing_rule_item_code_router, prefix="/v1/pricing-rule-item-code", tags=["ACCOUNTS"])
app.include_router(pricing_rule_item_group_router, prefix="/v1/pricing-rule-item-group", tags=["ACCOUNTS"])
app.include_router(pricing_rule_router, prefix="/v1/pricing-rule", tags=["ACCOUNTS"])
app.include_router(process_payment_reconciliation_log_router, prefix="/v1/process-payment-reconciliation-log", tags=["ACCOUNTS"])
app.include_router(process_period_closing_voucher_detail_router, prefix="/v1/process-period-closing-voucher-detail", tags=["ACCOUNTS"])
app.include_router(process_period_closing_voucher_router, prefix="/v1/process-period-closing-voucher", tags=["ACCOUNTS"])
app.include_router(process_subscription_router, prefix="/v1/process-subscription", tags=["ACCOUNTS"])
app.include_router(promotional_scheme_router, prefix="/v1/promotional-scheme", tags=["ACCOUNTS"])
app.include_router(repost_accounting_ledger_router, prefix="/v1/repost-accounting-ledger", tags=["ACCOUNTS"])
app.include_router(repost_allowed_types_router, prefix="/v1/repost-allowed-types", tags=["ACCOUNTS"])
app.include_router(repost_payment_ledger_router, prefix="/v1/repost-payment-ledger", tags=["ACCOUNTS"])
app.include_router(sales_invoice_advance_router, prefix="/v1/sales-invoice-advance", tags=["ACCOUNTS"])
app.include_router(sales_invoice_timesheet_router, prefix="/v1/sales-invoice-timesheet", tags=["ACCOUNTS"])
app.include_router(subscription_invoice_router, prefix="/v1/subscription-invoice", tags=["ACCOUNTS"])
app.include_router(subscription_plan_detail_router, prefix="/v1/subscription-plan-detail", tags=["ACCOUNTS"])
app.include_router(subscription_settings_router, prefix="/v1/subscription-settings", tags=["ACCOUNTS"])
app.include_router(transaction_deletion_record_details_router, prefix="/v1/transaction-deletion-record-details", tags=["ACCOUNTS"])
app.include_router(unreconcile_payment_router, prefix="/v1/unreconcile-payment", tags=["ACCOUNTS"])
app.include_router(account_closing_balance_router, prefix="/v1/account-closing-balance", tags=["ACCOUNTS"])
app.include_router(budget_account_router, prefix="/v1/budget-account", tags=["ACCOUNTS"])
app.include_router(budget_router, prefix="/v1/budget", tags=["ACCOUNTS"])
app.include_router(campaign_item_router, prefix="/v1/campaign-item", tags=["ACCOUNTS"])
app.include_router(cashier_closing_payments_router, prefix="/v1/cashier-closing-payments", tags=["ACCOUNTS"])
app.include_router(currency_exchange_settings_details_router, prefix="/v1/currency-exchange-settings-details", tags=["ACCOUNTS"])
app.include_router(currency_exchange_settings_result_router, prefix="/v1/currency-exchange-settings-result", tags=["ACCOUNTS"])
app.include_router(customer_group_item_router, prefix="/v1/customer-group-item", tags=["ACCOUNTS"])
app.include_router(customer_item_router, prefix="/v1/customer-item", tags=["ACCOUNTS"])
app.include_router(exchange_rate_revaluation_account_router, prefix="/v1/exchange-rate-revaluation-account", tags=["ACCOUNTS"])
app.include_router(financial_report_row_router, prefix="/v1/financial-report-row", tags=["ACCOUNTS"])
app.include_router(invoice_discounting_router, prefix="/v1/invoice-discounting", tags=["ACCOUNTS"])
app.include_router(ledger_merge_router, prefix="/v1/ledger-merge", tags=["ACCOUNTS"])
app.include_router(loyalty_program_router, prefix="/v1/loyalty-program", tags=["ACCOUNTS"])
app.include_router(monthly_distribution_router, prefix="/v1/monthly-distribution", tags=["ACCOUNTS"])
app.include_router(opening_invoice_creation_tool_router, prefix="/v1/opening-invoice-creation-tool", tags=["ACCOUNTS"])
app.include_router(payment_gateway_account_router, prefix="/v1/payment-gateway-account", tags=["ACCOUNTS"])
app.include_router(payment_reconciliation_router, prefix="/v1/payment-reconciliation", tags=["ACCOUNTS"])
app.include_router(period_closing_voucher_router, prefix="/v1/period-closing-voucher", tags=["ACCOUNTS"])
app.include_router(pos_closing_entry_detail_router, prefix="/v1/pos-closing-entry-detail", tags=["ACCOUNTS"])
app.include_router(pos_closing_entry_taxes_router, prefix="/v1/pos-closing-entry-taxes", tags=["ACCOUNTS"])
app.include_router(pos_field_router, prefix="/v1/pos-field", tags=["ACCOUNTS"])
app.include_router(pos_invoice_router, prefix="/v1/pos-invoice", tags=["ACCOUNTS"])
app.include_router(pos_opening_entry_detail_router, prefix="/v1/pos-opening-entry-detail", tags=["ACCOUNTS"])
app.include_router(pos_profile_router, prefix="/v1/pos-profile", tags=["ACCOUNTS"])
app.include_router(pos_search_fields_router, prefix="/v1/pos-search-fields", tags=["ACCOUNTS"])
app.include_router(process_deferred_accounting_router, prefix="/v1/process-deferred-accounting", tags=["ACCOUNTS"])
app.include_router(process_payment_reconciliation_log_allocations_router, prefix="/v1/process-payment-reconciliation-log-allocations", tags=["ACCOUNTS"])
app.include_router(process_payment_reconciliation_router, prefix="/v1/process-payment-reconciliation", tags=["ACCOUNTS"])
app.include_router(process_statement_of_accounts_router, prefix="/v1/process-statement-of-accounts", tags=["ACCOUNTS"])
app.include_router(promotional_scheme_price_discount_router, prefix="/v1/promotional-scheme-price-discount", tags=["ACCOUNTS"])
app.include_router(promotional_scheme_product_discount_router, prefix="/v1/promotional-scheme-product-discount", tags=["ACCOUNTS"])
app.include_router(purchase_invoice_router, prefix="/v1/purchase-invoice", tags=["ACCOUNTS"])
app.include_router(repost_accounting_ledger_items_router, prefix="/v1/repost-accounting-ledger-items", tags=["ACCOUNTS"])
app.include_router(repost_payment_ledger_items_router, prefix="/v1/repost-payment-ledger-items", tags=["ACCOUNTS"])
app.include_router(sales_invoice_payment_router, prefix="/v1/sales-invoice-payment", tags=["ACCOUNTS"])
app.include_router(sales_invoice_reference_router, prefix="/v1/sales-invoice-reference", tags=["ACCOUNTS"])
app.include_router(sales_invoice_router, prefix="/v1/sales-invoice", tags=["ACCOUNTS"])
app.include_router(sales_partner_item_router, prefix="/v1/sales-partner-item", tags=["ACCOUNTS"])
app.include_router(share_transfer_router, prefix="/v1/share-transfer", tags=["ACCOUNTS"])
app.include_router(ledger_health_router, prefix="/v1/ledger-health", tags=["ACCOUNTS"])
app.include_router(ledger_health_monitor_router, prefix="/v1/ledger-health-monitor", tags=["ACCOUNTS"])
app.include_router(ledger_health_monitor_company_router, prefix="/v1/ledger-health-monitor-companies", tags=["ACCOUNTS"])
app.include_router(pegged_currencies_router, prefix="/v1/pegged-currencies", tags=["ACCOUNTS"])
app.include_router(pegged_currency_details_router, prefix="/v1/pegged-currency-details", tags=["ACCOUNTS"])
app.include_router(tax_withholding_group_router, prefix="/v1/tax-withholding-groups", tags=["ACCOUNTS"])
app.include_router(shipping_rule_router, prefix="/v1/shipping-rule", tags=["ACCOUNTS"])
app.include_router(south_africa_vat_account_router, prefix="/v1/south-africa-vat-account", tags=["ACCOUNTS"])
app.include_router(subscription_plan_router, prefix="/v1/subscription-plan", tags=["ACCOUNTS"])
app.include_router(subscription_router, prefix="/v1/subscription", tags=["ACCOUNTS"])
app.include_router(supplier_group_item_router, prefix="/v1/supplier-group-item", tags=["ACCOUNTS"])
app.include_router(supplier_item_router, prefix="/v1/supplier-item", tags=["ACCOUNTS"])
app.include_router(tax_withholding_entry_router, prefix="/v1/tax-withholding-entry", tags=["ACCOUNTS"])
app.include_router(territory_item_router, prefix="/v1/territory-item", tags=["ACCOUNTS"])
app.include_router(unreconcile_payment_entries_router, prefix="/v1/unreconcile-payment-entries", tags=["ACCOUNTS"])
app.include_router(bank_reconciliation_tool_router, prefix="/v1/bank-reconciliation-tool", tags=["ACCOUNTS"])
app.include_router(bank_statement_import_log_router, prefix="/v1/bank-statement-import-log", tags=["ACCOUNTS"])
app.include_router(bank_statement_import_router, prefix="/v1/bank-statement-import", tags=["ACCOUNTS"])
app.include_router(budget_distribution_router, prefix="/v1/budget-distribution", tags=["ACCOUNTS"])
app.include_router(discounted_invoice_router, prefix="/v1/discounted-invoice", tags=["ACCOUNTS"])
app.include_router(dunning_router, prefix="/v1/dunning", tags=["ACCOUNTS"])
app.include_router(ledger_merge_accounts_router, prefix="/v1/ledger-merge-accounts", tags=["ACCOUNTS"])
app.include_router(loyalty_program_collection_router, prefix="/v1/loyalty-program-collection", tags=["ACCOUNTS"])
app.include_router(monthly_distribution_percentage_router, prefix="/v1/monthly-distribution-percentage", tags=["ACCOUNTS"])
app.include_router(opening_invoice_creation_tool_item_router, prefix="/v1/opening-invoice-creation-tool-item", tags=["ACCOUNTS"])
app.include_router(payment_order_router, prefix="/v1/payment-order", tags=["ACCOUNTS"])
app.include_router(payment_reconciliation_allocation_router, prefix="/v1/payment-reconciliation-allocation", tags=["ACCOUNTS"])
app.include_router(payment_reconciliation_invoice_router, prefix="/v1/payment-reconciliation-invoice", tags=["ACCOUNTS"])
app.include_router(payment_reconciliation_payment_router, prefix="/v1/payment-reconciliation-payment", tags=["ACCOUNTS"])
app.include_router(payment_request_router, prefix="/v1/payment-request", tags=["ACCOUNTS"])
app.include_router(pos_customer_group_router, prefix="/v1/pos-customer-group", tags=["ACCOUNTS"])
app.include_router(pos_invoice_item_router, prefix="/v1/pos-invoice-item", tags=["ACCOUNTS"])
app.include_router(pos_item_group_router, prefix="/v1/pos-item-group", tags=["ACCOUNTS"])
app.include_router(pos_payment_method_router, prefix="/v1/pos-payment-method", tags=["ACCOUNTS"])
app.include_router(pos_profile_user_router, prefix="/v1/pos-profile-user", tags=["ACCOUNTS"])
app.include_router(process_statement_of_accounts_cc_router, prefix="/v1/process-statement-of-accounts-cc", tags=["ACCOUNTS"])
app.include_router(process_statement_of_accounts_customer_router, prefix="/v1/process-statement-of-accounts-customer", tags=["ACCOUNTS"])
app.include_router(psoa_cost_center_router, prefix="/v1/psoa-cost-center", tags=["ACCOUNTS"])
app.include_router(psoa_project_router, prefix="/v1/psoa-project", tags=["ACCOUNTS"])
app.include_router(purchase_invoice_advance_router, prefix="/v1/purchase-invoice-advance", tags=["ACCOUNTS"])
app.include_router(purchase_invoice_item_router, prefix="/v1/purchase-invoice-item", tags=["ACCOUNTS"])
app.include_router(sales_invoice_item_router, prefix="/v1/sales-invoice-item", tags=["ACCOUNTS"])
app.include_router(shipping_rule_condition_router, prefix="/v1/shipping-rule-condition", tags=["ACCOUNTS"])
app.include_router(shipping_rule_country_router, prefix="/v1/shipping-rule-country", tags=["ACCOUNTS"])
app.include_router(bank_statement_import_log_column_map_router, prefix="/v1/bank-statement-import-log-column-map", tags=["ACCOUNTS"])
app.include_router(overdue_payment_router, prefix="/v1/overdue-payment", tags=["ACCOUNTS"])
app.include_router(payment_order_reference_router, prefix="/v1/payment-order-reference", tags=["ACCOUNTS"])
app.include_router(payment_reference_router, prefix="/v1/payment-reference", tags=["ACCOUNTS"])
app.include_router(closed_document_router, prefix="/v1/closed-document", tags=["ACCOUNTS"])

# STOCK 80 + BUYING 19 + SELLING 20 + MFG 48 = 167 routers
app.include_router(batch_router, prefix="/v1/batch", tags=["STOCK"])
app.include_router(bin_router, prefix="/v1/bin", tags=["STOCK"])
app.include_router(brand_router, prefix="/v1/brand", tags=["STOCK"])
app.include_router(company_restriction_router, prefix="/v1/company-restriction", tags=["STOCK"])
app.include_router(customs_tariff_number_router, prefix="/v1/customs-tariff-number", tags=["STOCK"])
app.include_router(delivery_note_router, prefix="/v1/delivery-note", tags=["STOCK"])
app.include_router(delivery_note_item_router, prefix="/v1/delivery-note-item", tags=["STOCK"])
app.include_router(delivery_settings_router, prefix="/v1/delivery-settings", tags=["STOCK"])
app.include_router(delivery_stop_router, prefix="/v1/delivery-stop", tags=["STOCK"])
app.include_router(delivery_trip_router, prefix="/v1/delivery-trip", tags=["STOCK"])
app.include_router(inventory_dimension_router, prefix="/v1/inventory-dimension", tags=["STOCK"])
app.include_router(item_router, prefix="/v1/item", tags=["STOCK"])
app.include_router(item_alternative_router, prefix="/v1/item-alternative", tags=["STOCK"])
app.include_router(item_attribute_router, prefix="/v1/item-attribute", tags=["STOCK"])
app.include_router(item_attribute_value_router, prefix="/v1/item-attribute-value", tags=["STOCK"])
app.include_router(item_barcode_router, prefix="/v1/item-barcode", tags=["STOCK"])
app.include_router(item_customer_detail_router, prefix="/v1/item-customer-detail", tags=["STOCK"])
app.include_router(item_default_router, prefix="/v1/item-default", tags=["STOCK"])
app.include_router(item_group_router, prefix="/v1/item-group", tags=["STOCK"])
app.include_router(item_lead_time_router, prefix="/v1/item-lead-time", tags=["STOCK"])
app.include_router(item_manufacturer_router, prefix="/v1/item-manufacturer", tags=["STOCK"])
app.include_router(item_price_router, prefix="/v1/item-price", tags=["STOCK"])
app.include_router(item_quality_inspection_parameter_router, prefix="/v1/item-quality-inspection-parameter", tags=["STOCK"])
app.include_router(item_reorder_router, prefix="/v1/item-reorder", tags=["STOCK"])
app.include_router(item_standard_cost_router, prefix="/v1/item-standard-cost", tags=["STOCK"])
app.include_router(item_supplier_router, prefix="/v1/item-supplier", tags=["STOCK"])
app.include_router(item_tax_router, prefix="/v1/item-tax", tags=["STOCK"])
app.include_router(item_variant_router, prefix="/v1/item-variant", tags=["STOCK"])
app.include_router(item_variant_attribute_router, prefix="/v1/item-variant-attribute", tags=["STOCK"])
app.include_router(item_variant_settings_router, prefix="/v1/item-variant-settings", tags=["STOCK"])
app.include_router(item_website_specification_router, prefix="/v1/item-website-specification", tags=["STOCK"])
app.include_router(landed_cost_item_router, prefix="/v1/landed-cost-item", tags=["STOCK"])
app.include_router(landed_cost_purchase_receipt_router, prefix="/v1/landed-cost-purchase-receipt", tags=["STOCK"])
app.include_router(landed_cost_taxes_and_charges_router, prefix="/v1/landed-cost-taxes-and-charges", tags=["STOCK"])
app.include_router(landed_cost_vendor_invoice_router, prefix="/v1/landed-cost-vendor-invoice", tags=["STOCK"])
app.include_router(landed_cost_voucher_router, prefix="/v1/landed-cost-voucher", tags=["STOCK"])
app.include_router(manufacturer_router, prefix="/v1/manufacturer", tags=["STOCK"])
app.include_router(material_request_router, prefix="/v1/material-request", tags=["STOCK"])
app.include_router(material_request_item_router, prefix="/v1/material-request-item", tags=["STOCK"])
app.include_router(packed_item_router, prefix="/v1/packed-item", tags=["STOCK"])
app.include_router(packing_slip_router, prefix="/v1/packing-slip", tags=["STOCK"])
app.include_router(packing_slip_item_router, prefix="/v1/packing-slip-item", tags=["STOCK"])
app.include_router(pick_list_router, prefix="/v1/pick-list", tags=["STOCK"])
app.include_router(pick_list_item_router, prefix="/v1/pick-list-item", tags=["STOCK"])
app.include_router(price_list_router, prefix="/v1/price-list", tags=["STOCK"])
app.include_router(price_list_country_router, prefix="/v1/price-list-country", tags=["STOCK"])
app.include_router(purchase_receipt_router, prefix="/v1/purchase-receipt", tags=["STOCK"])
app.include_router(purchase_receipt_item_router, prefix="/v1/purchase-receipt-item", tags=["STOCK"])
app.include_router(putaway_rule_router, prefix="/v1/putaway-rule", tags=["STOCK"])
app.include_router(quality_inspection_router, prefix="/v1/quality-inspection", tags=["STOCK"])
app.include_router(quality_inspection_parameter_router, prefix="/v1/quality-inspection-parameter", tags=["STOCK"])
app.include_router(quality_inspection_parameter_group_router, prefix="/v1/quality-inspection-parameter-group", tags=["STOCK"])
app.include_router(quality_inspection_reading_router, prefix="/v1/quality-inspection-reading", tags=["STOCK"])
app.include_router(quality_inspection_template_router, prefix="/v1/quality-inspection-template", tags=["STOCK"])
app.include_router(quick_stock_balance_router, prefix="/v1/quick-stock-balance", tags=["STOCK"])
app.include_router(repost_item_valuation_router, prefix="/v1/repost-item-valuation", tags=["STOCK"])
app.include_router(serial_and_batch_bundle_router, prefix="/v1/serial-and-batch-bundle", tags=["STOCK"])
app.include_router(serial_and_batch_entry_router, prefix="/v1/serial-and-batch-entry", tags=["STOCK"])
app.include_router(serial_no_router, prefix="/v1/serial-no", tags=["STOCK"])
app.include_router(shipment_router, prefix="/v1/shipment", tags=["STOCK"])
app.include_router(shipment_delivery_note_router, prefix="/v1/shipment-delivery-note", tags=["STOCK"])
app.include_router(shipment_parcel_router, prefix="/v1/shipment-parcel", tags=["STOCK"])
app.include_router(shipment_parcel_template_router, prefix="/v1/shipment-parcel-template", tags=["STOCK"])
app.include_router(stock_closing_balance_router, prefix="/v1/stock-closing-balance", tags=["STOCK"])
app.include_router(stock_closing_entry_router, prefix="/v1/stock-closing-entry", tags=["STOCK"])
app.include_router(stock_entry_router, prefix="/v1/stock-entry", tags=["STOCK"])
app.include_router(stock_entry_detail_router, prefix="/v1/stock-entry-detail", tags=["STOCK"])
app.include_router(stock_entry_type_router, prefix="/v1/stock-entry-type", tags=["STOCK"])
app.include_router(stock_ledger_entry_router, prefix="/v1/stock-ledger-entry", tags=["STOCK"])
app.include_router(stock_reconciliation_router, prefix="/v1/stock-reconciliation", tags=["STOCK"])
app.include_router(stock_reconciliation_item_router, prefix="/v1/stock-reconciliation-item", tags=["STOCK"])
app.include_router(stock_reposting_settings_router, prefix="/v1/stock-reposting-settings", tags=["STOCK"])
app.include_router(stock_reservation_entry_router, prefix="/v1/stock-reservation-entry", tags=["STOCK"])
app.include_router(stock_settings_router, prefix="/v1/stock-settings", tags=["STOCK"])
app.include_router(uom_router, prefix="/v1/uom", tags=["STOCK"])
app.include_router(uom_category_router, prefix="/v1/uom-category", tags=["STOCK"])
app.include_router(uom_conversion_detail_router, prefix="/v1/uom-conversion-detail", tags=["STOCK"])
app.include_router(variant_field_router, prefix="/v1/variant-field", tags=["STOCK"])
app.include_router(warehouse_router, prefix="/v1/warehouse", tags=["STOCK"])
app.include_router(warehouse_type_router, prefix="/v1/warehouse-type", tags=["STOCK"])
app.include_router(buying_settings_router, prefix="/api/buying/buying-settings", tags=["BUYING"])
app.include_router(customer_number_at_supplier_router, prefix="/api/buying/customer-number-at-supplier", tags=["BUYING"])
app.include_router(purchase_order_router, prefix="/api/buying/purchase-order", tags=["BUYING"])
app.include_router(purchase_order_item_router, prefix="/api/buying/purchase-order-item", tags=["BUYING"])
app.include_router(purchase_receipt_item_supplied_router, prefix="/api/buying/purchase-receipt-item-supplied", tags=["BUYING"])
app.include_router(request_for_quotation_router, prefix="/api/buying/request-for-quotation", tags=["BUYING"])
app.include_router(request_for_quotation_item_router, prefix="/api/buying/request-for-quotation-item", tags=["BUYING"])
app.include_router(request_for_quotation_supplier_router, prefix="/api/buying/request-for-quotation-supplier", tags=["BUYING"])
app.include_router(supplier_router, prefix="/api/buying/supplier", tags=["BUYING"])
app.include_router(supplier_quotation_router, prefix="/api/buying/supplier-quotation", tags=["BUYING"])
app.include_router(supplier_quotation_item_router, prefix="/api/buying/supplier-quotation-item", tags=["BUYING"])
app.include_router(supplier_scorecard_router, prefix="/api/buying/supplier-scorecard", tags=["BUYING"])
app.include_router(supplier_scorecard_criteria_router, prefix="/api/buying/supplier-scorecard-criteria", tags=["BUYING"])
app.include_router(supplier_scorecard_period_router, prefix="/api/buying/supplier-scorecard-period", tags=["BUYING"])
app.include_router(supplier_scorecard_scoring_criteria_router, prefix="/api/buying/supplier-scorecard-scoring-criteria", tags=["BUYING"])
app.include_router(supplier_scorecard_scoring_standing_router, prefix="/api/buying/supplier-scorecard-scoring-standing", tags=["BUYING"])
app.include_router(supplier_scorecard_scoring_variable_router, prefix="/api/buying/supplier-scorecard-scoring-variable", tags=["BUYING"])
app.include_router(supplier_scorecard_standing_router, prefix="/api/buying/supplier-scorecard-standing", tags=["BUYING"])
app.include_router(supplier_scorecard_variable_router, prefix="/api/buying/supplier-scorecard-variable", tags=["BUYING"])
app.include_router(erpnext_customer_router, prefix="/api/selling/customer", tags=["SELLING"])
app.include_router(customer_credit_limit_router, prefix="/api/selling/customer-credit-limit", tags=["SELLING"])
app.include_router(delivery_schedule_item_router, prefix="/api/selling/delivery-schedule-item", tags=["SELLING"])
app.include_router(industry_type_router, prefix="/api/selling/industry-type", tags=["SELLING"])
app.include_router(installation_note_router, prefix="/api/selling/installation-note", tags=["SELLING"])
app.include_router(installation_note_item_router, prefix="/api/selling/installation-note-item", tags=["SELLING"])
app.include_router(party_specific_item_router, prefix="/api/selling/party-specific-item", tags=["SELLING"])
app.include_router(product_bundle_router, prefix="/api/selling/product-bundle", tags=["SELLING"])
app.include_router(product_bundle_item_router, prefix="/api/selling/product-bundle-item", tags=["SELLING"])
app.include_router(proforma_invoice_router, prefix="/api/selling/proforma-invoice", tags=["SELLING"])
app.include_router(proforma_invoice_item_router, prefix="/api/selling/proforma-invoice-item", tags=["SELLING"])
app.include_router(quotation_router, prefix="/api/selling/quotation", tags=["SELLING"])
app.include_router(quotation_item_router, prefix="/api/selling/quotation-item", tags=["SELLING"])
app.include_router(sales_order_router, prefix="/api/selling/sales-order", tags=["SELLING"])
app.include_router(sales_order_item_router, prefix="/api/selling/sales-order-item", tags=["SELLING"])
app.include_router(sales_partner_type_router, prefix="/api/selling/sales-partner-type", tags=["SELLING"])
app.include_router(sales_team_router, prefix="/api/selling/sales-team", tags=["SELLING"])
app.include_router(selling_settings_router, prefix="/api/selling/selling-settings", tags=["SELLING"])
app.include_router(sms_center_router, prefix="/api/selling/sms-center", tags=["SELLING"])
app.include_router(supplier_number_at_customer_router, prefix="/api/selling/supplier-number-at-customer", tags=["SELLING"])
app.include_router(blanket_order_router, prefix="/api/manufacturing/blanket-order", tags=["MANUFACTURING"])
app.include_router(blanket_order_item_router, prefix="/api/manufacturing/blanket-order-item", tags=["MANUFACTURING"])
app.include_router(bom_router, prefix="/api/manufacturing/bom", tags=["MANUFACTURING"])
app.include_router(bom_creator_router, prefix="/api/manufacturing/bom-creator", tags=["MANUFACTURING"])
app.include_router(bom_creator_item_router, prefix="/api/manufacturing/bom-creator-item", tags=["MANUFACTURING"])
app.include_router(bom_explosion_item_router, prefix="/api/manufacturing/bom-explosion-item", tags=["MANUFACTURING"])
app.include_router(bom_item_router, prefix="/api/manufacturing/bom-item", tags=["MANUFACTURING"])
app.include_router(bom_operation_router, prefix="/api/manufacturing/bom-operation", tags=["MANUFACTURING"])
app.include_router(bom_secondary_item_router, prefix="/api/manufacturing/bom-secondary-item", tags=["MANUFACTURING"])
app.include_router(bom_update_batch_router, prefix="/api/manufacturing/bom-update-batch", tags=["MANUFACTURING"])
app.include_router(bom_update_log_router, prefix="/api/manufacturing/bom-update-log", tags=["MANUFACTURING"])
app.include_router(bom_update_tool_router, prefix="/api/manufacturing/bom-update-tool", tags=["MANUFACTURING"])
app.include_router(bom_website_item_router, prefix="/api/manufacturing/bom-website-item", tags=["MANUFACTURING"])
app.include_router(bom_website_operation_router, prefix="/api/manufacturing/bom-website-operation", tags=["MANUFACTURING"])
app.include_router(downtime_entry_router, prefix="/api/manufacturing/downtime-entry", tags=["MANUFACTURING"])
app.include_router(job_card_router, prefix="/api/manufacturing/job-card", tags=["MANUFACTURING"])
app.include_router(job_card_item_router, prefix="/api/manufacturing/job-card-item", tags=["MANUFACTURING"])
app.include_router(job_card_operation_router, prefix="/api/manufacturing/job-card-operation", tags=["MANUFACTURING"])
app.include_router(job_card_scheduled_time_router, prefix="/api/manufacturing/job-card-scheduled-time", tags=["MANUFACTURING"])
app.include_router(job_card_secondary_item_router, prefix="/api/manufacturing/job-card-secondary-item", tags=["MANUFACTURING"])
app.include_router(job_card_time_log_router, prefix="/api/manufacturing/job-card-time-log", tags=["MANUFACTURING"])
app.include_router(manufacturing_settings_router, prefix="/api/manufacturing/manufacturing-settings", tags=["MANUFACTURING"])
app.include_router(master_production_schedule_router, prefix="/api/manufacturing/master-production-schedule", tags=["MANUFACTURING"])
app.include_router(master_production_schedule_item_router, prefix="/api/manufacturing/master-production-schedule-item", tags=["MANUFACTURING"])
app.include_router(material_request_plan_item_router, prefix="/api/manufacturing/material-request-plan-item", tags=["MANUFACTURING"])
app.include_router(operation_router, prefix="/api/manufacturing/operation", tags=["MANUFACTURING"])
app.include_router(plant_floor_router, prefix="/api/manufacturing/plant-floor", tags=["MANUFACTURING"])
app.include_router(production_plan_router, prefix="/api/manufacturing/production-plan", tags=["MANUFACTURING"])
app.include_router(production_plan_item_router, prefix="/api/manufacturing/production-plan-item", tags=["MANUFACTURING"])
app.include_router(production_plan_item_reference_router, prefix="/api/manufacturing/production-plan-item-reference", tags=["MANUFACTURING"])
app.include_router(production_plan_material_request_router, prefix="/api/manufacturing/production-plan-material-request", tags=["MANUFACTURING"])
app.include_router(production_plan_material_request_warehouse_router, prefix="/api/manufacturing/production-plan-material-request-warehouse", tags=["MANUFACTURING"])
app.include_router(production_plan_sales_order_router, prefix="/api/manufacturing/production-plan-sales-order", tags=["MANUFACTURING"])
app.include_router(production_plan_sub_assembly_item_router, prefix="/api/manufacturing/production-plan-sub-assembly-item", tags=["MANUFACTURING"])
app.include_router(routing_router, prefix="/api/manufacturing/routing", tags=["MANUFACTURING"])
app.include_router(sales_forecast_router, prefix="/api/manufacturing/sales-forecast", tags=["MANUFACTURING"])
app.include_router(sales_forecast_item_router, prefix="/api/manufacturing/sales-forecast-item", tags=["MANUFACTURING"])
app.include_router(sub_operation_router, prefix="/api/manufacturing/sub-operation", tags=["MANUFACTURING"])
app.include_router(work_order_router, prefix="/api/manufacturing/work-order", tags=["MANUFACTURING"])
app.include_router(work_order_additional_item_router, prefix="/api/manufacturing/work-order-additional-item", tags=["MANUFACTURING"])
app.include_router(work_order_item_router, prefix="/api/manufacturing/work-order-item", tags=["MANUFACTURING"])
app.include_router(work_order_operation_router, prefix="/api/manufacturing/work-order-operation", tags=["MANUFACTURING"])
app.include_router(workstation_router, prefix="/api/manufacturing/workstation", tags=["MANUFACTURING"])
app.include_router(workstation_cost_router, prefix="/api/manufacturing/workstation-cost", tags=["MANUFACTURING"])
app.include_router(workstation_operating_component_router, prefix="/api/manufacturing/workstation-operating-component", tags=["MANUFACTURING"])
app.include_router(workstation_operating_component_account_router, prefix="/api/manufacturing/workstation-operating-component-account", tags=["MANUFACTURING"])
app.include_router(workstation_type_router, prefix="/api/manufacturing/workstation-type", tags=["MANUFACTURING"])
app.include_router(workstation_working_hour_router, prefix="/api/manufacturing/workstation-working-hour", tags=["MANUFACTURING"])

@app.on_event("startup")
async def startup():
    logger.info("[Startup] MSME Platform starting...")
    try:
        if os.getenv("ENABLE_REDIS_STREAM", "false").lower() == "true":
            await retry_pending_events()
            asyncio.create_task(EventStreamConsumer().start())
            logger.info("[Startup] Event stream consumer started ✓")
        else:
            logger.info("[Startup] Event stream skipped (ENABLE_REDIS_STREAM=false)")
    except Exception as e:
        logger.warning(f"[Startup] Redis background event stream skipped: {e}")

@app.on_event("shutdown")
async def shutdown():
    logger.info("[Shutdown] MSME Platform shutting down...")

@app.get("/health")
def health():
    return {"status": "ok", "service": "msme-platform", "erpnext_modules": {"accounts": 191, "stock": 80, "buying": 19, "selling": 20, "manufacturing": 48, "total": 358, "msme_core": 15, "grand_total": 373}}
