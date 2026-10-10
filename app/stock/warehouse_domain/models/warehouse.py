"""

Warehouse -- converted from ``erpnext/stock/doctype/warehouse``.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import Boolean, ForeignKey, Integer, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel



__all__ = ["Warehouse"]







class Warehouse(TenantModel):

    __tablename__ = "warehouses"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_warehouses_business_name"),

    )



    #: Upstream declares no ``autoname``; Frappe mints a hash.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    warehouse_name: Mapped[str] = mapped_column(String(140), nullable=False)

    is_group: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    company: Mapped[str] = mapped_column(String(140), nullable=False)

    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    account = relationship("Account", foreign_keys=[account_id])

    email_id: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    phone_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    mobile_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    address_line_1: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    address_line_2: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    city: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    state: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    pin: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    parent_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    parent_warehouse = relationship("Warehouse", foreign_keys=[parent_warehouse_id])

    lft: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    rgt: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    old_parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    old_parent = relationship("Warehouse", foreign_keys=[old_parent_id])

    warehouse_type_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouse_types.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    warehouse_type = relationship("WarehouseType", foreign_keys=[warehouse_type_id])

    default_in_transit_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    default_in_transit_warehouse = relationship("Warehouse", foreign_keys=[default_in_transit_warehouse_id])

    is_rejected_warehouse: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    customer: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<Warehouse id={self.id}>"
