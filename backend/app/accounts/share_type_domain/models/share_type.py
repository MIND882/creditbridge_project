"""

Share Type -- converted from ``erpnext/accounts/doctype/share_type``.



A class of share (Ordinary, Preference, ...) with a face value implied by its

description. ``autoname`` is ``field:title``.



Upstream's controller is empty -- there is no validation to port.

"""



from __future__ import annotations



from typing import Optional



from sqlalchemy import String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel, tenant_index



__all__ = ["ShareType"]





class ShareType(TenantModel):

    """``autoname = field:title``."""



    __tablename__ = "share_types"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_share_types_business_name"),

        tenant_index("ix_share_types_name", "name"),

    )



    name: Mapped[str] = mapped_column(String(140), nullable=False)

    title: Mapped[str] = mapped_column(String(140), nullable=False)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)



    def __repr__(self) -> str:

        return f"<ShareType id={self.id} name={self.name!r}>"
