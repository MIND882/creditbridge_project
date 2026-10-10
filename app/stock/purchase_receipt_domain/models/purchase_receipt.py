"""

Purchase Receipt -- converted from ``erpnext/stock/doctype/purchase_receipt``.



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



from app.stock.purchase_receipt_item_domain.models.purchase_receipt_item import PurchaseReceiptItem



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["PurchaseReceipt", "PurchaseReceiptNamingSeries", "PurchaseReceiptApplyDiscountOn", "PurchaseReceiptStatus"]





class PurchaseReceiptNamingSeries(str, enum.Enum):

    MAT_PRE_YYYY = "MAT-PRE-.YYYY.-"

    MAT_PR_RET_YYYY = "MAT-PR-RET-.YYYY.-"



class PurchaseReceiptApplyDiscountOn(str, enum.Enum):

    GRAND_TOTAL = "Grand Total"

    NET_TOTAL = "Net Total"



class PurchaseReceiptStatus(str, enum.Enum):

    DRAFT = "Draft"

    PARTLY_BILLED = "Partly Billed"

    TO_BILL = "To Bill"

    COMPLETED = "Completed"

    RETURN = "Return"

    RETURN_ISSUED = "Return Issued"

    CANCELLED = "Cancelled"

    CLOSED = "Closed"





class PurchaseReceipt(SubmittableModel, TenantModel):

    __tablename__ = "purchase_receipts"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_purchase_receipts_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    title: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    naming_series: Mapped[str] = mapped_column(SAEnum(PurchaseReceiptNamingSeries, native_enum=False, length=22, validate_strings=True), nullable=False)

    supplier: Mapped[str] = mapped_column(String(140), nullable=False)

    supplier_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    supplier_delivery_note: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    posting_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    posting_time: Mapped[dt.time] = mapped_column(Time, nullable=False)

    set_posting_time: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    company: Mapped[str] = mapped_column(String(140), nullable=False)

    is_return: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    return_against_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("purchase_receipts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    return_against = relationship("PurchaseReceipt", foreign_keys=[return_against_id])

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

    buying_price_list = relationship("PriceList", foreign_keys=[buying_price_list_id])

    price_list_currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    plc_conversion_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    ignore_pricing_rule: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    set_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    set_warehouse = relationship("Warehouse", foreign_keys=[set_warehouse_id])

    rejected_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    rejected_warehouse = relationship("Warehouse", foreign_keys=[rejected_warehouse_id])

    is_subcontracted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    supplier_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    supplier_warehouse = relationship("Warehouse", foreign_keys=[supplier_warehouse_id])

    total_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_net_total: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    net_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_net_weight: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    tax_category_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("tax_categories.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    tax_category = relationship("TaxCategory", foreign_keys=[tax_category_id])

    shipping_rule_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("shipping_rules.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    shipping_rule = relationship("ShippingRule", foreign_keys=[shipping_rule_id])

    taxes_and_charges_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("purchase_taxes_and_charges_templates.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    taxes_and_charges = relationship("PurchaseTaxesAndChargesTemplate", foreign_keys=[taxes_and_charges_id])

    other_charges_calculation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    base_taxes_and_charges_added: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_taxes_and_charges_deducted: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_total_taxes_and_charges: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    taxes_and_charges_added: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    taxes_and_charges_deducted: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_taxes_and_charges: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    apply_discount_on: Mapped[Optional[str]] = mapped_column(SAEnum(PurchaseReceiptApplyDiscountOn, native_enum=False, length=15, validate_strings=True), nullable=True)

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

    in_words: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    disable_rounded_total: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    tc_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    terms: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    status: Mapped[str] = mapped_column(SAEnum(PurchaseReceiptStatus, native_enum=False, length=17, validate_strings=True), nullable=False)

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("purchase_receipts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("PurchaseReceipt", foreign_keys=[amended_from_id])

    range: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    per_billed: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    auto_repeat: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    letter_head: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    select_print_heading: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    language: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    group_same_items: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    instructions: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    remarks: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    transporter_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    lr_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    lr_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    is_internal_supplier: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    inter_company_reference_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("delivery_notes.id", ondelete="RESTRICT", use_alter=True, name="fk_purchase_receipts_inter_company_reference_id"),

        nullable=True, index=True,

    )

    inter_company_reference = relationship("DeliveryNote", foreign_keys=[inter_company_reference_id])

    scan_barcode: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    billing_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    billing_address_display: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    apply_putaway_rule: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    per_returned: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    set_from_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    set_from_warehouse = relationship("Warehouse", foreign_keys=[set_from_warehouse_id])

    represents_company: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])

    incoterm: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    named_place: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    subcontracting_receipt: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    dispatch_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    dispatch_address_display: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    last_scanned_warehouse: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    items: Mapped[list["PurchaseReceiptItem"]] = relationship(  # noqa: F821

        "PurchaseReceiptItem",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[PurchaseReceiptItem.parent_id]",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PurchaseReceipt id={self.id}>"
