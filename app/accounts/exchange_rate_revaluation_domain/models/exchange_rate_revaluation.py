"""

Exchange Rate Revaluation -- converted from ``erpnext/accounts/doctype/exchange_rate_revaluation``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Date, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.exchange_rate_revaluation_account_domain.models.exchange_rate_revaluation_account import ExchangeRateRevaluationAccount



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["ExchangeRateRevaluation"]







class ExchangeRateRevaluation(SubmittableModel, TenantModel):

    __tablename__ = "exchange_rate_revaluations"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_exchange_rate_revaluations_business_name"),

    )



    #: ``autoname`` = 'ACC-ERR-.YYYY.-.#####'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    posting_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    amended_from: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    gain_loss_unbooked: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    gain_loss_booked: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_gain_loss: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rounding_loss_allowance: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    accounts = relationship(

        ExchangeRateRevaluationAccount,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=ExchangeRateRevaluationAccount.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ExchangeRateRevaluation id={self.id}>"
