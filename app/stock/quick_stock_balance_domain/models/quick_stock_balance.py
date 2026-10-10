"""

Quick Stock Balance -- converted from ``erpnext/stock/doctype/quick_stock_balance``.



A Frappe Single (``issingle: 1``): one row per ``business_id``, enforced by a unique constraint on ``business_id`` alone.

"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Date, ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel



__all__ = ["QuickStockBalance"]







class QuickStockBalance(TenantModel):

    __tablename__ = "quick_stock_balances"

    __table_args__ = (

        UniqueConstraint("business_id", name="uq_quick_stock_balances_business"),

    )



    warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    warehouse = relationship("Warehouse", foreign_keys=[warehouse_id])

    item_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item = relationship("Item", foreign_keys=[item_id])

    item_barcode: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    item_description: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    value: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    image: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<QuickStockBalance id={self.id}>"
