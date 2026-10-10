"""

Delivery Note Item -- converted from ``erpnext/stock/doctype/delivery_note_item``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Delivery Note).

"""



from __future__ import annotations



import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, ForeignKey, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["DeliveryNoteItem", "DeliveryNoteItemMarginType"]





class DeliveryNoteItemMarginType(str, enum.Enum):

    PERCENTAGE = "Percentage"

    AMOUNT = "Amount"





class DeliveryNoteItem(ChildTableModel, TenantModel):

    __tablename__ = "delivery_note_items"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_delivery_note_items_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("delivery_notes.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "DeliveryNote",

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

    is_product_bundle: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    product_bundle: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    item_name: Mapped[str] = mapped_column(String(140), nullable=False)

    customer_item_code: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    image: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    image_view: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    qty: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    stock_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    stock_uom = relationship("Uom", foreign_keys=[stock_uom_id])

    uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    uom = relationship("Uom", foreign_keys=[uom_id])

    conversion_factor: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    stock_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    price_list_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_price_list_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    margin_type: Mapped[Optional[str]] = mapped_column(SAEnum(DeliveryNoteItemMarginType, native_enum=False, length=14, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    margin_rate_or_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rate_with_margin: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    discount_percentage: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_rate_with_margin: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

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

    target_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    target_warehouse = relationship("Warehouse", foreign_keys=[target_warehouse_id])

    quality_inspection_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("quality_inspections.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    quality_inspection = relationship("QualityInspection", foreign_keys=[quality_inspection_id])

    actual_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    actual_batch_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    item_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("item_groups.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item_group = relationship("ItemGroup", foreign_keys=[item_group_id])

    brand_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("brands.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    brand = relationship("Brand", foreign_keys=[brand_id])

    item_tax_rate: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    expense_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    expense_account = relationship("Account", foreign_keys=[expense_account_id])

    item_tax_template_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("item_tax_templates.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item_tax_template = relationship("ItemTaxTemplate", foreign_keys=[item_tax_template_id])

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])

    allow_zero_valuation_rate: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    against_sales_order: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    against_sales_invoice_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("sales_invoices.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    against_sales_invoice = relationship("SalesInvoice", foreign_keys=[against_sales_invoice_id])

    so_detail: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    si_detail: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    installed_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    billed_amt: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    page_break: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    dn_detail: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    returned_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    incoming_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    stock_uom_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    grant_commission: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    pick_list_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    purchase_order: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    purchase_order_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    has_item_scanned: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    material_request_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("material_requests.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    material_request = relationship("MaterialRequest", foreign_keys=[material_request_id])

    material_request_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    received_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    packed_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0)

    serial_and_batch_bundle_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("serial_and_batch_bundles.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    serial_and_batch_bundle = relationship("SerialAndBatchBundle", foreign_keys=[serial_and_batch_bundle_id])

    serial_no: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    batch_no_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("batches.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    batch_no = relationship("Batch", foreign_keys=[batch_no_id])

    use_serial_batch_fields: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    distributed_discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    company_total_stock: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    against_pick_list_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("pick_lists.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    against_pick_list = relationship("PickList", foreign_keys=[against_pick_list_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<DeliveryNoteItem id={self.id}>"
