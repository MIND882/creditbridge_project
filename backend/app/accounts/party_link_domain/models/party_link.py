"""

Party Link -- converted from ``erpnext/accounts/doctype/party_link``.





"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["PartyLink"]







class PartyLink(TenantModel):

    __tablename__ = "party_links"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_party_links_business_name"),

    )



    #: ``autoname`` = 'ACC-PT-LNK-.###.'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    primary_role: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    secondary_role: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    primary_party: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    secondary_party: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PartyLink id={self.id}>"
