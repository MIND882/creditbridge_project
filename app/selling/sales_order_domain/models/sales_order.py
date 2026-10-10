"""

Sales Order -- converted from ``erpnext/selling/doctype/sales_order``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, Enum as SAEnum, ForeignKey, Integer, Numeric, String, Text, Time, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.selling.sales_order_item_domain.models.sales_order_item import SalesOrderItem

from app.selling.delivery_schedule_item_domain.models.delivery_schedule_item import DeliveryScheduleItem



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["SalesOrder", "SalesOrderNamingSeries", "SalesOrderOrderType", "SalesOrderApplyDiscountOn", "SalesOrderStatus", "SalesOrderDeliveryStatus", "SalesOrderBillingStatus", "SalesOrderAdvancePaymentStatus"]





class SalesOrderNamingSeries(str, enum.Enum):

    SAL_ORD_YYYY = "SAL-ORD-.YYYY.-"



class SalesOrderOrderType(str, enum.Enum):

    SALES = "Sales"

    MAINTENANCE = "Maintenance"

    SHOPPING_CART = "Shopping Cart"



class SalesOrderApplyDiscountOn(str, enum.Enum):

    GRAND_TOTAL = "Grand Total"

    NET_TOTAL = "Net Total"



class SalesOrderStatus(str, enum.Enum):

    DRAFT = "Draft"

    ON_HOLD = "On Hold"

    TO_PAY = "To Pay"

    TO_DELIVER_AND_BILL = "To Deliver and Bill"

    TO_BILL = "To Bill"

    TO_DELIVER = "To Deliver"

    COMPLETED = "Completed"

    CANCELLED = "Cancelled"

    CLOSED = "Closed"



class SalesOrderDeliveryStatus(str, enum.Enum):

    NOT_DELIVERED = "Not Delivered"

    FULLY_DELIVERED = "Fully Delivered"

    PARTLY_DELIVERED = "Partly Delivered"

    CLOSED = "Closed"

    NOT_APPLICABLE = "Not Applicable"



class SalesOrderBillingStatus(str, enum.Enum):

    NOT_BILLED = "Not Billed"

    FULLY_BILLED = "Fully Billed"

    PARTLY_BILLED = "Partly Billed"

    CLOSED = "Closed"



class SalesOrderAdvancePaymentStatus(str, enum.Enum):

    NOT_REQUESTED = "Not Requested"

    REQUESTED = "Requested"

    PARTIALLY_PAID = "Partially Paid"

    FULLY_PAID = "Fully Paid"





class SalesOrder(SubmittableModel, TenantModel):

    __tablename__ = "sales_orders"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_sales_orders_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    company: Mapped[str] = mapped_column(String(140), nullable=False)

    naming_series: Mapped[str] = mapped_column(SAEnum(SalesOrderNamingSeries, values_callable=lambda x: [e.value for e in x], native_enum=False, length=19, validate_strings=True), nullable=False)

    customer_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("selling_customers.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    customer = relationship("app.selling.customer_domain.models.customer.Customer", foreign_keys=[customer_id])

    customer_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    order_type: Mapped[str] = mapped_column(SAEnum(SalesOrderOrderType, values_callable=lambda x: [e.value for e in x], native_enum=False, length=17, validate_strings=True), nullable=False)

    transaction_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    transaction_time: Mapped[Optional[dt.time]] = mapped_column(Time, nullable=True)

    delivery_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    tax_id: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    skip_delivery_note: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    has_unit_price_items: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    is_subcontracted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("sales_orders.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("app.selling.sales_order_domain.models.sales_order.SalesOrder", foreign_keys=[amended_from_id])

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("app.accounts.cost_center_domain.models.cost_center.CostCenter", foreign_keys=[cost_center_id])

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    currency: Mapped[str] = mapped_column(String(140), nullable=False)

    conversion_rate: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    selling_price_list_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("price_lists.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    selling_price_list = relationship("app.stock.price_list_domain.models.price_list.PriceList", foreign_keys=[selling_price_list_id])

    price_list_currency: Mapped[str] = mapped_column(String(140), nullable=False)

    plc_conversion_rate: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    ignore_pricing_rule: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    scan_barcode: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    last_scanned_warehouse: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    set_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    set_warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[set_warehouse_id])

    reserve_stock: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    total_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_net_weight: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_net_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    net_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    tax_category_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("tax_categories.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    tax_category = relationship("app.accounts.tax_category_domain.models.tax_category.TaxCategory", foreign_keys=[tax_category_id])

    taxes_and_charges_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("sales_taxes_and_charges_templates.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    taxes_and_charges = relationship("app.accounts.sales_taxes_and_charges_template_domain.models.sales_taxes_and_charges_template.SalesTaxesAndChargesTemplate", foreign_keys=[taxes_and_charges_id])

    shipping_rule_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("shipping_rules.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    shipping_rule = relationship("app.accounts.shipping_rule_domain.models.shipping_rule.ShippingRule", foreign_keys=[shipping_rule_id])

    incoterm: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    named_place: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    base_total_taxes_and_charges: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_taxes_and_charges: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    grand_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    in_words: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    disable_rounded_total: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    rounding_adjustment: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rounded_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_grand_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_in_words: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    base_rounding_adjustment: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_rounded_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    advance_paid: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    apply_discount_on: Mapped[Optional[str]] = mapped_column(SAEnum(SalesOrderApplyDiscountOn, native_enum=False, length=15, validate_strings=True), nullable=True)

    base_discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    coupon_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("coupon_codes.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    coupon_code = relationship("app.accounts.coupon_code_domain.models.coupon_code.CouponCode", foreign_keys=[coupon_code_id])

    additional_discount_percentage: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    other_charges_calculation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    customer_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    address_display: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    customer_group: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    territory: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    contact_person: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    contact_display: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    contact_phone: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    contact_mobile: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    contact_email: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    shipping_address_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    shipping_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    dispatch_address_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    dispatch_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    company_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    company_address_display: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    company_contact_person: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    ignore_default_payment_terms_template: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    payment_terms_template_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("payment_terms_templates.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    payment_terms_template = relationship("app.accounts.payment_terms_template_domain.models.payment_terms_template.PaymentTermsTemplate", foreign_keys=[payment_terms_template_id])

    tc_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    terms: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    status: Mapped[str] = mapped_column(SAEnum(SalesOrderStatus, values_callable=lambda x: [e.value for e in x], native_enum=False, length=23, validate_strings=True), nullable=False)

    delivery_status: Mapped[Optional[str]] = mapped_column(SAEnum(SalesOrderDeliveryStatus, native_enum=False, length=20, validate_strings=True), nullable=True)

    per_delivered: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    per_billed: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    per_picked: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    billing_status: Mapped[Optional[str]] = mapped_column(SAEnum(SalesOrderBillingStatus, values_callable=lambda x: [e.value for e in x], native_enum=False, length=17, validate_strings=True), nullable=True)

    advance_payment_status: Mapped[Optional[str]] = mapped_column(SAEnum(SalesOrderAdvancePaymentStatus,values_callable=lambda x: [e.value for e in x],  native_enum=False, length=18, validate_strings=True), nullable=True)

    sales_partner: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    amount_eligible_for_commission: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    commission_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_commission: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    loyalty_points: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    loyalty_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    from_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    to_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    auto_repeat: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    letter_head: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    group_same_items: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    select_print_heading: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    language: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    utm_source: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    utm_medium: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    utm_campaign: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    utm_content: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_internal_customer: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    po_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    po_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    represents_company: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    title: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    inter_company_order_reference_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("purchase_orders.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    inter_company_order_reference = relationship("app.buying.purchase_order_domain.models.purchase_order.PurchaseOrder", foreign_keys=[inter_company_order_reference_id])

    party_account_currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    items: Mapped[list["SalesOrderItem"]] = relationship(  # noqa: F821

        "app.selling.sales_order_item_domain.models.sales_order_item.SalesOrderItem",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys=[SalesOrderItem.parent_id],

    )



    delivery_schedule: Mapped[list["DeliveryScheduleItem"]] = relationship(  # noqa: F821

        "app.selling.delivery_schedule_item_domain.models.delivery_schedule_item.DeliveryScheduleItem",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys=[DeliveryScheduleItem.parent_id],

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SalesOrder id={self.id}>"
