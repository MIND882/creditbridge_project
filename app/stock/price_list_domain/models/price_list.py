"""

Price List -- converted from ``erpnext/stock/doctype/price_list``.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import Boolean, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.stock.price_list_country_domain.models.price_list_country import PriceListCountry



from app.core.base_model import TenantModel



__all__ = ["PriceList"]







class PriceList(TenantModel):

    __tablename__ = "price_lists"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_price_lists_business_name"),

    )



    #: ``autoname`` = 'field:price_list_name' -- derived in the service at create time.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    price_list_name: Mapped[str] = mapped_column(String(140), nullable=False)

    currency: Mapped[str] = mapped_column(String(140), nullable=False)

    buying: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    selling: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    price_not_uom_dependent: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    countries: Mapped[list["PriceListCountry"]] = relationship(  # noqa: F821

        "PriceListCountry",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[PriceListCountry.parent_id]",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PriceList id={self.id}>"
