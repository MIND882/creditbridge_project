"""

Cashier Closing -- converted from ``erpnext/accounts/doctype/cashier_closing``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Date, Enum as SAEnum, Numeric, String, Time, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.cashier_closing_payments_domain.models.cashier_closing_payments import CashierClosingPayments



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["CashierClosing", "CashierClosingNamingSeries"]







class CashierClosingNamingSeries(str, enum.Enum):

    POS_CLO = "POS-CLO-"









class CashierClosing(SubmittableModel, TenantModel):

    __tablename__ = "cashier_closings"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_cashier_closings_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    naming_series: Mapped[Optional[CashierClosingNamingSeries]] = mapped_column(

        SAEnum(CashierClosingNamingSeries, native_enum=False, length=8, validate_strings=True),

        nullable=True,

    )

    user: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    from_time: Mapped[Optional[dt.time]] = mapped_column(Time, nullable=True)

    time: Mapped[Optional[dt.time]] = mapped_column(Time, nullable=True)

    expense: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    custody: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    returns: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    outstanding_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    net_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    amended_from: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    payments = relationship(

        CashierClosingPayments,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=CashierClosingPayments.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<CashierClosing id={self.id}>"
