"""

POS Opening Entry -- converted from ``erpnext/accounts/doctype/pos_opening_entry``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, DateTime, Enum as SAEnum, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.pos_opening_entry_detail_domain.models.pos_opening_entry_detail import POSOpeningEntryDetail



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["POSOpeningEntry", "POSOpeningEntryStatus"]







class POSOpeningEntryStatus(str, enum.Enum):

    DRAFT = "Draft"

    OPEN = "Open"

    CLOSED = "Closed"

    CANCELLED = "Cancelled"









class POSOpeningEntry(SubmittableModel, TenantModel):

    __tablename__ = "pos_opening_entries"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_pos_opening_entries_business_name"),

    )



    #: ``autoname`` = 'POS-OPE-.YYYY.-.#####'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    period_start_date: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)

    period_end_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    posting_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    pos_profile: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    user: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    amended_from: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    set_posting_date: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    status: Mapped[Optional[POSOpeningEntryStatus]] = mapped_column(

        SAEnum(POSOpeningEntryStatus, native_enum=False, length=9, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    pos_closing_entry: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    balance_details = relationship(

        POSOpeningEntryDetail,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=POSOpeningEntryDetail.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<POSOpeningEntry id={self.id}>"
