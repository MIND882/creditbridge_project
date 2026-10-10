"""

Quality Inspection Parameter Group -- converted from ``erpnext/stock/doctype/quality_inspection_parameter_group``.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["QualityInspectionParameterGroup"]







class QualityInspectionParameterGroup(TenantModel):

    __tablename__ = "quality_inspection_parameter_groups"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_quality_inspection_parameter_groups_business_name"),

    )



    #: ``autoname`` = 'field:group_name' -- derived in the service at create time.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    group_name: Mapped[str] = mapped_column(String(140), nullable=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<QualityInspectionParameterGroup id={self.id}>"
