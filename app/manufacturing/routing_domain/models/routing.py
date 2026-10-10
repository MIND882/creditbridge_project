"""

Routing -- converted from ``erpnext/manufacturing/doctype/routing``.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import Boolean, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["Routing"]







class Routing(TenantModel):

    __tablename__ = "routings"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_routings_business_name"),

    )



    #: ``autoname`` = 'field:routing_name' -- derived in the service at create time.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    routing_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<Routing id={self.id}>"
