"""

Company Restriction -- converted from ``erpnext/stock/doctype/company_restriction``.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["CompanyRestriction"]







class CompanyRestriction(TenantModel):

    __tablename__ = "company_restrictions"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_company_restrictions_business_name"),

    )



    #: ``autoname`` = 'hash'.

    #: Upstream ``autoname = 'hash'``: Frappe assigns an opaque random hash.

    #: There is no content to hash here, so a UUID4 is the faithful

    #: equivalent -- unique, opaque, and not user-visible. Without a

    #: default the column is NOT NULL and every insert fails.

    name: Mapped[str] = mapped_column(

        String(140), nullable=False, default=lambda: uuid.uuid4().hex

    )



    company: Mapped[str] = mapped_column(String(140), nullable=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<CompanyRestriction id={self.id}>"
