"""

Serial No -- converted from ``erpnext/stock/doctype/serial_no``.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Date, Enum as SAEnum, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel



__all__ = ["SerialNo", "SerialNoAssetStatus", "SerialNoMaintenanceStatus", "SerialNoStatus"]





class SerialNoAssetStatus(str, enum.Enum):

    ISSUE = "Issue"

    RECEIPT = "Receipt"

    TRANSFER = "Transfer"



class SerialNoMaintenanceStatus(str, enum.Enum):

    UNDER_WARRANTY = "Under Warranty"

    OUT_OF_WARRANTY = "Out of Warranty"

    UNDER_AMC = "Under AMC"

    OUT_OF_AMC = "Out of AMC"



class SerialNoStatus(str, enum.Enum):

    ACTIVE = "Active"

    INACTIVE = "Inactive"

    CONSUMED = "Consumed"

    DELIVERED = "Delivered"

    EXPIRED = "Expired"





class SerialNo(TenantModel):

    __tablename__ = "serial_nos"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_serial_nos_business_name"),

    )



    #: ``autoname`` = 'field:serial_no' -- derived in the service at create time.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    serial_no: Mapped[str] = mapped_column(String(140), nullable=False)

    item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    item_code = relationship("Item", foreign_keys=[item_code_id])

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    item_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("item_groups.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item_group = relationship("ItemGroup", foreign_keys=[item_group_id])

    brand_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("brands.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    brand = relationship("Brand", foreign_keys=[brand_id])

    asset: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    asset_status: Mapped[Optional[str]] = mapped_column(SAEnum(SerialNoAssetStatus, native_enum=False, length=12, validate_strings=True), nullable=True)

    location: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    employee: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    maintenance_status: Mapped[Optional[str]] = mapped_column(SAEnum(SerialNoMaintenanceStatus, native_enum=False, length=19, validate_strings=True), nullable=True)

    warranty_period: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    warranty_expiry_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    amc_expiry_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    company: Mapped[str] = mapped_column(String(140), nullable=False)

    work_order: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    warehouse = relationship("Warehouse", foreign_keys=[warehouse_id])

    batch_no_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("batchs.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    batch_no = relationship("Batch", foreign_keys=[batch_no_id])

    purchase_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    status: Mapped[Optional[str]] = mapped_column(SAEnum(SerialNoStatus, native_enum=False, length=13, validate_strings=True), nullable=True)

    customer: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    reference_doctype: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    reference_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    posting_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SerialNo id={self.id}>"
