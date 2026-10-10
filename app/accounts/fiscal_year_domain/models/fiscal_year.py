"""

Fiscal Year -- converted from ``erpnext/accounts/doctype/fiscal_year``.



The accounting calendar. ``autoname`` is ``field:year``, so the name is a label

like ``2026`` or ``2026-2027``.



Upstream ``validate()`` runs:



    validate_dates()   -> start <= end, and unless ``is_short_year`` the end date

                          must be exactly one year after the start minus a day

    validate_overlap() -> two fiscal years may overlap in dates only if they

                          serve different companies



``is_short_year`` is upstream's escape hatch for jurisdictions that permit a

first or final accounting period shorter than twelve months (the US and Germany

are the cited examples), so ``validate_dates`` returns early for those.



``fiscal_year_company.company`` is a plain string, not the tenancy key: the

overlap rule is only meaningful when two fiscal years can name different

companies. See the note on ``ModeOfPayment``.



``auto_create_fiscal_year`` (the scheduler that rolls a year forward three days

before it ends) and the ``frappe.cache().delete_key("fiscal_years")`` calls in

``on_update``/``on_trash`` are not ported -- this conversion has no scheduler and

no shared cache to invalidate.

"""



from __future__ import annotations



import datetime as dt

from typing import Optional



from sqlalchemy import Boolean, Date, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.fiscal_year_company_domain.models.fiscal_year_company import (

    FiscalYearCompany,

)

from app.core.base_model import TenantModel, tenant_index



__all__ = ["FiscalYear"]





class FiscalYear(TenantModel):

    """``autoname = field:year``."""



    __tablename__ = "fiscal_years"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_fiscal_years_business_name"),

        tenant_index("ix_fiscal_years_business_year_start_date", "year_start_date"),

    )



    name: Mapped[str] = mapped_column(String(140), nullable=False)

    year: Mapped[str] = mapped_column(String(140), nullable=False)



    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    year_start_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    year_end_date: Mapped[dt.date] = mapped_column(Date, nullable=False)



    #: Set when the scheduler rolled this year forward from the previous one.

    auto_created: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    #: A short year is exempt from the "exactly one year" rule.

    is_short_year: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    companies = relationship(

        FiscalYearCompany,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=FiscalYearCompany.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:

        return f"<FiscalYear id={self.id} name={self.name!r} {self.year_start_date}..{self.year_end_date}>"
