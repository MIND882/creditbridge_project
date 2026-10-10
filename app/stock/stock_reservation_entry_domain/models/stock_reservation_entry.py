"""

Stock Reservation Entry -- converted from ``erpnext/stock/doctype/stock_reservation_entry``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["StockReservationEntry", "StockReservationEntryVoucherType", "StockReservationEntryStatus", "StockReservationEntryReservationBasedOn", "StockReservationEntryFromVoucherType"]





class StockReservationEntryVoucherType(str, enum.Enum):

    SALES_ORDER = "Sales Order"

    WORK_ORDER = "Work Order"

    SUBCONTRACTING_INWARD_ORDER = "Subcontracting Inward Order"

    PRODUCTION_PLAN = "Production Plan"

    SUBCONTRACTING_ORDER = "Subcontracting Order"



class StockReservationEntryStatus(str, enum.Enum):

    DRAFT = "Draft"

    PARTIALLY_RESERVED = "Partially Reserved"

    RESERVED = "Reserved"

    PARTIALLY_DELIVERED = "Partially Delivered"

    PARTIALLY_USED = "Partially Used"

    DELIVERED = "Delivered"

    CANCELLED = "Cancelled"

    CLOSED = "Closed"



class StockReservationEntryReservationBasedOn(str, enum.Enum):

    QTY = "Qty"

    SERIAL_AND_BATCH = "Serial and Batch"



class StockReservationEntryFromVoucherType(str, enum.Enum):

    PICK_LIST = "Pick List"

    PURCHASE_RECEIPT = "Purchase Receipt"

    STOCK_ENTRY = "Stock Entry"

    WORK_ORDER = "Work Order"

    PRODUCTION_PLAN = "Production Plan"

    SUBCONTRACTING_INWARD_ORDER = "Subcontracting Inward Order"





class StockReservationEntry(SubmittableModel, TenantModel):

    __tablename__ = "stock_reservation_entrys"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_stock_reservation_entrys_business_name"),

    )



    #: ``autoname`` = 'MAT-SRE-.YYYY.-.#####'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item_code = relationship("Item", foreign_keys=[item_code_id])

    warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    warehouse = relationship("Warehouse", foreign_keys=[warehouse_id])

    voucher_type: Mapped[Optional[str]] = mapped_column(SAEnum(StockReservationEntryVoucherType, native_enum=False, length=31, validate_strings=True), nullable=True)

    voucher_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    voucher_detail_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    stock_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    stock_uom = relationship("Uom", foreign_keys=[stock_uom_id])

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    company: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    reserved_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    status: Mapped[Optional[str]] = mapped_column(SAEnum(StockReservationEntryStatus, native_enum=False, length=23, validate_strings=True), nullable=True)

    delivered_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0)

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("stock_reservation_entrys.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("StockReservationEntry", foreign_keys=[amended_from_id])

    available_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0)

    voucher_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0)

    has_serial_no: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    has_batch_no: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    reservation_based_on: Mapped[Optional[str]] = mapped_column(SAEnum(StockReservationEntryReservationBasedOn, native_enum=False, length=20, validate_strings=True), nullable=True)

    from_voucher_type: Mapped[Optional[str]] = mapped_column(SAEnum(StockReservationEntryFromVoucherType, native_enum=False, length=31, validate_strings=True), nullable=True)

    from_voucher_detail_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    from_voucher_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    consumed_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    transferred_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<StockReservationEntry id={self.id}>"
