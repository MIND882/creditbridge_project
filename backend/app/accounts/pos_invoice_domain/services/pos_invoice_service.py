# HAND-WRITTEN

"""

Business logic for POS Invoice -- port of

``erpnext/accounts/doctype/pos_invoice/pos_invoice.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream hooks:

    validate

    before_submit

    on_submit

    before_cancel

    on_cancel

    clear_unallocated_mode_of_payments

    create_and_add_consolidated_sales_invoice

    create_return_sales_invoice

    delink_serial_and_batch_bundle

    submit_serial_batch_bundle

    check_phone_payments

    validate_stock_availablility

    validate_is_pos_using_sales_invoice

    validate_serialised_or_batched_item

    validate_return_items_qty

    validate_mode_of_payment

    validate_change_account

    validate_change_amount

    validate_payment_amount

    validate_company_with_pos_company

    set_outstanding_amount

    validate_loyalty_transaction

    set_status

    set_pos_fields

    set_missing_values

    reset_mode_of_payments

    create_payment_request

    get_new_payment_request

    get_existing_payment_request

    update_payments



**Upstream has 23 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.pos_invoice_domain.models.pos_invoice import POSInvoice

from app.accounts.pos_invoice_item_domain.models.pos_invoice_item import POSInvoiceItem

from app.accounts.pricing_rule_detail_domain.models.pricing_rule_detail import PricingRuleDetail

from app.accounts.sales_invoice_timesheet_domain.models.sales_invoice_timesheet import SalesInvoiceTimesheet

from app.accounts.sales_invoice_advance_domain.models.sales_invoice_advance import SalesInvoiceAdvance

from app.accounts.cashier_closing_payments_domain.models.cashier_closing_payments import CashierClosingPayments

from app.accounts.pos_invoice_domain.repositories.pos_invoice_repository import (

    POSInvoiceRepository,

)

from app.accounts.pos_invoice_domain.schemas.pos_invoice import (

    POSInvoiceCreate,

    POSInvoiceUpdate,

)

from app.accounts.sales_invoice_payment_domain.models.sales_invoice_payment import SalesInvoicePayment  # noqa: F401

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["POSInvoiceService"]





class POSInvoiceService:

    def __init__(self, repository: Optional[POSInvoiceRepository] = None) -> None:

        self.repository = repository or POSInvoiceRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> POSInvoice:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("POS Invoice", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: POSInvoice

    ) -> None:

        """

        TODO(PORT-VALIDATION): upstream validation is NOT ported.



        This controller has **23 ``frappe.throw`` site(s)** upstream.

        None are enforced here, so writes upstream would reject

        currently succeed. It fails open deliberately rather than

        blocking the CRUD surface, but must not be read as complete.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> POSInvoice:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[POSInvoice]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[POSInvoice].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_items(

        self, business_id: uuid.UUID, row: POSInvoice, items: list[dict]

    ) -> None:

        row.items.clear()

        for idx, item in enumerate(items, start=1):

            row.items.append(

                POSInvoiceItem(

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

                    item_group=item.get('item_group'),

                    brand=item.get('brand'),

                    image=item.get('image'),

                    image_view=item.get('image_view'),

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

                    item_tax_template_id=item.get('item_tax_template_id'),

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

                    is_fixed_asset=item.get('is_fixed_asset'),

                    asset=item.get('asset'),

                    finance_book_id=item.get('finance_book_id'),

                    expense_account_id=item.get('expense_account_id'),

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

                    item_tax_rate=item.get('item_tax_rate'),

                    actual_batch_qty=item.get('actual_batch_qty'),

                    actual_qty=item.get('actual_qty'),

                    sales_order=item.get('sales_order'),

                    so_detail=item.get('so_detail'),

                    delivery_note=item.get('delivery_note'),

                    dn_detail=item.get('dn_detail'),

                    delivered_qty=item.get('delivered_qty'),

                    cost_center_id=item.get('cost_center_id'),

                    page_break=item.get('page_break'),

                    project=item.get('project'),

                    pos_invoice_item=item.get('pos_invoice_item'),

                    grant_commission=item.get('grant_commission'),

                    has_item_scanned=item.get('has_item_scanned'),

                    serial_and_batch_bundle=item.get('serial_and_batch_bundle'),

                    use_serial_batch_fields=item.get('use_serial_batch_fields'),

                    distributed_discount_amount=item.get('distributed_discount_amount'),

                )

            )



    def _replace_pricing_rules(

        self, business_id: uuid.UUID, row: POSInvoice, items: list[dict]

    ) -> None:

        row.pricing_rules.clear()

        for idx, item in enumerate(items, start=1):

            row.pricing_rules.append(

                PricingRuleDetail(

                    business_id=business_id,

                    idx=idx,

                    parenttype='POS Invoice',

                    pricing_rule=item.get('pricing_rule'),

                    item_code=item.get('item_code'),

                    margin_type=item.get('margin_type'),

                    rate_or_discount=item.get('rate_or_discount'),

                    child_docname=item.get('child_docname'),

                    rule_applied=item.get('rule_applied'),

                )

            )



    def _replace_timesheets(

        self, business_id: uuid.UUID, row: POSInvoice, items: list[dict]

    ) -> None:

        row.timesheets.clear()

        for idx, item in enumerate(items, start=1):

            row.timesheets.append(

                SalesInvoiceTimesheet(

                    business_id=business_id,

                    idx=idx,

                    parenttype='POS Invoice',

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

        self, business_id: uuid.UUID, row: POSInvoice, items: list[dict]

    ) -> None:

        row.advances.clear()

        for idx, item in enumerate(items, start=1):

            row.advances.append(

                SalesInvoiceAdvance(

                    business_id=business_id,

                    idx=idx,

                    parenttype='POS Invoice',

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

        self, business_id: uuid.UUID, row: POSInvoice, items: list[dict]

    ) -> None:

        row.payments.clear()

        for idx, item in enumerate(items, start=1):

            row.payments.append(

                SalesInvoicePayment(

                    business_id=business_id,

                    idx=idx,

                    parenttype='POS Invoice',

                    mode_of_payment_id=item.get('mode_of_payment_id'),

                    amount=item.get('amount'),

                    account_id=item.get('account_id'),

                    type=item.get('type'),

                    base_amount=item.get('base_amount'),

                    clearance_date=item.get('clearance_date'),

                    default=item.get('default'),

                    reference_no=item.get('reference_no'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(POSInvoice).where(

                    POSInvoice.business_id == business_id

                )

            )

            or 0

        )

        return f"POS-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: POSInvoiceCreate

    ) -> POSInvoice:

        row = POSInvoice(

            business_id=business_id,

            name=self.next_name(db, business_id),

            naming_series=payload.naming_series,

            customer=payload.customer,

            customer_name=payload.customer_name,

            is_pos=payload.is_pos,

            pos_profile=payload.pos_profile,

            is_return=payload.is_return,

            posting_date=payload.posting_date,

            posting_time=payload.posting_time,

            set_posting_time=payload.set_posting_time,

            due_date=payload.due_date,

            amended_from=payload.amended_from,

            return_against=payload.return_against,

            update_billed_amount_in_sales_order=payload.update_billed_amount_in_sales_order,

            project=payload.project,

            cost_center_id=payload.cost_center_id,

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

            consolidated_invoice=payload.consolidated_invoice,

            coupon_code=payload.coupon_code,

            amount_eligible_for_commission=payload.amount_eligible_for_commission,

            update_billed_amount_in_delivery_note=payload.update_billed_amount_in_delivery_note,

            utm_medium=payload.utm_medium,

            utm_campaign=payload.utm_campaign,

            utm_source=payload.utm_source,

            company_contact_person=payload.company_contact_person,

            last_scanned_warehouse=payload.last_scanned_warehouse,

            title=payload.title,

        )

        self._replace_items(business_id, row, [x.model_dump() for x in payload.items])

        self._replace_pricing_rules(business_id, row, [x.model_dump() for x in payload.pricing_rules])

        self._replace_timesheets(business_id, row, [x.model_dump() for x in payload.timesheets])

        self._replace_advances(business_id, row, [x.model_dump() for x in payload.advances])

        self._replace_payments(business_id, row, [x.model_dump() for x in payload.payments])



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

        payload: POSInvoiceUpdate,

    ) -> POSInvoice:

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

    ) -> POSInvoice:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "POS Invoice")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> POSInvoice:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "POS Invoice")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row
