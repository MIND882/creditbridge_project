"""

Quality Inspection Template -- converted from ``erpnext/stock/doctype/quality_inspection_template``.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.stock.item_quality_inspection_parameter_domain.models.item_quality_inspection_parameter import ItemQualityInspectionParameter



from app.core.base_model import TenantModel



__all__ = ["QualityInspectionTemplate"]







class QualityInspectionTemplate(TenantModel):

    __tablename__ = "quality_inspection_templates"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_quality_inspection_templates_business_name"),

    )



    #: ``autoname`` = 'field:quality_inspection_template_name' -- derived in the service at create time.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    quality_inspection_template_name: Mapped[str] = mapped_column(String(140), nullable=False)



    item_quality_inspection_parameter: Mapped[list["ItemQualityInspectionParameter"]] = relationship(  # noqa: F821

        "ItemQualityInspectionParameter",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[ItemQualityInspectionParameter.parent_id]",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<QualityInspectionTemplate id={self.id}>"
