"""

Stock Closing Balance -- converted from ``erpnext/stock/doctype/stock_closing_balance``.

"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, Text, Time, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel



__all__ = ["StockClosingBalance"]







class StockClosingBalance(TenantModel):

    __tablename__ = "stock_closing_balances"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_stock_closing_balances_business_name"),

    )



    #: Upstream declares no ``autoname``; Frappe mints a hash.

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

    posting_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    posting_time: Mapped[Optional[dt.time]] = mapped_column(Time, nullable=True)

    posting_datetime: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)

    actual_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    valuation_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    stock_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    company: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    stock_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    stock_uom = relationship("Uom", foreign_keys=[stock_uom_id])

    stock_value_difference: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    item_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("item_groups.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item_group = relationship("ItemGroup", foreign_keys=[item_group_id])

    stock_closing_entry_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("stock_closing_entrys.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    stock_closing_entry = relationship("StockClosingEntry", foreign_keys=[stock_closing_entry_id])

    inventory_dimension_key: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    batch_no_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("batchs.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    batch_no = relationship("Batch", foreign_keys=[batch_no_id])

    fifo_queue: Mapped[Optional[str]] = mapped_column(Text, nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<StockClosingBalance id={self.id}>"
