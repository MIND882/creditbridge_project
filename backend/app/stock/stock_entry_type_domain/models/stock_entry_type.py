"""

Stock Entry Type -- converted from ``erpnext/stock/doctype/stock_entry_type``.

"""



from __future__ import annotations



import enum

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["StockEntryType", "StockEntryTypePurpose"]





class StockEntryTypePurpose(str, enum.Enum):

    MATERIAL_ISSUE = "Material Issue"

    MATERIAL_RECEIPT = "Material Receipt"

    MATERIAL_TRANSFER = "Material Transfer"

    MATERIAL_TRANSFER_FOR_MANUFACTURE = "Material Transfer for Manufacture"

    MATERIAL_CONSUMPTION_FOR_MANUFACTURE = "Material Consumption for Manufacture"

    MANUFACTURE = "Manufacture"

    REPACK = "Repack"

    SEND_TO_SUBCONTRACTOR = "Send to Subcontractor"

    DISASSEMBLE = "Disassemble"

    RECEIVE_FROM_CUSTOMER = "Receive from Customer"

    RETURN_RAW_MATERIAL_TO_CUSTOMER = "Return Raw Material to Customer"

    SUBCONTRACTING_DELIVERY = "Subcontracting Delivery"

    SUBCONTRACTING_RETURN = "Subcontracting Return"





class StockEntryType(TenantModel):

    __tablename__ = "stock_entry_types"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_stock_entry_types_business_name"),

    )



    #: ``autoname`` = 'Prompt' -- the client supplies the name.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    purpose: Mapped[str] = mapped_column(SAEnum(StockEntryTypePurpose, native_enum=False, length=40, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=False)

    add_to_transit: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    is_standard: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<StockEntryType id={self.id}>"
