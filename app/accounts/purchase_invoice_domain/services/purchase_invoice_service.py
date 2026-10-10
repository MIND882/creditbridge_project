# HAND-WRITTEN

"""

Business logic for Purchase Invoice -- port of

``erpnext/accounts/doctype/purchase_invoice/purchase_invoice.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream hooks:

    onload

    before_save

    invoice_is_blocked

    validate

    set_percentage_received

    validate_release_date

    validate_cash

    create_remarks

    set_missing_values

    validate_credit_to_acc

    validate_with_previous_doc

    validate_warehouse

    validate_item_code

    set_expense_account

    force_set_against_expense_account

    po_required

    pr_required

    validate_write_off_account

    validate_write_off_cost_center

    check_prev_docstatus

    update_status_updater_args

    validate_purchase_receipt_if_update_stock

    validate_for_repost

    before_submit

    on_submit

    on_update_after_submit

    refresh_subscription_status

    make_gl_entries

    update_supplier_outstanding

    get_gl_entries

    check_asset_cwip_enabled

    on_cancel

    update_project

    validate_supplier_invoice

    on_recurring

    block_invoice

    unblock_invoice

    set_status



**Upstream has 10 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import datetime as dt

import uuid

from decimal import Decimal

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.account_domain.models.account import Account

from app.accounts.purchase_invoice_domain.models.purchase_invoice import (

    PurchaseInvoice,

    PurchaseInvoiceIsOpening,

)

from app.accounts.pos_invoice_item_domain.models.pos_invoice_item import POSInvoiceItem

from app.accounts.pricing_rule_detail_domain.models.pricing_rule_detail import PricingRuleDetail

from app.accounts.sales_invoice_advance_domain.models.sales_invoice_advance import SalesInvoiceAdvance

from app.accounts.tax_withholding_entry_domain.models.tax_withholding_entry import TaxWithholdingEntry

from app.accounts.purchase_invoice_domain.repositories.purchase_invoice_repository import (

    PurchaseInvoiceRepository,

)

from app.accounts.purchase_invoice_domain.schemas.purchase_invoice import (

    PurchaseInvoiceCreate,

    PurchaseInvoiceUpdate,

)

from app.accounts.purchase_invoice_item_domain.models.purchase_invoice_item import PurchaseInvoiceItem  # noqa: F401

from app.accounts.purchase_invoice_advance_domain.models.purchase_invoice_advance import PurchaseInvoiceAdvance  # noqa: F401

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



__all__ = ["PurchaseInvoiceService"]





class PurchaseInvoiceService:

    def __init__(self, repository: Optional[PurchaseInvoiceRepository] = None) -> None:

        # The fiscal-year lookup is a cross-domain read, so the service is

        # held rather than re-resolving it on every validation pass.

        self._fiscal_years = FiscalYearService()

        self.repository = repository or PurchaseInvoiceRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PurchaseInvoice:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Purchase Invoice", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: PurchaseInvoice, *, is_new: bool

    ) -> None:

        """

        Port of upstream ``validate``. Upstream order is preserved where the

        rules were ported; see the note at the end for what is missing.

        """

        # accounts_controller.validate_date_with_fiscal_year

        self._validate_date_with_fiscal_year(db, business_id, row)

        # accounts_controller.validate_qty_is_not_zero

        self._validate_qty_is_not_zero(row)

        self._validate_credit_to_acc(db, business_id, row)

        # accounts_controller.check_conversion_rate

        self._check_conversion_rate(row)



        # validate: ``if not self.is_opening: self.is_opening = "No"``

        if not row.is_opening:

            row.is_opening = PurchaseInvoiceIsOpening.NO



        # TODO(PORT-VALIDATION): the remaining upstream rules are NOT ported.

        # They read Buying or Stock state, neither of which is converted:

        #

        #   validate_with_previous_doc      -- billed/returned qty against

        #                                      Purchase Order and Purchase

        #                                      Receipt; "Row #N: Cannot receive

        #                                      more than N".

        #   ensure_supplier_is_not_blocked  -- accounts_controller; reads the

        #                                      Supplier doctype's blocked flag.

        #   validate_warehouse /

        #   update_current_stock            -- batch, serial and stock levels.

        #   Landed Cost, asset

        #   capitalisation                  -- need Asset and Stock modules.

        #   deferred expense, tax

        #   withholding, provisional        -- need the tax and totals engine

        #                                      (erpnext.accounts.services.taxes).

        #

        # These fail open. A Purchase Invoice that upstream would reject for an

        # over-received quantity or a blocked supplier is accepted here.

        return None



    # ── validate_date_with_fiscal_year (accounts_controller) ──────────────

    def _validate_date_with_fiscal_year(

        self, db: Session, business_id: uuid.UUID, row: PurchaseInvoice

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

                code="purchase_invoice_not_in_fiscal_year",

                details={"posting_date": row.posting_date.isoformat()},

            )



    # ── check_conversion_rate (accounts_controller) ───────────────────────

    def _check_conversion_rate(self, row: PurchaseInvoice) -> None:

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

                code="purchase_invoice_zero_conversion_rate",

                details={"conversion_rate": str(row.conversion_rate)},

            )



    # ── validate_qty_is_not_zero (accounts_controller) ────────────────────

    def _validate_qty_is_not_zero(self, row: PurchaseInvoice) -> None:

        """Skipped for returns and debit notes, which carry no quantity."""

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

                    code="purchase_invoice_zero_qty",

                    details={"idx": item.idx, "item": item.item_name},

                )



    # ── validate_credit_to_acc ────────────────────────────────────────────

    def _validate_credit_to_acc(

        self, db: Session, business_id: uuid.UUID, row: PurchaseInvoice

    ) -> None:

        """

        The payable account the invoice is booked to. Mirror of the Sales

        Invoice rule, with Payable in place of Receivable.



        Upstream first falls back to the party's default account via

        ``get_party_account``. That reads the Supplier doctype's ``accounts``

        child table; Supplier is not converted, so a blank Credit To is simply

        an error here.

        """

        if not row.credit_to_id:

            raise DomainValidationError(

                "Credit To is required",

                code="purchase_invoice_credit_to_required",

                details={"credit_to_id": None},

            )



        account = db.scalar(

            select(Account).where(

                Account.id == row.credit_to_id, Account.business_id == business_id

            )

        )

        if account is None:

            raise DomainValidationError(

                "Credit To is required",

                code="purchase_invoice_credit_to_required",

                details={"credit_to_id": str(row.credit_to_id)},

            )



        report_type = getattr(account.report_type, "value", account.report_type)

        if report_type != "Balance Sheet":

            raise DomainValidationError(

                "Please ensure that the Credit To account is a Balance Sheet "

                "account. You can change the parent account to a Balance Sheet "

                "account or select a different account.",

                code="purchase_invoice_credit_to_not_balance_sheet",

                details={"account": account.name, "report_type": str(report_type)},

            )



        if row.supplier:

            account_type = getattr(account.account_type, "value", account.account_type)

            if account_type != "Payable":

                raise DomainValidationError(

                    f"Please ensure that the Credit To account {account.name} is "

                    f"a Payable account. You can change the account type to "

                    f"Payable or select a different account.",

                    code="purchase_invoice_credit_to_not_payable",

                    details={"account": account.name, "account_type": str(account_type)},

                )



        # ``self.party_account_currency = account.account_currency``. The

        # converted Account has no account_currency column.

        if not row.party_account_currency:

            row.party_account_currency = row.currency



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PurchaseInvoice:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PurchaseInvoice]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PurchaseInvoice].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_items(

        self, business_id: uuid.UUID, row: PurchaseInvoice, items: list[dict]

    ) -> None:

        row.items.clear()

        for idx, item in enumerate(items, start=1):

            row.items.append(

                PurchaseInvoiceItem(

                    business_id=business_id,

                    idx=idx,

                    name=item.get('name'),

                    item_code=item.get('item_code'),

                    item_name=item.get('item_name'),

                    description=item.get('description'),

                    image=item.get('image'),

                    image_view=item.get('image_view'),

                    received_qty=item.get('received_qty'),

                    qty=item.get('qty'),

                    rejected_qty=item.get('rejected_qty'),

                    stock_uom=item.get('stock_uom'),

                    uom=item.get('uom'),

                    conversion_factor=item.get('conversion_factor'),

                    stock_qty=item.get('stock_qty'),

                    price_list_rate=item.get('price_list_rate'),

                    discount_percentage=item.get('discount_percentage'),

                    discount_amount=item.get('discount_amount'),

                    base_price_list_rate=item.get('base_price_list_rate'),

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

                    weight_per_unit=item.get('weight_per_unit'),

                    total_weight=item.get('total_weight'),

                    weight_uom=item.get('weight_uom'),

                    warehouse=item.get('warehouse'),

                    rejected_warehouse=item.get('rejected_warehouse'),

                    quality_inspection=item.get('quality_inspection'),

                    batch_no=item.get('batch_no'),

                    serial_no=item.get('serial_no'),

                    rejected_serial_no=item.get('rejected_serial_no'),

                    expense_account_id=item.get('expense_account_id'),

                    item_tax_template_id=item.get('item_tax_template_id'),

                    project=item.get('project'),

                    cost_center_id=item.get('cost_center_id'),

                    deferred_expense_account_id=item.get('deferred_expense_account_id'),

                    service_stop_date=item.get('service_stop_date'),

                    enable_deferred_expense=item.get('enable_deferred_expense'),

                    service_start_date=item.get('service_start_date'),

                    service_end_date=item.get('service_end_date'),

                    allow_zero_valuation_rate=item.get('allow_zero_valuation_rate'),

                    brand=item.get('brand'),

                    item_group=item.get('item_group'),

                    item_tax_rate=item.get('item_tax_rate'),

                    item_tax_amount=item.get('item_tax_amount'),

                    purchase_order=item.get('purchase_order'),

                    include_exploded_items=item.get('include_exploded_items'),

                    is_fixed_asset=item.get('is_fixed_asset'),

                    asset_location=item.get('asset_location'),

                    po_detail=item.get('po_detail'),

                    purchase_receipt=item.get('purchase_receipt'),

                    page_break=item.get('page_break'),

                    pr_detail=item.get('pr_detail'),

                    valuation_rate=item.get('valuation_rate'),

                    rm_supp_cost=item.get('rm_supp_cost'),

                    landed_cost_voucher_amount=item.get('landed_cost_voucher_amount'),

                    manufacturer=item.get('manufacturer'),

                    manufacturer_part_no=item.get('manufacturer_part_no'),

                    asset_category=item.get('asset_category'),

                    from_warehouse=item.get('from_warehouse'),

                    purchase_invoice_item=item.get('purchase_invoice_item'),

                    stock_uom_rate=item.get('stock_uom_rate'),

                    sales_invoice_item=item.get('sales_invoice_item'),

                    margin_type=item.get('margin_type'),

                    margin_rate_or_amount=item.get('margin_rate_or_amount'),

                    rate_with_margin=item.get('rate_with_margin'),

                    base_rate_with_margin=item.get('base_rate_with_margin'),

                    product_bundle=item.get('product_bundle'),

                    apply_tds=item.get('apply_tds'),

                    serial_and_batch_bundle=item.get('serial_and_batch_bundle'),

                    rejected_serial_and_batch_bundle=item.get('rejected_serial_and_batch_bundle'),

                    wip_composite_asset=item.get('wip_composite_asset'),

                    use_serial_batch_fields=item.get('use_serial_batch_fields'),

                    material_request=item.get('material_request'),

                    material_request_item=item.get('material_request_item'),

                    sales_incoming_rate=item.get('sales_incoming_rate'),

                    distributed_discount_amount=item.get('distributed_discount_amount'),

                    tax_withholding_category_id=item.get('tax_withholding_category_id'),

                    delivered_by_supplier=item.get('delivered_by_supplier'),

                )

            )



    def _replace_pricing_rules(

        self, business_id: uuid.UUID, row: PurchaseInvoice, items: list[dict]

    ) -> None:

        row.pricing_rules.clear()

        for idx, item in enumerate(items, start=1):

            row.pricing_rules.append(

                PricingRuleDetail(

                    business_id=business_id,

                    idx=idx,

                    parenttype='Purchase Invoice',

                    pricing_rule=item.get('pricing_rule'),

                    item_code=item.get('item_code'),

                    margin_type=item.get('margin_type'),

                    rate_or_discount=item.get('rate_or_discount'),

                    child_docname=item.get('child_docname'),

                    rule_applied=item.get('rule_applied'),

                )

            )



    def _replace_advances(

        self, business_id: uuid.UUID, row: PurchaseInvoice, items: list[dict]

    ) -> None:

        row.advances.clear()

        for idx, item in enumerate(items, start=1):

            row.advances.append(

                PurchaseInvoiceAdvance(

                    business_id=business_id,

                    idx=idx,

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



    def _replace_tax_withholding_entries(

        self, business_id: uuid.UUID, row: PurchaseInvoice, items: list[dict]

    ) -> None:

        row.tax_withholding_entries.clear()

        for idx, item in enumerate(items, start=1):

            row.tax_withholding_entries.append(

                TaxWithholdingEntry(

                    business_id=business_id,

                    idx=idx,

                    parenttype='Purchase Invoice',

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

                select(func.count()).select_from(PurchaseInvoice).where(

                    PurchaseInvoice.business_id == business_id

                )

            )

            or 0

        )

        year = dt.date.today().year

        return f"ACC-PINV-{year}-{count + 1:08d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: PurchaseInvoiceCreate

    ) -> PurchaseInvoice:

        row = PurchaseInvoice(

            business_id=business_id,

            name=self.next_name(db, business_id),

            title=payload.title,

            naming_series=payload.naming_series,

            supplier=payload.supplier,

            supplier_name=payload.supplier_name,

            due_date=payload.due_date,

            is_paid=payload.is_paid,

            is_return=payload.is_return,

            apply_tds=payload.apply_tds,

            cost_center_id=payload.cost_center_id,

            posting_date=payload.posting_date,

            posting_time=payload.posting_time,

            set_posting_time=payload.set_posting_time,

            amended_from=payload.amended_from,

            on_hold=payload.on_hold,

            release_date=payload.release_date,

            hold_comment=payload.hold_comment,

            bill_no=payload.bill_no,

            bill_date=payload.bill_date,

            return_against=payload.return_against,

            update_billed_amount_in_purchase_order=payload.update_billed_amount_in_purchase_order,

            update_billed_amount_in_purchase_receipt=payload.update_billed_amount_in_purchase_receipt,

            supplier_address=payload.supplier_address,

            address_display=payload.address_display,

            contact_person=payload.contact_person,

            contact_display=payload.contact_display,

            contact_mobile=payload.contact_mobile,

            contact_email=payload.contact_email,

            shipping_address=payload.shipping_address,

            shipping_address_display=payload.shipping_address_display,

            currency=payload.currency,

            conversion_rate=payload.conversion_rate,

            buying_price_list=payload.buying_price_list,

            price_list_currency=payload.price_list_currency,

            plc_conversion_rate=payload.plc_conversion_rate,

            ignore_pricing_rule=payload.ignore_pricing_rule,

            set_warehouse=payload.set_warehouse,

            rejected_warehouse=payload.rejected_warehouse,

            is_subcontracted=payload.is_subcontracted,

            update_stock=payload.update_stock,

            scan_barcode=payload.scan_barcode,

            total_qty=payload.total_qty,

            base_total=payload.base_total,

            base_net_total=payload.base_net_total,

            total=payload.total,

            net_total=payload.net_total,

            total_net_weight=payload.total_net_weight,

            tax_category_id=payload.tax_category_id,

            shipping_rule=payload.shipping_rule,

            taxes_and_charges=payload.taxes_and_charges,

            other_charges_calculation=payload.other_charges_calculation,

            base_taxes_and_charges_added=payload.base_taxes_and_charges_added,

            base_taxes_and_charges_deducted=payload.base_taxes_and_charges_deducted,

            base_total_taxes_and_charges=payload.base_total_taxes_and_charges,

            taxes_and_charges_added=payload.taxes_and_charges_added,

            taxes_and_charges_deducted=payload.taxes_and_charges_deducted,

            total_taxes_and_charges=payload.total_taxes_and_charges,

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

            disable_rounded_total=payload.disable_rounded_total,

            mode_of_payment_id=payload.mode_of_payment_id,

            cash_bank_account_id=payload.cash_bank_account_id,

            clearance_date=payload.clearance_date,

            paid_amount=payload.paid_amount,

            base_paid_amount=payload.base_paid_amount,

            write_off_amount=payload.write_off_amount,

            base_write_off_amount=payload.base_write_off_amount,

            write_off_account_id=payload.write_off_account_id,

            write_off_cost_center_id=payload.write_off_cost_center_id,

            allocate_advances_automatically=payload.allocate_advances_automatically,

            payment_terms_template_id=payload.payment_terms_template_id,

            tc_name=payload.tc_name,

            terms=payload.terms,

            letter_head=payload.letter_head,

            group_same_items=payload.group_same_items,

            select_print_heading=payload.select_print_heading,

            language=payload.language,

            is_internal_supplier=payload.is_internal_supplier,

            credit_to_id=payload.credit_to_id,

            party_account_currency=payload.party_account_currency,

            is_opening=payload.is_opening,

            against_expense_account=payload.against_expense_account,

            status=payload.status,

            inter_company_invoice_reference=payload.inter_company_invoice_reference,

            remarks=payload.remarks,

            from_date=payload.from_date,

            to_date=payload.to_date,

            auto_repeat=payload.auto_repeat,

            billing_address=payload.billing_address,

            billing_address_display=payload.billing_address_display,

            project=payload.project,

            unrealized_profit_loss_account_id=payload.unrealized_profit_loss_account_id,

            set_from_warehouse=payload.set_from_warehouse,

            supplier_warehouse=payload.supplier_warehouse,

            per_received=payload.per_received,

            ignore_default_payment_terms_template=payload.ignore_default_payment_terms_template,

            subscription=payload.subscription,

            incoterm=payload.incoterm,

            named_place=payload.named_place,

            only_include_allocated_payments=payload.only_include_allocated_payments,

            use_company_roundoff_cost_center=payload.use_company_roundoff_cost_center,

            use_transaction_date_exchange_rate=payload.use_transaction_date_exchange_rate,

            supplier_group=payload.supplier_group,

            update_outstanding_for_self=payload.update_outstanding_for_self,

            sender=payload.sender,

            dispatch_address_display=payload.dispatch_address_display,

            dispatch_address=payload.dispatch_address,

            last_scanned_warehouse=payload.last_scanned_warehouse,

            claimed_landed_cost_amount=payload.claimed_landed_cost_amount,

            tax_withholding_group_id=payload.tax_withholding_group_id,

            ignore_tax_withholding_threshold=payload.ignore_tax_withholding_threshold,

            override_tax_withholding_entries=payload.override_tax_withholding_entries,

        )

        self._replace_items(business_id, row, [x.model_dump() for x in payload.items])

        self._replace_pricing_rules(business_id, row, [x.model_dump() for x in payload.pricing_rules])

        self._replace_advances(business_id, row, [x.model_dump() for x in payload.advances])

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

        payload: PurchaseInvoiceUpdate,

    ) -> PurchaseInvoice:

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

                if field_name == "advances":

                    self._replace_advances(business_id, row, value or [])

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

    ) -> PurchaseInvoice:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Purchase Invoice")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PurchaseInvoice:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Purchase Invoice")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row
