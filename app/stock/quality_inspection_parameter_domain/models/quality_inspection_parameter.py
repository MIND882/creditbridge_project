"""

Quality Inspection Parameter -- converted from ``erpnext/stock/doctype/quality_inspection_parameter``.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import ForeignKey, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel



__all__ = ["QualityInspectionParameter"]







class QualityInspectionParameter(TenantModel):

    __tablename__ = "quality_inspection_parameters"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_quality_inspection_parameters_business_name"),

    )



    #: ``autoname`` = 'field:parameter' -- derived in the service at create time.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    parameter: Mapped[str] = mapped_column(String(140), nullable=False)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    parameter_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("quality_inspection_parameter_groups.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    parameter_group = relationship("QualityInspectionParameterGroup", foreign_keys=[parameter_group_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<QualityInspectionParameter id={self.id}>"
