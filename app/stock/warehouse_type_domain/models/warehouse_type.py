"""

Warehouse Type -- converted from ``erpnext/stock/doctype/warehouse_type``.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["WarehouseType"]







class WarehouseType(TenantModel):

    __tablename__ = "warehouse_types"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_warehouse_types_business_name"),

    )



    #: ``autoname`` = 'Prompt' -- the client supplies the name.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    description: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<WarehouseType id={self.id}>"
