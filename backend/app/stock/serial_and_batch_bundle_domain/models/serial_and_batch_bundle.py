"""

Serial and Batch Bundle -- converted from ``erpnext/stock/doctype/serial_and_batch_bundle``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, DateTime, Enum as SAEnum, ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.stock.serial_and_batch_entry_domain.models.serial_and_batch_entry import SerialAndBatchEntry



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["SerialAndBatchBundle", "SerialAndBatchBundleTypeOfTransaction", "SerialAndBatchBundleNamingSeries"]





class SerialAndBatchBundleTypeOfTransaction(str, enum.Enum):

    INWARD = "Inward"

    OUTWARD = "Outward"

    MAINTENANCE = "Maintenance"

    ASSET_REPAIR = "Asset Repair"



class SerialAndBatchBundleNamingSeries(str, enum.Enum):

    SABB = "SABB-.########"





class SerialAndBatchBundle(SubmittableModel, TenantModel):

    __tablename__ = "serial_and_batch_bundles"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_serial_and_batch_bundles_business_name"),

    )



    #: ``autoname`` = 'hash'.

    #: Upstream ``autoname = 'hash'``: Frappe assigns an opaque random hash.

    #: There is no content to hash here, so a UUID4 is the faithful

    #: equivalent -- unique, opaque, and not user-visible. Without a

    #: default the column is NOT NULL and every insert fails.

    name: Mapped[str] = mapped_column(

        String(140), nullable=False, default=lambda: uuid.uuid4().hex

    )



    company: Mapped[str] = mapped_column(String(140), nullable=False)

    item_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("item_groups.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item_group = relationship("ItemGroup", foreign_keys=[item_group_id])

    has_serial_no: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    item_code = relationship("Item", foreign_keys=[item_code_id])

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    has_batch_no: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    voucher_type: Mapped[str] = mapped_column(String(140), nullable=False)

    voucher_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_cancelled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("serial_and_batch_bundles.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("SerialAndBatchBundle", foreign_keys=[amended_from_id])

    avg_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    warehouse = relationship("Warehouse", foreign_keys=[warehouse_id])

    type_of_transaction: Mapped[str] = mapped_column(SAEnum(SerialAndBatchBundleTypeOfTransaction, native_enum=False, length=16, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=False)

    is_rejected: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    voucher_detail_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    returned_against: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    naming_series: Mapped[Optional[str]] = mapped_column(SAEnum(SerialAndBatchBundleNamingSeries, native_enum=False, length=18, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    is_packed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    posting_datetime: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)



    entries: Mapped[list["SerialAndBatchEntry"]] = relationship(  # noqa: F821

        "SerialAndBatchEntry",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[SerialAndBatchEntry.parent_id]",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SerialAndBatchBundle id={self.id}>"
