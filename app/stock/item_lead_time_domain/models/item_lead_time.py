"""

Item Lead Time -- converted from ``erpnext/stock/doctype/item_lead_time``.

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import ForeignKey, Integer, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel



__all__ = ["ItemLeadTime"]







class ItemLeadTime(TenantModel):

    __tablename__ = "item_lead_times"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_item_lead_times_business_name"),

    )



    #: ``autoname`` = 'field:item_code' -- derived in the service at create time.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item_code = relationship("Item", foreign_keys=[item_code_id])

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    buffer_time: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    no_of_shift: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=1)

    manufacturing_time_in_mins: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    total_workstation_time: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    daily_yield: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=90)

    capacity_per_day: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    no_of_units_produced: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    purchase_time: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    shift_time_in_hours: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    no_of_workstations: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    stock_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    stock_uom = relationship("Uom", foreign_keys=[stock_uom_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ItemLeadTime id={self.id}>"
