"""

Batch -- converted from ``erpnext/stock/doctype/batch``.

"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel



__all__ = ["Batch"]







class Batch(TenantModel):

    __tablename__ = "batchs"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_batchs_business_name"),

    )



    #: ``autoname`` = 'field:batch_id' -- derived in the service at create time.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    batch_id: Mapped[str] = mapped_column(String(140), nullable=False)

    item_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    item = relationship("Item", foreign_keys=[item_id])

    image: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    parent_batch_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("batchs.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    parent_batch = relationship("Batch", foreign_keys=[parent_batch_id])

    manufacturing_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    expiry_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    supplier: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    reference_doctype: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    reference_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    description: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    batch_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    stock_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    stock_uom = relationship("Uom", foreign_keys=[stock_uom_id])

    qty_to_produce: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    produced_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    use_batchwise_valuation: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    allow_negative_stock_for_batch: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<Batch id={self.id}>"
