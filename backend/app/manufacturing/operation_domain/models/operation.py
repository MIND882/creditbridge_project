"""

Operation -- converted from ``erpnext/manufacturing/doctype/operation``.

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.manufacturing.sub_operation_domain.models.sub_operation import SubOperation



from app.core.base_model import TenantModel



__all__ = ["Operation"]







class Operation(TenantModel):

    __tablename__ = "operations"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_operations_business_name"),

    )



    #: ``autoname`` = 'prompt'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    workstation_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("workstations.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    workstation = relationship("app.manufacturing.workstation_domain.models.workstation.Workstation", foreign_keys=[workstation_id])

    is_corrective_operation: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    create_job_card_based_on_batch_size: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    quality_inspection_template_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("quality_inspection_templates.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    quality_inspection_template = relationship("app.stock.quality_inspection_template_domain.models.quality_inspection_template.QualityInspectionTemplate", foreign_keys=[quality_inspection_template_id])

    batch_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=1)

    total_operation_time: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    work_instruction: Mapped[Optional[str]] = mapped_column(Text, nullable=True)



    sub_operations: Mapped[list["SubOperation"]] = relationship(  # noqa: F821

        "app.manufacturing.sub_operation_domain.models.sub_operation.SubOperation",

        back_populates="parent",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        cascade="all, delete-orphan",

        foreign_keys=[SubOperation.parent_id],

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<Operation id={self.id}>"
