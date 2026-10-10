"""

Shareholder -- converted from ``erpnext/accounts/doctype/shareholder``.



The register of who holds equity, and how much. ``autoname`` is

``naming_series:`` with options ``ACC-SH-.YYYY.-``, so names look like

``ACC-SH-2026-00001``.



Upstream's controller carries only lifecycle plumbing -- ``onload`` and

``on_trash`` delegate to Frappe's address-and-contact helpers, which have no

counterpart here. The one piece of real logic is ``before_save``:



    for entry in self.share_balance:

        entry.amount = entry.no_of_shares * entry.rate



``amount`` is therefore never trusted from the client; it is recomputed on every

write. The client may send it, and the value is overwritten.



``company`` collapses into ``business_id`` (see the Account model note).

``contact_list`` is upstream a ``Code`` field holding serialised JSON produced by

the desk UI; it is kept as opaque text.

"""



from __future__ import annotations



from typing import Optional



from sqlalchemy import Boolean, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.share_balance_domain.models.share_balance import ShareBalance

from app.core.base_model import TenantModel, tenant_index



__all__ = ["Shareholder", "NAMING_SERIES"]



NAMING_SERIES = "ACC-SH-.YYYY.-"





class Shareholder(TenantModel):

    """``autoname = naming_series:`` (``ACC-SH-.YYYY.-#####``)."""



    __tablename__ = "shareholders"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_shareholders_business_name"),

        tenant_index("ix_shareholders_business_title", "title"),

    )



    name: Mapped[str] = mapped_column(String(140), nullable=False)

    naming_series: Mapped[str] = mapped_column(

        String(140), nullable=False, default=NAMING_SERIES

    )



    title: Mapped[str] = mapped_column(String(140), nullable=False)

    folio_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    #: A shareholder that is itself a company rather than a person.

    is_company: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    #: Upstream a ``Code`` field holding serialised JSON from the desk UI.

    contact_list: Mapped[Optional[str]] = mapped_column(Text, nullable=True)



    share_balance = relationship(

        ShareBalance,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=ShareBalance.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:

        return f"<Shareholder id={self.id} name={self.name!r} title={self.title!r}>"
