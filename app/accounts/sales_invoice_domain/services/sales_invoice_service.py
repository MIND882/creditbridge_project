# HAND-WRITTEN

"""

Business logic for Sales Invoice -- port of

``erpnext/accounts/doctype/sales_invoice/sales_invoice.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream hooks:

    set_indicator

    onload

    validate

    validate_update_stock_for_pick_list_reference

    validate_accounts

    validate_for_repost

    validate_item_cost_centers

    validate_income_account

    before_save

    before_submit

    on_submit

    before_cancel

    on_cancel

    update_status_updater_args

    check_credit_limit

    check_overdue_billing_threshold

    set_missing_values

    set_pos_fields

    refresh_subscription_status

    reset_mode_of_payments

    set_account_for_mode_of_payment

    validate_pos

    validate_pos_opening_entry

    clear_unallocated_mode_of_payments

    validate_full_payment

    get_company_abbr

    validate_debit_to_acc

    validate_with_previous_doc

    set_against_income_account

    force_set_against_income_account

    add_remarks

    validate_auto_set_posting_time

    so_dn_required

    validate_proj_cust

    validate_warehouse

    validate_delivery_note

    validate_subcontracted_sales_order

    validate_scio_self_rm_qty

    validate_write_off_account

    validate_account_for_change_amount

    validate_debit_note_with_update_stock

    validate_dropship_item

    update_current_stock

    update_packing_list

    is_auto_fetch_timesheet_enabled

    add_timesheet_data

    check_prev_docstatus

    make_gl_entries

    get_gl_entries

    enable_discount_accounting

    update_billing_status_in_dn

    on_recurring

    update_project

    update_billed_qty_in_scio

    on_update_after_submit

    set_status

    is_subcontracted



**Upstream has 14 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import datetime as dt

import uuid

from decimal import Decimal

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.account_domain.models.account import Account

from app.accounts.sales_invoice_domain.models.sales_invoice import (

    SalesInvoice,

    SalesInvoiceIsOpening,

)

from app.accounts.pricing_rule_detail_domain.models.pricing_rule_detail import PricingRuleDetail

from app.accounts.sales_invoice_timesheet_domain.models.sales_invoice_timesheet import SalesInvoiceTimesheet

from app.accounts.sales_invoice_advance_domain.models.sales_invoice_advance import SalesInvoiceAdvance

from app.accounts.cashier_closing_payments_domain.models.cashier_closing_payments import CashierClosingPayments

from app.accounts.tax_withholding_entry_domain.models.tax_withholding_entry import TaxWithholdingEntry

from app.accounts.sales_invoice_domain.repositories.sales_invoice_repository import (

    SalesInvoiceRepository,

)

from app.accounts.sales_invoice_domain.schemas.sales_invoice import (

    SalesInvoiceCreate,

    SalesInvoiceUpdate,

)

from app.accounts.sales_invoice_item_domain.models.sales_invoice_item import SalesInvoiceItem  # noqa: F401

from app.accounts.fiscal_year_domain.services.fiscal_year_service import (

    FiscalYearService,

)

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SalesInvoiceService"]





class SalesInvoiceService:

    def __init__(self, repository: Optional[SalesInvoiceRepository] = None) -> None:

        # The fiscal-year lookup is a cross-domain read, so the service is

        # held rather than re-resolving it on every validation pass.

        self._fiscal_years = FiscalYearService()

        self.repository = repository or SalesInvoiceRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SalesInvoice:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Sales Invoice", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: SalesInvoice, *, is_new: bool

    ) -> None:

        """

        Port of upstream ``validate``. Upstream order is preserved where the

        rules were ported; see ``_UNPORTED`` for what is missing and why.

        """

        # accounts_controller.validate_date_with_fiscal_year

        self._validate_date_with_fiscal_year(db, business_id, row)

        # accounts_controller.validate_qty_is_not_zero

        self._validate_qty_is_not_zero(row)

        self._validate_debit_to_acc(db, business_id, row)

        # accounts_controller.check_conversion_rate

        self._check_conversion_rate(row)



        # validate: ``if not self.is_opening: self.is_opening = "No"``

        if not row.is_opening:

            row.is_opening = SalesInvoiceIsOpening.NO



        # validate: ``if self.is_return and not self.return_against and

        # self.timesheets: frappe.throw("Direct return is not allowed for

        # Timesheet.")``

        if row.is_return and not row.return_against and row.timesheets:

            raise DomainValidationError(

                "Direct return is not allowed for Timesheet.",

                code="sales_invoice_direct_timesheet_return",

                details={"return_against": None},

            )



        # TODO(PORT-VALIDATION): the remaining upstream rules are NOT ported.

        # They read Stock or Selling state, neither of which is converted:

        #

        #   so_dn_required              -- "Sales Order or Delivery Note

        #                                  required" unless POS/return/debit

        #                                  note; reads Sales Order and Delivery

        #                                  Note docstatus.

        #   validate_with_previous_doc  -- billed/returned qty against Sales

        #                                  Order and Delivery Note.

        #   validate_warehouse /

        #   update_current_stock        -- "Warehouse required for stock Item",

        #                                  batch and serial validation, actual

        #                                  stock levels.

        #   validate_pos /

        #   validate_created_using_pos  -- POS Profile, POS Opening Entry, full

        #                                  payment coverage.

        #   validate_delivery_note,

        #   validate_subcontracted_*,

        #   validate_dropship_item      -- all Sales Order / stock coupled.

        #   validate_item_cost_centers,

        #   validate_accounts,

        #   set_against_income_account  -- need the tax and totals engine

        #                                  (erpnext.accounts.services.taxes).

        #   deferred revenue, loyalty,

        #   coupon, inter-company       -- need Selling, Stock and CRM.

        #

        # These fail open. A Sales Invoice that upstream would reject for a

        # missing warehouse, an over-billed Sales Order or an unsubmitted POS

        # entry is accepted here.

        return None



    # ── validate_date_with_fiscal_year (accounts_controller) ──────────────

    def _validate_date_with_fiscal_year(

        self, db: Session, business_id: uuid.UUID, row: SalesInvoice

    ) -> None:

        """

        The posting date must fall inside an enabled fiscal year.



        Upstream has two branches: when the doctype carries a ``fiscal_year``

        field it calls ``validate_fiscal_year``, which silently reassigns the

        field when the date disagrees; otherwise it calls ``get_fiscal_year``,

        which raises ``FiscalYearError`` when nothing covers the date.



        Neither invoice has a ``fiscal_year`` column, so the second branch

        applies and the failure is a hard 400.

        """

        if not row.posting_date:

            return

        if self._fiscal_years.get_for_date(db, business_id, row.posting_date) is None:

            raise DomainValidationError(

                f"Posting Date {row.posting_date.isoformat()} is not in any "

                f"active Fiscal Year",

                code="sales_invoice_not_in_fiscal_year",

                details={"posting_date": row.posting_date.isoformat()},

            )



    # ── check_conversion_rate (accounts_controller) ───────────────────────

    def _check_conversion_rate(self, row: SalesInvoice) -> None:

        """

        ``if not self.conversion_rate: throw("Conversion rate cannot be 0")``.



        Upstream then compares the document currency against the company's

        default currency and throws "Conversion rate must be 1.00 if document

        currency is same as company currency", plus a msgprint for the inverse

        case. Those two branches are NOT ported: ``Company`` is not converted,

        the tenant is ``business_id``, and it carries no company currency to

        compare against. Guessing one would be worse than skipping the check.

        """

        if not Decimal(str(row.conversion_rate or 0)):

            raise DomainValidationError(

                "Conversion rate cannot be 0",

                code="sales_invoice_zero_conversion_rate",

                details={"conversion_rate": str(row.conversion_rate)},

            )



    # ── validate_qty_is_not_zero (accounts_controller) ────────────────────

    def _validate_qty_is_not_zero(self, row: SalesInvoice) -> None:

        """

        Upstream skips this when ``is_return`` or ``is_debit_note``: a credit

        note legitimately carries no quantity.

        """

        # accounts_controller reads ``self.get("is_debit_note")``; that

        # field exists on Sales Invoice but not on Purchase Invoice, so

        # getattr keeps this faithful for both.

        if row.is_return or getattr(row, "is_debit_note", False):

            return

        for item in row.items:

            if not Decimal(str(item.qty or 0)):

                raise DomainValidationError(

                    f"Row #{item.idx}: Quantity for Item {item.item_name or item.item_code} "

                    f"cannot be zero.",

                    code="sales_invoice_zero_qty",

                    details={"idx": item.idx, "item": item.item_name},

                )



    # ── validate_debit_to_acc ─────────────────────────────────────────────

    def _validate_debit_to_acc(

        self, db: Session, business_id: uuid.UUID, row: SalesInvoice

    ) -> None:

        """

        The receivable account an invoice is booked to. Three upstream throws:

        missing account, wrong report type, and wrong account type when a

        customer is set.



        Upstream first falls back to the party's default account via

        ``get_party_account``. That reads the Customer doctype's

        ``accounts`` child table; Customer is not converted, so there is no

        fallback here and a blank Debit To is simply an error.

        """

        if not row.debit_to_id:

            raise DomainValidationError(

                "Debit To is required",

                code="sales_invoice_debit_to_required",

                details={"debit_to_id": None},

            )



        account = db.scalar(

            select(Account).where(

                Account.id == row.debit_to_id, Account.business_id == business_id

            )

        )

        if account is None:

            raise DomainValidationError(

                "Debit To is required",

                code="sales_invoice_debit_to_required",

                details={"debit_to_id": str(row.debit_to_id)},

            )



        report_type = getattr(account.report_type, "value", account.report_type)

        if report_type != "Balance Sheet":

            raise DomainValidationError(

                "Please ensure Debit To account is a Balance Sheet account. You "

                "can change the parent account to a Balance Sheet account or "

                "select a different account.",

                code="sales_invoice_debit_to_not_balance_sheet",

                details={"account": account.name, "report_type": str(report_type)},

            )



        if row.customer:

            account_type = getattr(account.account_type, "value", account.account_type)

            if account_type != "Receivable":

                raise DomainValidationError(

                    f"Please ensure Debit To account {account.name} is a "

                    f"Receivable account. Change the account type to Receivable "

                    f"or select a different account.",

                    code="sales_invoice_debit_to_not_receivable",

                    details={"account": account.name, "account_type": str(account_type)},

                )



        # ``self.party_account_currency = account.account_currency``. The

        # converted Account has no account_currency column, so the invoice

        # currency is the only available source.

        if not row.party_account_currency:

            row.party_account_currency = row.currency



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SalesInvoice:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[SalesInvoice]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SalesInvoice].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_items(

        self, business_id: uuid.UUID, row: SalesInvoice, items: list[dict]

    ) -> None:

        row.items.clear()

        for idx, item in enumerate(items, start=1):

            row.items.append(

                SalesInvoiceItem(

                    business_id=business_id,

                    idx=idx,

                    name=item.get('name'),

                    barcode=item.get('barcode'),

                    item_code=item.get('item_code'),

                    is_product_bundle=item.get('is_product_bundle'),

                    product_bundle=item.get('product_bundle'),

                    item_name=item.get('item_name'),

                    customer_item_code=item.get('customer_item_code'),

                    description=item.get('description'),

                    image_view=item.get('image_view'),

                    image=item.get('image'),

                    qty=item.get('qty'),

                    stock_uom=item.get('stock_uom'),

                    uom=item.get('uom'),

                    conversion_factor=item.get('conversion_factor'),

                    stock_qty=item.get('stock_qty'),

                    price_list_rate=item.get('price_list_rate'),

                    base_price_list_rate=item.get('base_price_list_rate'),

                    margin_type=item.get('margin_type'),

                    margin_rate_or_amount=item.get('margin_rate_or_amount'),

                    rate_with_margin=item.get('rate_with_margin'),

                    discount_percentage=item.get('discount_percentage'),

                    discount_amount=item.get('discount_amount'),

                    base_rate_with_margin=item.get('base_rate_with_margin'),

                    rate=item.get('rate'),

                    amount=item.get('amount'),

                    base_rate=item.get('base_rate'),

                    base_amount=item.get('base_amount'),

                    pricing_rules=item.get('pricing_rules'),

                    is_free_item=item.get('is_free_item'),

                    net_rate=item.get('net_rate'),

                    net_amount=item.get('net_amount'),

                    base_net_rate=item.get('base_net_rate'),

                    base_net_amount=item.get('base_net_amount'),

                    delivered_by_supplier=item.get('delivered_by_supplier'),

                    income_account_id=item.get('income_account_id'),

                    expense_account_id=item.get('expense_account_id'),

                    item_tax_template_id=item.get('item_tax_template_id'),

                    cost_center_id=item.get('cost_center_id'),

                    deferred_revenue_account_id=item.get('deferred_revenue_account_id'),

                    service_stop_date=item.get('service_stop_date'),

                    enable_deferred_revenue=item.get('enable_deferred_revenue'),

                    service_start_date=item.get('service_start_date'),

                    service_end_date=item.get('service_end_date'),

                    weight_per_unit=item.get('weight_per_unit'),

                    total_weight=item.get('total_weight'),

                    weight_uom=item.get('weight_uom'),

                    warehouse=item.get('warehouse'),

                    target_warehouse=item.get('target_warehouse'),

                    quality_inspection=item.get('quality_inspection'),

                    batch_no=item.get('batch_no'),

                    allow_zero_valuation_rate=item.get('allow_zero_valuation_rate'),

                    serial_no=item.get('serial_no'),

                    item_group=item.get('item_group'),

                    brand=item.get('brand'),

                    item_tax_rate=item.get('item_tax_rate'),

                    actual_batch_qty=item.get('actual_batch_qty'),

                    actual_qty=item.get('actual_qty'),

                    sales_order=item.get('sales_order'),

                    so_detail=item.get('so_detail'),

                    delivery_note=item.get('delivery_note'),

                    dn_detail=item.get('dn_detail'),

                    delivered_qty=item.get('delivered_qty'),

                    is_fixed_asset=item.get('is_fixed_asset'),

                    asset=item.get('asset'),

                    page_break=item.get('page_break'),

                    finance_book_id=item.get('finance_book_id'),

                    project=item.get('project'),

                    sales_invoice_item=item.get('sales_invoice_item'),

                    incoming_rate=item.get('incoming_rate'),

                    stock_uom_rate=item.get('stock_uom_rate'),

                    discount_account_id=item.get('discount_account_id'),

                    grant_commission=item.get('grant_commission'),

                    purchase_order=item.get('purchase_order'),

                    purchase_order_item=item.get('purchase_order_item'),

                    has_item_scanned=item.get('has_item_scanned'),

                    serial_and_batch_bundle=item.get('serial_and_batch_bundle'),

                    use_serial_batch_fields=item.get('use_serial_batch_fields'),

                    distributed_discount_amount=item.get('distributed_discount_amount'),

                    company_total_stock=item.get('company_total_stock'),

                    pos_invoice_item=item.get('pos_invoice_item'),

                    pos_invoice=item.get('pos_invoice'),

                    scio_detail=item.get('scio_detail'),

                    tax_withholding_category_id=item.get('tax_withholding_category_id'),

                    apply_tds=item.get('apply_tds'),

                    against_pick_list=item.get('against_pick_list'),

                    pick_list_item=item.get('pick_list_item'),

                )

            )



    def _replace_pricing_rules(

        self, business_id: uuid.UUID, row: SalesInvoice, items: list[dict]

    ) -> None:

        row.pricing_rules.clear()

        for idx, item in enumerate(items, start=1):

            row.pricing_rules.append(

                PricingRuleDetail(

                    business_id=business_id,

                    idx=idx,

                    parenttype='Sales Invoice',

                    pricing_rule=item.get('pricing_rule'),

                    item_code=item.get('item_code'),

                    margin_type=item.get('margin_type'),

                    rate_or_discount=item.get('rate_or_discount'),

                    child_docname=item.get('child_docname'),

                    rule_applied=item.get('rule_applied'),

                )

            )



    def _replace_timesheets(

        self, business_id: uuid.UUID, row: SalesInvoice, items: list[dict]

    ) -> None:

        row.timesheets.clear()

        for idx, item in enumerate(items, start=1):

            row.timesheets.append(

                SalesInvoiceTimesheet(

                    business_id=business_id,

                    idx=idx,

                    parenttype='Sales Invoice',

                    time_sheet=item.get('time_sheet'),

                    billing_hours=item.get('billing_hours'),

                    billing_amount=item.get('billing_amount'),

                    timesheet_detail=item.get('timesheet_detail'),

                    activity_type=item.get('activity_type'),

                    description=item.get('description'),

                    from_time=item.get('from_time'),

                    to_time=item.get('to_time'),

                    project_name=item.get('project_name'),

                )

            )



    def _replace_advances(

        self, business_id: uuid.UUID, row: SalesInvoice, items: list[dict]

    ) -> None:

        row.advances.clear()

        for idx, item in enumerate(items, start=1):

            row.advances.append(

                SalesInvoiceAdvance(

                    business_id=business_id,

                    idx=idx,

                    parenttype='Sales Invoice',

                    reference_type=item.get('reference_type'),

                    reference_name=item.get('reference_name'),

                    remarks=item.get('remarks'),

                    reference_row=item.get('reference_row'),

                    advance_amount=item.get('advance_amount'),

                    allocated_amount=item.get('allocated_amount'),

                    exchange_gain_loss=item.get('exchange_gain_loss'),

                    ref_exchange_rate=item.get('ref_exchange_rate'),

                    difference_posting_date=item.get('difference_posting_date'),

                )

            )



    def _replace_payments(

        self, business_id: uuid.UUID, row: SalesInvoice, items: list[dict]

    ) -> None:

        row.payments.clear()

        for idx, item in enumerate(items, start=1):

            row.payments.append(

                CashierClosingPayments(

                    business_id=business_id,

                    idx=idx,

                    mode_of_payment_id=item.get('mode_of_payment_id'),

                    amount=item.get('amount'),

                )

            )



    def _replace_tax_withholding_entries(

        self, business_id: uuid.UUID, row: SalesInvoice, items: list[dict]

    ) -> None:

        row.tax_withholding_entries.clear()

        for idx, item in enumerate(items, start=1):

            row.tax_withholding_entries.append(

                TaxWithholdingEntry(

                    business_id=business_id,

                    idx=idx,

                    parenttype='Sales Invoice',

                    party_type=item.get('party_type'),

                    party=item.get('party'),

                    tax_id=item.get('tax_id'),

                    tax_withholding_category_id=item.get('tax_withholding_category_id'),

                    tax_rate=item.get('tax_rate'),

                    taxable_amount=item.get('taxable_amount'),

                    lower_deduction_certificate=item.get('lower_deduction_certificate'),

                    status=item.get('status'),

                    currency=item.get('currency'),

                    conversion_rate=item.get('conversion_rate'),

                    withholding_doctype=item.get('withholding_doctype'),

                    withholding_name=item.get('withholding_name'),

                    taxable_doctype=item.get('taxable_doctype'),

                    taxable_name=item.get('taxable_name'),

                    taxable_date=item.get('taxable_date'),

                    withholding_date=item.get('withholding_date'),

                    under_withheld_reason=item.get('under_withheld_reason'),

                    withholding_amount=item.get('withholding_amount'),

                    tax_withholding_group_id=item.get('tax_withholding_group_id'),

                    created_by_migration=item.get('created_by_migration'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(SalesInvoice).where(

                    SalesInvoice.business_id == business_id

                )

            )

            or 0

        )

        year = dt.date.today().year

        return f"ACC-SINV-{year}-{count + 1:08d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: SalesInvoiceCreate

    ) -> SalesInvoice:

        row = SalesInvoice(

            business_id=business_id,

            name=self.next_name(db, business_id),

            naming_series=payload.naming_series,

            customer=payload.customer,

            customer_name=payload.customer_name,

            project=payload.project,

            is_pos=payload.is_pos,

            pos_profile=payload.pos_profile,

            is_return=payload.is_return,

            cost_center_id=payload.cost_center_id,

            posting_date=payload.posting_date,

            posting_time=payload.posting_time,

            set_posting_time=payload.set_posting_time,

            due_date=payload.due_date,

            amended_from=payload.amended_from,

            return_against=payload.return_against,

            update_billed_amount_in_sales_order=payload.update_billed_amount_in_sales_order,

            po_no=payload.po_no,

            po_date=payload.po_date,

            customer_address=payload.customer_address,

            address_display=payload.address_display,

            contact_person=payload.contact_person,

            contact_display=payload.contact_display,

            contact_mobile=payload.contact_mobile,

            contact_email=payload.contact_email,

            territory=payload.territory,

            shipping_address_name=payload.shipping_address_name,

            shipping_address=payload.shipping_address,

            company_address=payload.company_address,

            company_address_display=payload.company_address_display,

            currency=payload.currency,

            conversion_rate=payload.conversion_rate,

            selling_price_list=payload.selling_price_list,

            price_list_currency=payload.price_list_currency,

            plc_conversion_rate=payload.plc_conversion_rate,

            ignore_pricing_rule=payload.ignore_pricing_rule,

            set_warehouse=payload.set_warehouse,

            update_stock=payload.update_stock,

            scan_barcode=payload.scan_barcode,

            total_billing_amount=payload.total_billing_amount,

            total_qty=payload.total_qty,

            base_total=payload.base_total,

            base_net_total=payload.base_net_total,

            total=payload.total,

            net_total=payload.net_total,

            total_net_weight=payload.total_net_weight,

            taxes_and_charges=payload.taxes_and_charges,

            shipping_rule=payload.shipping_rule,

            tax_category_id=payload.tax_category_id,

            other_charges_calculation=payload.other_charges_calculation,

            base_total_taxes_and_charges=payload.base_total_taxes_and_charges,

            total_taxes_and_charges=payload.total_taxes_and_charges,

            loyalty_points=payload.loyalty_points,

            loyalty_amount=payload.loyalty_amount,

            redeem_loyalty_points=payload.redeem_loyalty_points,

            loyalty_program=payload.loyalty_program,

            loyalty_redemption_account_id=payload.loyalty_redemption_account_id,

            loyalty_redemption_cost_center_id=payload.loyalty_redemption_cost_center_id,

            apply_discount_on=payload.apply_discount_on,

            base_discount_amount=payload.base_discount_amount,

            additional_discount_percentage=payload.additional_discount_percentage,

            discount_amount=payload.discount_amount,

            base_grand_total=payload.base_grand_total,

            base_rounding_adjustment=payload.base_rounding_adjustment,

            base_rounded_total=payload.base_rounded_total,

            base_in_words=payload.base_in_words,

            grand_total=payload.grand_total,

            rounding_adjustment=payload.rounding_adjustment,

            rounded_total=payload.rounded_total,

            in_words=payload.in_words,

            total_advance=payload.total_advance,

            outstanding_amount=payload.outstanding_amount,

            allocate_advances_automatically=payload.allocate_advances_automatically,

            payment_terms_template_id=payload.payment_terms_template_id,

            cash_bank_account_id=payload.cash_bank_account_id,

            base_paid_amount=payload.base_paid_amount,

            paid_amount=payload.paid_amount,

            base_change_amount=payload.base_change_amount,

            change_amount=payload.change_amount,

            account_for_change_amount_id=payload.account_for_change_amount_id,

            write_off_amount=payload.write_off_amount,

            base_write_off_amount=payload.base_write_off_amount,

            write_off_outstanding_amount_automatically=payload.write_off_outstanding_amount_automatically,

            write_off_account_id=payload.write_off_account_id,

            write_off_cost_center_id=payload.write_off_cost_center_id,

            tc_name=payload.tc_name,

            terms=payload.terms,

            letter_head=payload.letter_head,

            group_same_items=payload.group_same_items,

            language=payload.language,

            select_print_heading=payload.select_print_heading,

            inter_company_invoice_reference=payload.inter_company_invoice_reference,

            customer_group=payload.customer_group,

            is_discounted=payload.is_discounted,

            status=payload.status,

            debit_to_id=payload.debit_to_id,

            party_account_currency=payload.party_account_currency,

            is_opening=payload.is_opening,

            remarks=payload.remarks,

            sales_partner=payload.sales_partner,

            commission_rate=payload.commission_rate,

            total_commission=payload.total_commission,

            from_date=payload.from_date,

            to_date=payload.to_date,

            auto_repeat=payload.auto_repeat,

            against_income_account=payload.against_income_account,

            is_consolidated=payload.is_consolidated,

            is_internal_customer=payload.is_internal_customer,

            unrealized_profit_loss_account_id=payload.unrealized_profit_loss_account_id,

            set_target_warehouse=payload.set_target_warehouse,

            is_debit_note=payload.is_debit_note,

            disable_rounded_total=payload.disable_rounded_total,

            additional_discount_account_id=payload.additional_discount_account_id,

            dispatch_address_name=payload.dispatch_address_name,

            dispatch_address=payload.dispatch_address,

            ignore_default_payment_terms_template=payload.ignore_default_payment_terms_template,

            total_billing_hours=payload.total_billing_hours,

            amount_eligible_for_commission=payload.amount_eligible_for_commission,

            subscription=payload.subscription,

            is_cash_or_non_trade_discount=payload.is_cash_or_non_trade_discount,

            incoterm=payload.incoterm,

            named_place=payload.named_place,

            only_include_allocated_payments=payload.only_include_allocated_payments,

            use_company_roundoff_cost_center=payload.use_company_roundoff_cost_center,

            update_billed_amount_in_delivery_note=payload.update_billed_amount_in_delivery_note,

            dont_create_loyalty_points=payload.dont_create_loyalty_points,

            coupon_code=payload.coupon_code,

            update_outstanding_for_self=payload.update_outstanding_for_self,

            utm_medium=payload.utm_medium,

            utm_content=payload.utm_content,

            utm_campaign=payload.utm_campaign,

            utm_source=payload.utm_source,

            company_contact_person=payload.company_contact_person,

            is_created_using_pos=payload.is_created_using_pos,

            pos_closing_entry=payload.pos_closing_entry,

            last_scanned_warehouse=payload.last_scanned_warehouse,

            has_subcontracted=payload.has_subcontracted,

            apply_tds=payload.apply_tds,

            tax_withholding_group_id=payload.tax_withholding_group_id,

            ignore_tax_withholding_threshold=payload.ignore_tax_withholding_threshold,

            override_tax_withholding_entries=payload.override_tax_withholding_entries,

            title=payload.title,

        )

        self._replace_items(business_id, row, [x.model_dump() for x in payload.items])

        self._replace_pricing_rules(business_id, row, [x.model_dump() for x in payload.pricing_rules])

        self._replace_timesheets(business_id, row, [x.model_dump() for x in payload.timesheets])

        self._replace_advances(business_id, row, [x.model_dump() for x in payload.advances])

        self._replace_payments(business_id, row, [x.model_dump() for x in payload.payments])

        self._replace_tax_withholding_entries(business_id, row, [x.model_dump() for x in payload.tax_withholding_entries])



        try:

            db.flush()  # children need ids before validation reads them

            self._validate(db, business_id, row, is_new=True)

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

        payload: SalesInvoiceUpdate,

    ) -> SalesInvoice:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "items":

                    self._replace_items(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "pricing_rules":

                    self._replace_pricing_rules(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "timesheets":

                    self._replace_timesheets(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "advances":

                    self._replace_advances(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "payments":

                    self._replace_payments(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "tax_withholding_entries":

                    self._replace_tax_withholding_entries(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

            db.flush()

            self._validate(db, business_id, row, is_new=False)

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

    ) -> SalesInvoice:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Sales Invoice")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SalesInvoice:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Sales Invoice")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row
