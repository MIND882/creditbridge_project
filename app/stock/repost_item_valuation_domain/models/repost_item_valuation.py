"""

Repost Item Valuation -- converted from ``erpnext/stock/doctype/repost_item_valuation``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, Enum as SAEnum, ForeignKey, Integer, String, Text, Time, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["RepostItemValuation", "RepostItemValuationStatus", "RepostItemValuationBasedOn"]





class RepostItemValuationStatus(str, enum.Enum):

    QUEUED = "Queued"

    IN_PROGRESS = "In Progress"

    COMPLETED = "Completed"

    SKIPPED = "Skipped"

    FAILED = "Failed"

    CANCELLED = "Cancelled"



class RepostItemValuationBasedOn(str, enum.Enum):

    TRANSACTION = "Transaction"

    ITEM_AND_WAREHOUSE = "Item and Warehouse"





class RepostItemValuation(SubmittableModel, TenantModel):

    __tablename__ = "repost_item_valuations"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_repost_item_valuations_business_name"),

    )



    #: ``autoname`` = 'hash'.

    #: Upstream ``autoname = 'hash'``: Frappe assigns an opaque random hash.

    #: There is no content to hash here, so a UUID4 is the faithful

    #: equivalent -- unique, opaque, and not user-visible. Without a

    #: default the column is NOT NULL and every insert fails.

    name: Mapped[str] = mapped_column(

        String(140), nullable=False, default=lambda: uuid.uuid4().hex

    )



    item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item_code = relationship("Item", foreign_keys=[item_code_id])

    warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    warehouse = relationship("Warehouse", foreign_keys=[warehouse_id])

    posting_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    posting_time: Mapped[Optional[dt.time]] = mapped_column(Time, nullable=True)

    status: Mapped[Optional[str]] = mapped_column(SAEnum(RepostItemValuationStatus, native_enum=False, length=15, validate_strings=True), nullable=True)

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("repost_item_valuations.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("RepostItemValuation", foreign_keys=[amended_from_id])

    error_log: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    company: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    voucher_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    voucher_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    based_on: Mapped[str] = mapped_column(SAEnum(RepostItemValuationBasedOn, native_enum=False, length=22, validate_strings=True), nullable=False)

    allow_negative_stock: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    via_landed_cost_voucher: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    allow_zero_rate: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    items_to_be_repost: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    current_index: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    gl_reposting_index: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0)

    total_reposting_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    recreate_stock_ledgers: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    reposting_reference: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    repost_only_accounting_ledgers: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    total_vouchers: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    vouchers_posted: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    reposting_data_file: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    recalculate_valuation_rate: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<RepostItemValuation id={self.id}>"
