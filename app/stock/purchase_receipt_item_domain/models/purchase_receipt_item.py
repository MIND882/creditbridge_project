"""

Purchase Receipt Item -- converted from ``erpnext/stock/doctype/purchase_receipt_item``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Purchase Receipt).

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, Enum as SAEnum, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["PurchaseReceiptItem", "PurchaseReceiptItemMarginType"]





class PurchaseReceiptItemMarginType(str, enum.Enum):

    PERCENTAGE = "Percentage"

    AMOUNT = "Amount"





class PurchaseReceiptItem(ChildTableModel, TenantModel):

    __tablename__ = "purchase_receipt_items"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_purchase_receipt_items_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("purchase_receipts.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "PurchaseReceipt",

        back_populates="items",

        # explicit: a child can carry a second FK to its own parent

        # (item_variant_attribute.variant_of -> items), which would

        # otherwise make the join ambiguous

        foreign_keys=[parent_id],

    )



    #: ``autoname`` = 'hash'.

    #: Upstream ``autoname = 'hash'``: Frappe assigns an opaque random hash.

    #: There is no content to hash here, so a UUID4 is the faithful

    #: equivalent -- unique, opaque, and not user-visible. Without a

    #: default the column is NOT NULL and every insert fails.

    name: Mapped[str] = mapped_column(

        String(140), nullable=False, default=lambda: uuid.uuid4().hex

    )



    barcode: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    item_code = relationship("Item", foreign_keys=[item_code_id])

    supplier_part_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    item_name: Mapped[str] = mapped_column(String(140), nullable=False)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    image: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    image_view: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    received_qty: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rejected_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    uom = relationship("Uom", foreign_keys=[uom_id])

    stock_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    stock_uom = relationship("Uom", foreign_keys=[stock_uom_id])

    conversion_factor: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    retain_sample: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    sample_quantity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    price_list_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    discount_percentage: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_price_list_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_rate: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    base_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    pricing_rules: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_free_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    net_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    net_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_net_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_net_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    weight_per_unit: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_weight: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    weight_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    weight_uom = relationship("Uom", foreign_keys=[weight_uom_id])

    warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    warehouse = relationship("Warehouse", foreign_keys=[warehouse_id])

    rejected_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    rejected_warehouse = relationship("Warehouse", foreign_keys=[rejected_warehouse_id])

    quality_inspection_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("quality_inspections.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    quality_inspection = relationship("QualityInspection", foreign_keys=[quality_inspection_id])

    is_fixed_asset: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    purchase_order: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    schedule_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    stock_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    item_tax_template_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("item_tax_templates.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item_tax_template = relationship("ItemTaxTemplate", foreign_keys=[item_tax_template_id])

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])

    purchase_order_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    allow_zero_valuation_rate: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    billed_amt: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    landed_cost_voucher_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    brand_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("brands.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    brand = relationship("Brand", foreign_keys=[brand_id])

    item_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("item_groups.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item_group = relationship("ItemGroup", foreign_keys=[item_group_id])

    rm_supp_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    item_tax_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    valuation_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    item_tax_rate: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    page_break: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    material_request_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("material_requests.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    material_request = relationship("MaterialRequest", foreign_keys=[material_request_id])

    material_request_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    expense_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    expense_account = relationship("Account", foreign_keys=[expense_account_id])

    manufacturer_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("manufacturers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    manufacturer = relationship("Manufacturer", foreign_keys=[manufacturer_id])

    manufacturer_part_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    asset_location: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    asset_category: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    from_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    from_warehouse = relationship("Warehouse", foreign_keys=[from_warehouse_id])

    purchase_receipt_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    putaway_rule_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("putaway_rules.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    putaway_rule = relationship("PutawayRule", foreign_keys=[putaway_rule_id])

    returned_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    received_stock_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    stock_uom_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    delivery_note_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    margin_type: Mapped[Optional[str]] = mapped_column(SAEnum(PurchaseReceiptItemMarginType, native_enum=False, length=14, validate_strings=True), nullable=True)

    margin_rate_or_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rate_with_margin: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_rate_with_margin: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    purchase_invoice_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("purchase_invoices.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    purchase_invoice = relationship("PurchaseInvoice", foreign_keys=[purchase_invoice_id])

    purchase_invoice_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    product_bundle: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    provisional_expense_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    provisional_expense_account = relationship("Account", foreign_keys=[provisional_expense_account_id])

    has_item_scanned: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    serial_and_batch_bundle_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("serial_and_batch_bundles.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    serial_and_batch_bundle = relationship("SerialAndBatchBundle", foreign_keys=[serial_and_batch_bundle_id])

    serial_no: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    rejected_serial_no: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    batch_no_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("batchs.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    batch_no = relationship("Batch", foreign_keys=[batch_no_id])

    rejected_serial_and_batch_bundle_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("serial_and_batch_bundles.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    rejected_serial_and_batch_bundle = relationship("SerialAndBatchBundle", foreign_keys=[rejected_serial_and_batch_bundle_id])

    wip_composite_asset: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    sales_order: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    sales_order_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    subcontracting_receipt_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    use_serial_batch_fields: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    return_qty_from_rejected_warehouse: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    sales_incoming_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    distributed_discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    amount_difference_with_purchase_invoice: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PurchaseReceiptItem id={self.id}>"
