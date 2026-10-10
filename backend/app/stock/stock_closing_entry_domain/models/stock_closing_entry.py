"""

Stock Closing Entry -- converted from ``erpnext/stock/doctype/stock_closing_entry``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from typing import Optional

import uuid



from sqlalchemy import Date, Enum as SAEnum, ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["StockClosingEntry", "StockClosingEntryNamingSeries", "StockClosingEntryStatus"]





class StockClosingEntryNamingSeries(str, enum.Enum):

    CBAL = "CBAL-.#####"



class StockClosingEntryStatus(str, enum.Enum):

    DRAFT = "Draft"

    QUEUED = "Queued"

    IN_PROGRESS = "In Progress"

    COMPLETED = "Completed"

    FAILED = "Failed"

    CANCELLED = "Cancelled"





class StockClosingEntry(SubmittableModel, TenantModel):

    __tablename__ = "stock_closing_entries"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_stock_closing_entrys_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    naming_series: Mapped[Optional[str]] = mapped_column(SAEnum(StockClosingEntryNamingSeries, native_enum=False, length=15, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    company: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    status: Mapped[Optional[str]] = mapped_column(SAEnum(StockClosingEntryStatus, native_enum=False, length=15, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    from_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    to_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("stock_closing_entries.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("StockClosingEntry", foreign_keys=[amended_from_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<StockClosingEntry id={self.id}>"
