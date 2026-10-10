"""

Inventory Dimension -- converted from ``erpnext/stock/doctype/inventory_dimension``.

"""



from __future__ import annotations



import enum

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["InventoryDimension", "InventoryDimensionTypeOfTransaction"]





class InventoryDimensionTypeOfTransaction(str, enum.Enum):

    INWARD = "Inward"

    OUTWARD = "Outward"

    BOTH = "Both"





class InventoryDimension(TenantModel):

    __tablename__ = "inventory_dimensions"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_inventory_dimensions_business_name"),

    )



    #: ``autoname`` = 'field:dimension_name' -- derived in the service at create time.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    reference_document: Mapped[str] = mapped_column(String(140), nullable=False)

    dimension_name: Mapped[str] = mapped_column(String(140), nullable=False)

    document_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    istable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    condition: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    apply_to_all_doctypes: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    target_fieldname: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    source_fieldname: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    type_of_transaction: Mapped[Optional[str]] = mapped_column(SAEnum(InventoryDimensionTypeOfTransaction, native_enum=False, length=11, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    fetch_from_parent: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    mandatory_depends_on: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    reqd: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    validate_negative_stock: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<InventoryDimension id={self.id}>"
