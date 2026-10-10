"""

Stock Ledger Entry -- converted from ``erpnext/stock/doctype/stock_ledger_entry``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Numeric, String, Text, Time, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["StockLedgerEntry"]







class StockLedgerEntry(SubmittableModel, TenantModel):

    __tablename__ = "stock_ledger_entries"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_stock_ledger_entrys_business_name"),

    )



    #: ``autoname`` = 'MAT-SLE-.YYYY.-.#####'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item_code = relationship("Item", foreign_keys=[item_code_id])

    serial_no: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    batch_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    warehouse = relationship("Warehouse", foreign_keys=[warehouse_id])

    posting_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    posting_time: Mapped[Optional[dt.time]] = mapped_column(Time, nullable=True)

    voucher_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    voucher_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    voucher_detail_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    actual_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    incoming_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    outgoing_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    stock_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    stock_uom = relationship("Uom", foreign_keys=[stock_uom_id])

    qty_after_transaction: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    valuation_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    stock_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    stock_value_difference: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    stock_queue: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    company: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    fiscal_year: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_cancelled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    to_rename: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    dependant_sle_voucher_detail_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    recalculate_rate: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    serial_and_batch_bundle_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("serial_and_batch_bundles.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    serial_and_batch_bundle = relationship("SerialAndBatchBundle", foreign_keys=[serial_and_batch_bundle_id])

    has_batch_no: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    has_serial_no: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    is_adjustment_entry: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    auto_created_serial_and_batch_bundle: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    posting_datetime: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<StockLedgerEntry id={self.id}>"
