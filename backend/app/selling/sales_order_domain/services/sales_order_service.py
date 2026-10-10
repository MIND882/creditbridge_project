"""Business logic for Sales Order -- port of

``erpnext/selling/doctype/sales_order/sales_order.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.selling.sales_order_domain.models.sales_order import SalesOrder

from app.selling.sales_order_domain.repositories.sales_order_repository import (

    SalesOrderRepository,

)

from app.selling.sales_order_domain.schemas.sales_order import (

    SalesOrderCreate,

    SalesOrderUpdate,

)

from app.selling.sales_order_item_domain.models.sales_order_item import SalesOrderItem

from app.selling.delivery_schedule_item_domain.models.delivery_schedule_item import DeliveryScheduleItem

from app.core.errors import NotFoundError

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.pagination import ResultPage



__all__ = ["SalesOrderService"]





class SalesOrderService:

    def __init__(self, repository: Optional[SalesOrderRepository] = None) -> None:

        self.repository = repository or SalesOrderRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SalesOrder:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Sales Order", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: SalesOrder

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SalesOrder:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[SalesOrder]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SalesOrder].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID, series: Optional[str] = None) -> str:

        """A per-tenant sequential name; upstream mints one from ``naming_series``."""

        # ``naming_series`` is optional on input (Frappe fills it from a

        # default), so fall back to the doctype prefix when it is absent.

        series = series or ""

        prefix = series.split(".")[0].split("#")[0]

        if prefix and not prefix.endswith("-"):

            prefix += "-"

        count = int(

            db.scalar(

                select(func.count()).select_from(SalesOrder).where(

                    SalesOrder.business_id == business_id

                )

            )

            or 0

        )

        return f"{prefix}{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: SalesOrderCreate

    ) -> SalesOrder:

        row = SalesOrder(

            business_id=business_id,

            name=self.next_name(db, business_id, payload.naming_series),

            company=payload.company,

            naming_series=payload.naming_series,

            customer_id=payload.customer_id,

            customer_name=payload.customer_name,

            order_type=payload.order_type,

            transaction_date=payload.transaction_date,

            transaction_time=payload.transaction_time,

            delivery_date=payload.delivery_date,

            tax_id=payload.tax_id,

            skip_delivery_note=payload.skip_delivery_note,

            has_unit_price_items=payload.has_unit_price_items,

            is_subcontracted=payload.is_subcontracted,

            amended_from_id=payload.amended_from_id,

            cost_center_id=payload.cost_center_id,

            project=payload.project,

            currency=payload.currency,

            conversion_rate=payload.conversion_rate,

            selling_price_list_id=payload.selling_price_list_id,

            price_list_currency=payload.price_list_currency,

            plc_conversion_rate=payload.plc_conversion_rate,

            ignore_pricing_rule=payload.ignore_pricing_rule,

            scan_barcode=payload.scan_barcode,

            last_scanned_warehouse=payload.last_scanned_warehouse,

            set_warehouse_id=payload.set_warehouse_id,

            reserve_stock=payload.reserve_stock,

            total_qty=payload.total_qty,

            total_net_weight=payload.total_net_weight,

            base_total=payload.base_total,

            base_net_total=payload.base_net_total,

            total=payload.total,

            net_total=payload.net_total,

            tax_category_id=payload.tax_category_id,

            taxes_and_charges_id=payload.taxes_and_charges_id,

            shipping_rule_id=payload.shipping_rule_id,

            incoterm=payload.incoterm,

            named_place=payload.named_place,

            base_total_taxes_and_charges=payload.base_total_taxes_and_charges,

            total_taxes_and_charges=payload.total_taxes_and_charges,

            grand_total=payload.grand_total,

            in_words=payload.in_words,

            disable_rounded_total=payload.disable_rounded_total,

            rounding_adjustment=payload.rounding_adjustment,

            rounded_total=payload.rounded_total,

            base_grand_total=payload.base_grand_total,

            base_in_words=payload.base_in_words,

            base_rounding_adjustment=payload.base_rounding_adjustment,

            base_rounded_total=payload.base_rounded_total,

            advance_paid=payload.advance_paid,

            apply_discount_on=payload.apply_discount_on,

            base_discount_amount=payload.base_discount_amount,

            coupon_code_id=payload.coupon_code_id,

            additional_discount_percentage=payload.additional_discount_percentage,

            discount_amount=payload.discount_amount,

            other_charges_calculation=payload.other_charges_calculation,

            customer_address=payload.customer_address,

            address_display=payload.address_display,

            customer_group=payload.customer_group,

            territory=payload.territory,

            contact_person=payload.contact_person,

            contact_display=payload.contact_display,

            contact_phone=payload.contact_phone,

            contact_mobile=payload.contact_mobile,

            contact_email=payload.contact_email,

            shipping_address_name=payload.shipping_address_name,

            shipping_address=payload.shipping_address,

            dispatch_address_name=payload.dispatch_address_name,

            dispatch_address=payload.dispatch_address,

            company_address=payload.company_address,

            company_address_display=payload.company_address_display,

            company_contact_person=payload.company_contact_person,

            ignore_default_payment_terms_template=payload.ignore_default_payment_terms_template,

            payment_terms_template_id=payload.payment_terms_template_id,

            tc_name=payload.tc_name,

            terms=payload.terms,

            status=payload.status,

            delivery_status=payload.delivery_status,

            per_delivered=payload.per_delivered,

            per_billed=payload.per_billed,

            per_picked=payload.per_picked,

            billing_status=payload.billing_status,

            advance_payment_status=payload.advance_payment_status,

            sales_partner=payload.sales_partner,

            amount_eligible_for_commission=payload.amount_eligible_for_commission,

            commission_rate=payload.commission_rate,

            total_commission=payload.total_commission,

            loyalty_points=payload.loyalty_points,

            loyalty_amount=payload.loyalty_amount,

            from_date=payload.from_date,

            to_date=payload.to_date,

            auto_repeat=payload.auto_repeat,

            letter_head=payload.letter_head,

            group_same_items=payload.group_same_items,

            select_print_heading=payload.select_print_heading,

            language=payload.language,

            utm_source=payload.utm_source,

            utm_medium=payload.utm_medium,

            utm_campaign=payload.utm_campaign,

            utm_content=payload.utm_content,

            is_internal_customer=payload.is_internal_customer,

            po_no=payload.po_no,

            po_date=payload.po_date,

            represents_company=payload.represents_company,

            title=payload.title,

            inter_company_order_reference_id=payload.inter_company_order_reference_id,

            party_account_currency=payload.party_account_currency,

        )

        self._replace_items(business_id, row, [x.model_dump() for x in payload.items])

        self._replace_delivery_schedule(business_id, row, [x.model_dump() for x in payload.delivery_schedule])



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

        payload: SalesOrderUpdate,

    ) -> SalesOrder:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "items":

                    self._replace_items(business_id, row, value or [])

                    continue

                if field_name == "delivery_schedule":

                    self._replace_delivery_schedule(business_id, row, value or [])

                    continue

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

    ) -> SalesOrder:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Sales Order")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SalesOrder:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Sales Order")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row



    def _replace_items(

        self, business_id: uuid.UUID, row: SalesOrder, items: list[dict]

    ) -> None:

        row.items.clear()

        for idx, entry in enumerate(items, start=1):

            row.items.append(

                SalesOrderItem(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Sales Order",

                    parentfield="items",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_delivery_schedule(

        self, business_id: uuid.UUID, row: SalesOrder, delivery_schedule: list[dict]

    ) -> None:

        row.delivery_schedule.clear()

        for idx, entry in enumerate(delivery_schedule, start=1):

            row.delivery_schedule.append(

                DeliveryScheduleItem(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Sales Order",

                    parentfield="delivery_schedule",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )
