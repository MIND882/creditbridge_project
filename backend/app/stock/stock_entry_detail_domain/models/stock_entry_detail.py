"""

Stock Entry Detail -- converted from ``erpnext/stock/doctype/stock_entry_detail``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Stock Entry).

"""



from __future__ import annotations



import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["StockEntryDetail", "StockEntryDetailSecondaryItemType"]





class StockEntryDetailSecondaryItemType(str, enum.Enum):

    CO_PRODUCT = "Co-Product"

    BY_PRODUCT = "By-Product"

    SCRAP = "Scrap"

    ADDITIONAL_FINISHED_GOOD = "Additional Finished Good"





class StockEntryDetail(ChildTableModel, TenantModel):

    __tablename__ = "stock_entry_details"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_stock_entry_details_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("stock_entries.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "StockEntry",

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

    s_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    s_warehouse = relationship("Warehouse", foreign_keys=[s_warehouse_id])

    t_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    t_warehouse = relationship("Warehouse", foreign_keys=[t_warehouse_id])

    item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    item_code = relationship("Item", foreign_keys=[item_code_id])

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    image: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    image_view: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    qty: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    basic_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    basic_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    additional_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    valuation_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    uom = relationship("Uom", foreign_keys=[uom_id])

    conversion_factor: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    stock_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    stock_uom = relationship("Uom", foreign_keys=[stock_uom_id])

    transfer_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    retain_sample: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    sample_quantity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    serial_no: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    batch_no_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("batches.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    batch_no = relationship("Batch", foreign_keys=[batch_no_id])

    quality_inspection_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("quality_inspections.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    quality_inspection = relationship("QualityInspection", foreign_keys=[quality_inspection_id])

    expense_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    expense_account = relationship("Account", foreign_keys=[expense_account_id])

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])

    allow_zero_valuation_rate: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    actual_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    bom_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    allow_alternative_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    material_request_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("material_requests.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    material_request = relationship("MaterialRequest", foreign_keys=[material_request_id])

    material_request_item_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("material_request_items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    material_request_item = relationship("MaterialRequestItem", foreign_keys=[material_request_item_id])

    pick_list_item_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("pick_list_items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    pick_list_item = relationship("PickListItem", foreign_keys=[pick_list_item_id])

    original_item_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    original_item = relationship("Item", foreign_keys=[original_item_id])

    subcontracted_item_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    subcontracted_item = relationship("Item", foreign_keys=[subcontracted_item_id])

    against_stock_entry_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("stock_entries.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    against_stock_entry = relationship("StockEntry", foreign_keys=[against_stock_entry_id])

    ste_detail: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    transferred_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    item_group: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    reference_purchase_receipt_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("purchase_receipts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    reference_purchase_receipt = relationship("PurchaseReceipt", foreign_keys=[reference_purchase_receipt_id])

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    po_detail: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    sco_rm_detail: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    set_basic_rate_manually: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    putaway_rule_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("putaway_rules.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    putaway_rule = relationship("PutawayRule", foreign_keys=[putaway_rule_id])

    is_finished_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    job_card_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    has_item_scanned: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    serial_and_batch_bundle_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("serial_and_batch_bundles.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    serial_and_batch_bundle = relationship("SerialAndBatchBundle", foreign_keys=[serial_and_batch_bundle_id])

    use_serial_batch_fields: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    landed_cost_voucher_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    customer_provided_item_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    scio_detail: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    against_fg: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    secondary_item_type: Mapped[Optional[str]] = mapped_column(SAEnum(StockEntryDetailSecondaryItemType, native_enum=False, length=28, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    bom_secondary_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_legacy_scrap_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<StockEntryDetail id={self.id}>"
