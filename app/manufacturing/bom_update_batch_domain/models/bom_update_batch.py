"""

BOM Update Batch -- converted from ``erpnext/manufacturing/doctype/bom_update_batch``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Bom Update Log).

"""



from __future__ import annotations



import enum

from typing import Optional

import uuid



from sqlalchemy import Enum as SAEnum, ForeignKey, Integer, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["BomUpdateBatch", "BomUpdateBatchStatus"]





class BomUpdateBatchStatus(str, enum.Enum):

    PENDING = "Pending"

    COMPLETED = "Completed"





class BomUpdateBatch(ChildTableModel, TenantModel):

    __tablename__ = "bom_update_batchs"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_bom_update_batchs_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("bom_update_logs.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "app.manufacturing.bom_update_log_domain.models.bom_update_log.BomUpdateLog",

        back_populates="bom_batches",

        # explicit: a child can carry a second FK to its own parent

        # (item_variant_attribute.variant_of -> items), which would

        # otherwise make the join ambiguous

        foreign_keys=[parent_id],

    )

    parenttype: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    parentfield: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    #: ``autoname`` = 'hash'.

    #: Upstream ``autoname = 'hash'``: Frappe assigns an opaque random hash.

    #: There is no content to hash here, so a UUID4 is the faithful

    #: equivalent -- unique, opaque, and not user-visible. Without a

    #: default the column is NOT NULL and every insert fails.

    name: Mapped[str] = mapped_column(

        String(140), nullable=False, default=lambda: uuid.uuid4().hex

    )



    level: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    batch_no: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    boms_updated: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    status: Mapped[Optional[str]] = mapped_column(SAEnum(BomUpdateBatchStatus, native_enum=False, length=13, validate_strings=True), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<BomUpdateBatch id={self.id}>"
