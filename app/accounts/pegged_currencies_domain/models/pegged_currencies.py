"""

Pegged Currencies -- converted from ``erpnext/accounts/doctype/pegged_currencies``.





"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.pegged_currency_details_domain.models.pegged_currency_details import PeggedCurrencyDetails



from app.core.base_model import TenantModel



__all__ = ["PeggedCurrencies"]







class PeggedCurrencies(TenantModel):

    __tablename__ = "pegged_currencies"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_pegged_currencies_business_name"),

    )



    #: Upstream declares no ``autoname``; Frappe mints a hash.

    name: Mapped[str] = mapped_column(String(140), nullable=False)





    pegged_currency_item = relationship(

        PeggedCurrencyDetails,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=PeggedCurrencyDetails.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PeggedCurrencies id={self.id}>"
