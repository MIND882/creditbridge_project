"""

Purchase Order -- converted from ``erpnext/buying/doctype/purchase_order``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, Enum as SAEnum, ForeignKey, Numeric, String, Text, Time, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.buying.purchase_order_item_domain.models.purchase_order_item import PurchaseOrderItem



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["PurchaseOrder", "PurchaseOrderNamingSeries", "PurchaseOrderApplyDiscountOn", "PurchaseOrderStatus", "PurchaseOrderAdvancePaymentStatus"]





class PurchaseOrderNamingSeries(str, enum.Enum):

    PUR_ORD_YYYY = "PUR-ORD-.YYYY.-"



class PurchaseOrderApplyDiscountOn(str, enum.Enum):

    GRAND_TOTAL = "Grand Total"

    NET_TOTAL = "Net Total"



class PurchaseOrderStatus(str, enum.Enum):

    DRAFT = "Draft"

    ON_HOLD = "On Hold"

    TO_RECEIVE_AND_BILL = "To Receive and Bill"

    TO_BILL = "To Bill"

    TO_RECEIVE = "To Receive"

    COMPLETED = "Completed"

    CANCELLED = "Cancelled"

    CLOSED = "Closed"

    DELIVERED = "Delivered"



class PurchaseOrderAdvancePaymentStatus(str, enum.Enum):

    NOT_INITIATED = "Not Initiated"

    INITIATED = "Initiated"

    PARTIALLY_PAID = "Partially Paid"

    FULLY_PAID = "Fully Paid"





class PurchaseOrder(SubmittableModel, TenantModel):

    __tablename__ = "purchase_orders"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_purchase_orders_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    title: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    naming_series: Mapped[str] = mapped_column(SAEnum(PurchaseOrderNamingSeries, native_enum=False, length=19, validate_strings=True), nullable=False)

    supplier_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("suppliers.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    supplier = relationship("app.buying.supplier_domain.models.supplier.Supplier", foreign_keys=[supplier_id])

    supplier_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    company: Mapped[str] = mapped_column(String(140), nullable=False)

    transaction_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    schedule_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    order_confirmation_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    order_confirmation_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("purchase_orders.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("app.buying.purchase_order_domain.models.purchase_order.PurchaseOrder", foreign_keys=[amended_from_id])

    customer: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    customer_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    customer_contact_person: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    customer_contact_display: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    customer_contact_mobile: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    customer_contact_email: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    supplier_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    contact_person: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    address_display: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    contact_display: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    contact_mobile: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    contact_email: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    shipping_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    shipping_address_display: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    currency: Mapped[str] = mapped_column(String(140), nullable=False)

    conversion_rate: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    buying_price_list_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("price_lists.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    buying_price_list = relationship("app.stock.price_list_domain.models.price_list.PriceList", foreign_keys=[buying_price_list_id])

    price_list_currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    plc_conversion_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    ignore_pricing_rule: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    set_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    set_warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[set_warehouse_id])

    is_subcontracted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    supplier_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    supplier_warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[supplier_warehouse_id])

    scan_barcode: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    total_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_net_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    net_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_net_weight: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    taxes_and_charges_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("purchase_taxes_and_charges_templates.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    taxes_and_charges = relationship("app.accounts.purchase_taxes_and_charges_template_domain.models.purchase_taxes_and_charges_template.PurchaseTaxesAndChargesTemplate", foreign_keys=[taxes_and_charges_id])

    shipping_rule_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("shipping_rules.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    shipping_rule = relationship("app.accounts.shipping_rule_domain.models.shipping_rule.ShippingRule", foreign_keys=[shipping_rule_id])

    other_charges_calculation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    base_taxes_and_charges_added: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_taxes_and_charges_deducted: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_total_taxes_and_charges: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    taxes_and_charges_added: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    taxes_and_charges_deducted: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_taxes_and_charges: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    apply_discount_on: Mapped[Optional[str]] = mapped_column(SAEnum(PurchaseOrderApplyDiscountOn, native_enum=False, length=15, validate_strings=True), nullable=True)

    base_discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    additional_discount_percentage: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_grand_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_rounding_adjustment: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_in_words: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    base_rounded_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    grand_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rounding_adjustment: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rounded_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    disable_rounded_total: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    in_words: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    advance_paid: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    payment_terms_template_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("payment_terms_templates.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    payment_terms_template = relationship("app.accounts.payment_terms_template_domain.models.payment_terms_template.PaymentTermsTemplate", foreign_keys=[payment_terms_template_id])

    tc_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    terms: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    status: Mapped[str] = mapped_column(SAEnum(PurchaseOrderStatus, native_enum=False, length=23, validate_strings=True), nullable=False)

    ref_sq_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("supplier_quotations.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    ref_sq = relationship("app.buying.supplier_quotation_domain.models.supplier_quotation.SupplierQuotation", foreign_keys=[ref_sq_id])

    party_account_currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    inter_company_order_reference: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    per_received: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    per_billed: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    letter_head: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    select_print_heading: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    group_same_items: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    language: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    from_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    to_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    auto_repeat: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    tax_category_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("tax_categories.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    tax_category = relationship("app.accounts.tax_category_domain.models.tax_category.TaxCategory", foreign_keys=[tax_category_id])

    set_reserve_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    set_reserve_warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[set_reserve_warehouse_id])

    billing_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    billing_address_display: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    is_internal_supplier: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    represents_company: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("app.accounts.cost_center_domain.models.cost_center.CostCenter", foreign_keys=[cost_center_id])

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    set_from_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    set_from_warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[set_from_warehouse_id])

    incoterm: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    named_place: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    advance_payment_status: Mapped[Optional[str]] = mapped_column(SAEnum(PurchaseOrderAdvancePaymentStatus, native_enum=False, length=18, validate_strings=True), nullable=True)

    has_unit_price_items: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    dispatch_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    dispatch_address_display: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    supplier_group: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    last_scanned_warehouse: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    mps: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    transaction_time: Mapped[Optional[dt.time]] = mapped_column(Time, nullable=True)



    items: Mapped[list["PurchaseOrderItem"]] = relationship(  # noqa: F821

        "PurchaseOrderItem",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[PurchaseOrderItem.parent_id]",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PurchaseOrder id={self.id}>"
