"""

Item Price -- converted from ``erpnext/stock/doctype/item_price``.

"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel



__all__ = ["ItemPrice"]







class ItemPrice(TenantModel):

    __tablename__ = "item_prices"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_item_prices_business_name"),

    )



    #: ``autoname`` = 'hash'.

    #: Upstream ``autoname = 'hash'``: Frappe assigns an opaque random hash.

    #: There is no content to hash here, so a UUID4 is the faithful

    #: equivalent -- unique, opaque, and not user-visible. Without a

    #: default the column is NOT NULL and every insert fails.

    name: Mapped[str] = mapped_column(

        String(140), nullable=False, default=lambda: uuid.uuid4().hex

    )



    item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    item_code = relationship("Item", foreign_keys=[item_code_id])

    uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    uom = relationship("Uom", foreign_keys=[uom_id])

    packing_unit: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0)

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    brand_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("brands.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    brand = relationship("Brand", foreign_keys=[brand_id])

    item_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    price_list_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("price_lists.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    price_list = relationship("PriceList", foreign_keys=[price_list_id])

    customer: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    supplier: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    buying: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    selling: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    price_list_rate: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    valid_from: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    lead_time_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0)

    valid_upto: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    reference: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    batch_no_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("batches.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    batch_no = relationship("Batch", foreign_keys=[batch_no_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ItemPrice id={self.id}>"
