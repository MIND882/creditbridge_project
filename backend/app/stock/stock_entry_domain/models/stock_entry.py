"""

Stock Entry -- converted from ``erpnext/stock/doctype/stock_entry``.



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



from app.stock.stock_entry_detail_domain.models.stock_entry_detail import StockEntryDetail



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["StockEntry", "StockEntryNamingSeries", "StockEntryPurpose", "StockEntryIsOpening"]





class StockEntryNamingSeries(str, enum.Enum):

    MAT_STE_YYYY = "MAT-STE-.YYYY.-"



class StockEntryPurpose(str, enum.Enum):

    MATERIAL_ISSUE = "Material Issue"

    MATERIAL_RECEIPT = "Material Receipt"

    MATERIAL_TRANSFER = "Material Transfer"

    MATERIAL_TRANSFER_FOR_MANUFACTURE = "Material Transfer for Manufacture"

    MATERIAL_CONSUMPTION_FOR_MANUFACTURE = "Material Consumption for Manufacture"

    MANUFACTURE = "Manufacture"

    REPACK = "Repack"

    SEND_TO_SUBCONTRACTOR = "Send to Subcontractor"

    DISASSEMBLE = "Disassemble"

    RECEIVE_FROM_CUSTOMER = "Receive from Customer"

    RETURN_RAW_MATERIAL_TO_CUSTOMER = "Return Raw Material to Customer"

    SUBCONTRACTING_DELIVERY = "Subcontracting Delivery"

    SUBCONTRACTING_RETURN = "Subcontracting Return"



class StockEntryIsOpening(str, enum.Enum):

    NO = "No"

    YES = "Yes"





class StockEntry(SubmittableModel, TenantModel):

    __tablename__ = "stock_entries"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_stock_entrys_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    naming_series: Mapped[str] = mapped_column(SAEnum(StockEntryNamingSeries, native_enum=False, length=19, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=False)

    stock_entry_type_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("stock_entry_types.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    stock_entry_type = relationship("StockEntryType", foreign_keys=[stock_entry_type_id])

    outgoing_stock_entry_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("stock_entries.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    outgoing_stock_entry = relationship("StockEntry", foreign_keys=[outgoing_stock_entry_id])

    source_stock_entry_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("stock_entries.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    source_stock_entry = relationship("StockEntry", foreign_keys=[source_stock_entry_id])

    purpose: Mapped[Optional[str]] = mapped_column(SAEnum(StockEntryPurpose, native_enum=False, length=40, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    company: Mapped[str] = mapped_column(String(140), nullable=False)

    work_order: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    purchase_order: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    subcontracting_order: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    delivery_note_no_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("delivery_notes.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    delivery_note_no = relationship("DeliveryNote", foreign_keys=[delivery_note_no_id])

    sales_invoice_no_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("sales_invoices.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    sales_invoice_no = relationship("SalesInvoice", foreign_keys=[sales_invoice_no_id])

    purchase_receipt_no_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("purchase_receipts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    purchase_receipt_no = relationship("PurchaseReceipt", foreign_keys=[purchase_receipt_no_id])

    posting_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    posting_time: Mapped[Optional[dt.time]] = mapped_column(Time, nullable=True)

    set_posting_time: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    inspection_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    from_bom: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    bom_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    fg_completed_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    use_multi_level_bom: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    from_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    from_warehouse = relationship("Warehouse", foreign_keys=[from_warehouse_id])

    source_warehouse_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    source_address_display: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    to_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    to_warehouse = relationship("Warehouse", foreign_keys=[to_warehouse_id])

    target_warehouse_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    target_address_display: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    scan_barcode: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    total_incoming_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_outgoing_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    value_difference: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_additional_costs: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    supplier: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    supplier_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    supplier_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    address_display: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    select_print_heading: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    letter_head: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_opening: Mapped[Optional[str]] = mapped_column(SAEnum(StockEntryIsOpening, native_enum=False, length=7, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    remarks: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    per_transferred: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    job_card: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("stock_entries.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("StockEntry", foreign_keys=[amended_from_id])

    credit_note_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("journal_entries.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    credit_note = relationship("JournalEntry", foreign_keys=[credit_note_id])

    pick_list_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("pick_lists.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    pick_list = relationship("PickList", foreign_keys=[pick_list_id])

    add_to_transit: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    apply_putaway_rule: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    is_return: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    process_loss_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    process_loss_percentage: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    asset_repair: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    last_scanned_warehouse: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_additional_transfer_entry: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    subcontracting_inward_order: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])



    items: Mapped[list["StockEntryDetail"]] = relationship(  # noqa: F821

        "StockEntryDetail",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[StockEntryDetail.parent_id]",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<StockEntry id={self.id}>"
