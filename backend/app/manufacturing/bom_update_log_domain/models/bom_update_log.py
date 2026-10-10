"""

BOM Update Log -- converted from ``erpnext/manufacturing/doctype/bom_update_log``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import enum

from typing import Optional

import uuid



from sqlalchemy import Enum as SAEnum, ForeignKey, Integer, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.manufacturing.bom_update_batch_domain.models.bom_update_batch import BomUpdateBatch



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["BomUpdateLog", "BomUpdateLogUpdateType", "BomUpdateLogStatus"]





class BomUpdateLogUpdateType(str, enum.Enum):

    REPLACE_BOM = "Replace BOM"

    UPDATE_COST = "Update Cost"



class BomUpdateLogStatus(str, enum.Enum):

    QUEUED = "Queued"

    IN_PROGRESS = "In Progress"

    COMPLETED = "Completed"

    FAILED = "Failed"

    CANCELLED = "Cancelled"





class BomUpdateLog(SubmittableModel, TenantModel):

    __tablename__ = "bom_update_logs"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_bom_update_logs_business_name"),

    )



    #: ``autoname`` = 'pattern:BOM-UPDT-LOG-'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    update_type: Mapped[Optional[str]] = mapped_column(SAEnum(BomUpdateLogUpdateType, native_enum=False, length=15, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    status: Mapped[Optional[str]] = mapped_column(SAEnum(BomUpdateLogStatus, native_enum=False, length=15, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    current_bom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("boms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    current_bom = relationship("app.manufacturing.bom_domain.models.bom.Bom", foreign_keys=[current_bom_id])

    new_bom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("boms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    new_bom = relationship("app.manufacturing.bom_domain.models.bom.Bom", foreign_keys=[new_bom_id])

    error_log: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    current_level: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    processed_boms: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("bom_update_logs.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("app.manufacturing.bom_update_log_domain.models.bom_update_log.BomUpdateLog", foreign_keys=[amended_from_id])



    bom_batches: Mapped[list["BomUpdateBatch"]] = relationship(  # noqa: F821

        "app.manufacturing.bom_update_batch_domain.models.bom_update_batch.BomUpdateBatch",

        back_populates="parent",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        cascade="all, delete-orphan",

        foreign_keys=[BomUpdateBatch.parent_id],

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<BomUpdateLog id={self.id}>"
