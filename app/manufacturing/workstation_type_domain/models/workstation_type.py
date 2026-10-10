"""

Workstation Type -- converted from ``erpnext/manufacturing/doctype/workstation_type``.

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["WorkstationType"]







class WorkstationType(TenantModel):

    __tablename__ = "workstation_types"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_workstation_types_business_name"),

    )



    #: ``autoname`` = 'field:workstation_type' -- derived in the service at create time.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    workstation_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    hour_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    description: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<WorkstationType id={self.id}>"
