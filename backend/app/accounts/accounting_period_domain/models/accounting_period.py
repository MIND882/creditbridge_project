"""

Accounting Period -- converted from

``erpnext/accounts/doctype/accounting_period``.



JSON field        Type here            Notes

----------------  -------------------  ----------------------------------

period_name       String(140) reqd

start_date        Date        reqd

end_date          Date        reqd

company           *collapsed*          -> business_id

disabled          Boolean

closed_documents  Table                -> ClosedDocument child rows

exempted_role     String(140)          Link Role, kept as a label



``autoname`` is ``field:period_name`` combined with the company abbr upstream;

here the name is ``period_name`` plus the optional tenant abbr.

"""



from __future__ import annotations



import uuid

from datetime import date

from typing import Optional



from sqlalchemy import Boolean, Date, ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel, tenant_index



__all__ = ["AccountingPeriod"]





class AccountingPeriod(TenantModel):

    """

    A closed stretch of the calendar during which postings are refused.



    The interesting rule is ``validate_overlap``: two periods for the same

    tenant may not overlap in time.

    """



    __tablename__ = "accounting_periods"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_accounting_periods_business_id_name"),

        tenant_index("ix_accounting_periods_business_dates", "start_date", "end_date"),

    )



    name: Mapped[str] = mapped_column(String(255), nullable=False)

    period_name: Mapped[str] = mapped_column(String(140), nullable=False)



    start_date: Mapped[date] = mapped_column(Date, nullable=False)

    end_date: Mapped[date] = mapped_column(Date, nullable=False)



    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    #: ERPNext's ``exempted_role`` Link. Role is not converted, so the label is

    #: stored; the service compares it against the actor's roles.

    exempted_role: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    closed_documents: Mapped[list["ClosedDocument"]] = relationship(

        "ClosedDocument",

        back_populates="parent",

        cascade="all, delete-orphan",

        passive_deletes=True,

        order_by="ClosedDocument.idx",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<AccountingPeriod id={self.id} name={self.name!r}>"





class ClosedDocument(TenantModel):

    """

    Child table row (``erpnext/accounts/doctype/closed_document``).



    Records which document types are locked inside this period. ``istable: 1``

    upstream, so it has no API of its own.

    """



    __tablename__ = "closed_documents"



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounting_periods.id", ondelete="CASCADE"), nullable=True, index=True

    )

    parent: Mapped[Optional[AccountingPeriod]] = relationship(

        "AccountingPeriod", back_populates="closed_documents"

    )

    idx: Mapped[int] = mapped_column(nullable=False, default=0)



    #: Upstream a Link to DocType; no DocType registry exists here, so the

    #: doctype name is stored as a label.

    document_type: Mapped[str] = mapped_column(String(140), nullable=False)

    closed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ClosedDocument id={self.id} type={self.document_type!r}>"
