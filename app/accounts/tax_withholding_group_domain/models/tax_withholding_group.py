"""

Tax Withholding Group -- converted from ``erpnext/accounts/doctype/tax_withholding_group``.





"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["TaxWithholdingGroup"]







class TaxWithholdingGroup(TenantModel):

    __tablename__ = "tax_withholding_groups"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_tax_withholding_groups_business_name"),

    )



    #: ``autoname`` = 'field:group_name'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    group_name: Mapped[str] = mapped_column(String(140), nullable=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<TaxWithholdingGroup id={self.id}>"
