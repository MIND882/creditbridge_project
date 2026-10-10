"""

Putaway Rule -- converted from ``erpnext/stock/doctype/putaway_rule``.

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel



__all__ = ["PutawayRule"]







class PutawayRule(TenantModel):

    __tablename__ = "putaway_rules"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_putaway_rules_business_name"),

    )



    #: ``autoname`` = 'PUT-.####'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    item_code = relationship("Item", foreign_keys=[item_code_id])

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    warehouse = relationship("Warehouse", foreign_keys=[warehouse_id])

    capacity: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    stock_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    stock_uom = relationship("Uom", foreign_keys=[stock_uom_id])

    priority: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=1)

    company: Mapped[str] = mapped_column(String(140), nullable=False)

    disable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    uom = relationship("Uom", foreign_keys=[uom_id])

    stock_capacity: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    conversion_factor: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=1)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PutawayRule id={self.id}>"
