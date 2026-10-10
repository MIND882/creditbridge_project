"""

Shipment Parcel Template -- converted from ``erpnext/stock/doctype/shipment_parcel_template``.

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["ShipmentParcelTemplate"]







class ShipmentParcelTemplate(TenantModel):

    __tablename__ = "shipment_parcel_templates"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_shipment_parcel_templates_business_name"),

    )



    #: ``autoname`` = 'field:parcel_template_name' -- derived in the service at create time.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    length: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    width: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    height: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    weight: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    parcel_template_name: Mapped[str] = mapped_column(String(140), nullable=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ShipmentParcelTemplate id={self.id}>"
