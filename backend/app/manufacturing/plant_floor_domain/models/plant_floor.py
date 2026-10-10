"""

Plant Floor -- converted from ``erpnext/manufacturing/doctype/plant_floor``.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel



__all__ = ["PlantFloor"]







class PlantFloor(TenantModel):

    __tablename__ = "plant_floors"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_plant_floors_business_name"),

    )



    #: ``autoname`` = 'field:floor_name' -- derived in the service at create time.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    floor_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    company: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[warehouse_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PlantFloor id={self.id}>"
