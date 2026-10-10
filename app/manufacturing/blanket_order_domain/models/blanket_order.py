"""

Blanket Order -- converted from ``erpnext/manufacturing/doctype/blanket_order``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from typing import Optional

import uuid



from sqlalchemy import Date, Enum as SAEnum, ForeignKey, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.manufacturing.blanket_order_item_domain.models.blanket_order_item import BlanketOrderItem



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["BlanketOrder", "BlanketOrderNamingSeries", "BlanketOrderBlanketOrderType"]





class BlanketOrderNamingSeries(str, enum.Enum):

    MFG_BLR_YYYY = "MFG-BLR-.YYYY.-"



class BlanketOrderBlanketOrderType(str, enum.Enum):

    SELLING = "Selling"

    PURCHASING = "Purchasing"





class BlanketOrder(SubmittableModel, TenantModel):

    __tablename__ = "blanket_orders"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_blanket_orders_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    naming_series: Mapped[str] = mapped_column(SAEnum(BlanketOrderNamingSeries, native_enum=False, length=19, validate_strings=True), nullable=False)

    blanket_order_type: Mapped[str] = mapped_column(SAEnum(BlanketOrderBlanketOrderType, native_enum=False, length=14, validate_strings=True), nullable=False)

    customer_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("selling_customers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    customer = relationship("app.selling.customer_domain.models.customer.Customer", foreign_keys=[customer_id])

    customer_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    supplier_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("suppliers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    supplier = relationship("app.buying.supplier_domain.models.supplier.Supplier", foreign_keys=[supplier_id])

    supplier_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    order_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    order_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    from_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    to_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    company: Mapped[str] = mapped_column(String(140), nullable=False)

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("blanket_orders.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("app.manufacturing.blanket_order_domain.models.blanket_order.BlanketOrder", foreign_keys=[amended_from_id])

    tc_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    terms: Mapped[Optional[str]] = mapped_column(Text, nullable=True)



    items: Mapped[list["BlanketOrderItem"]] = relationship(  # noqa: F821

        "app.manufacturing.blanket_order_item_domain.models.blanket_order_item.BlanketOrderItem",

        back_populates="parent",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        cascade="all, delete-orphan",

        foreign_keys=[BlanketOrderItem.parent_id],

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<BlanketOrder id={self.id}>"
