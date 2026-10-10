"""

BOM Update Tool -- converted from ``erpnext/manufacturing/doctype/bom_update_tool``.



A Frappe Single (``issingle: 1``): one row per ``business_id``, enforced by a unique constraint on ``business_id`` alone.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import ForeignKey, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel



__all__ = ["BomUpdateTool"]







class BomUpdateTool(TenantModel):

    __tablename__ = "bom_update_tools"

    __table_args__ = (

        UniqueConstraint("business_id", name="uq_bom_update_tools_business"),

    )



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



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<BomUpdateTool id={self.id}>"
