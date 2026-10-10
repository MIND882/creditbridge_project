"""

Item Standard Cost -- converted from ``erpnext/stock/doctype/item_standard_cost``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Date, Enum as SAEnum, ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["ItemStandardCost", "ItemStandardCostNamingSeries"]





class ItemStandardCostNamingSeries(str, enum.Enum):

    ISC_YYYY = "ISC-.YYYY.-"





class ItemStandardCost(SubmittableModel, TenantModel):

    __tablename__ = "item_standard_costs"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_item_standard_costs_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    naming_series: Mapped[str] = mapped_column(SAEnum(ItemStandardCostNamingSeries, native_enum=False, length=15, validate_strings=True), nullable=False)

    item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    item_code = relationship("Item", foreign_keys=[item_code_id])

    company: Mapped[str] = mapped_column(String(140), nullable=False)

    standard_rate: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    effective_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    revaluation_entry_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("stock_reconciliations.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    revaluation_entry = relationship("StockReconciliation", foreign_keys=[revaluation_entry_id])

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("item_standard_costs.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("ItemStandardCost", foreign_keys=[amended_from_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ItemStandardCost id={self.id}>"
