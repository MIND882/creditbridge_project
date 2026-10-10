"""

Fiscal Year Company -- converted from

``erpnext/accounts/doctype/fiscal_year_company``.



A Frappe child table (``istable: 1``): names one company a fiscal year applies

to. Upstream the controller is empty.



``company`` is a plain string rather than the tenancy key -- ``FiscalYear``'s

overlap rule depends on two fiscal years being able to name different companies.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import ForeignKey, String

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["FiscalYearCompany"]





class FiscalYearCompany(ChildTableModel, TenantModel):

    """One row of ``FiscalYear.companies``."""



    __tablename__ = "fiscal_year_companies"



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("fiscal_years.id", ondelete="CASCADE"), nullable=True, index=True

    )

    parent = relationship(

        "FiscalYear", back_populates="companies", foreign_keys=[parent_id]

    )



    company: Mapped[str] = mapped_column(String(140), nullable=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<FiscalYearCompany id={self.id} idx={self.idx} company={self.company!r}>"
