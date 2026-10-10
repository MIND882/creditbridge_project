"""

Bin -- converted from ``erpnext/stock/doctype/bin``.

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel



__all__ = ["Bin"]







class Bin(TenantModel):

    __tablename__ = "bins"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_bins_business_name"),

    )



    #: ``autoname`` = 'hash'.

    #: Upstream ``autoname = 'hash'``: Frappe assigns an opaque random hash.

    #: There is no content to hash here, so a UUID4 is the faithful

    #: equivalent -- unique, opaque, and not user-visible. Without a

    #: default the column is NOT NULL and every insert fails.

    name: Mapped[str] = mapped_column(

        String(140), nullable=False, default=lambda: uuid.uuid4().hex

    )



    warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    warehouse = relationship("Warehouse", foreign_keys=[warehouse_id])

    item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    item_code = relationship("Item", foreign_keys=[item_code_id])

    reserved_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0.0)

    actual_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0.0)

    ordered_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0.0)

    indented_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0.0)

    planned_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    projected_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    reserved_qty_for_production: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    reserved_qty_for_sub_contract: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    stock_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    stock_uom = relationship("Uom", foreign_keys=[stock_uom_id])

    company: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    valuation_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    stock_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    reserved_qty_for_production_plan: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    reserved_stock: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<Bin id={self.id}>"
