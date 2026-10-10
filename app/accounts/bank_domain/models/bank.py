"""

Bank -- converted from ``erpnext/accounts/doctype/bank``.



JSON field                 Type here            Notes

-------------------------  -------------------  -------------------------

bank_name                  String(140) reqd     autoname: field:bank_name

swift_number               String(140)

website                    String(140)

plaid_access_token         String(140)          credential -- see note

bank_transaction_mapping   Table                -> BankTransactionMapping



``plaid_access_token`` is a third-party credential. It is stored as a plain

column here to match the ERPNext field, but it is excluded from the Read schema

so it cannot leak through the API. TODO(security): move to the encryption

helper in ``app.utils.encryption`` before any real Plaid integration.



``onload`` / ``on_trash`` upstream manage Frappe's generic Address/Contact

links. Neither is converted here, so those hooks are omitted rather than

faked.

"""



from __future__ import annotations



from typing import Optional



from sqlalchemy import String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel



__all__ = ["Bank"]





class Bank(TenantModel):

    """A bank or lending institution the tenant deals with."""



    __tablename__ = "banks"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_banks_business_id_name"),

    )



    #: ``autoname: field:bank_name`` upstream.

    name: Mapped[str] = mapped_column(String(140), nullable=False)

    bank_name: Mapped[str] = mapped_column(String(140), nullable=False)



    swift_number: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    website: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    #: Deliberately absent from BankRead.

    plaid_access_token: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    bank_transaction_mapping: Mapped[list["BankTransactionMapping"]] = relationship(  # noqa: F821

        "BankTransactionMapping",

        back_populates="parent",

        cascade="all, delete-orphan",

        passive_deletes=True,

        order_by="BankTransactionMapping.idx",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<Bank id={self.id} name={self.name!r}>"
