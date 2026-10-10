"""

Bank Account Subtype -- converted from ``erpnext/accounts/doctype/bank_account_subtype``.



A single-field lookup doctype. ``autoname`` is ``field:account_subtype``, so the label

*is* the identity upstream; here it is a unique column and ``id`` is the key.

"""



from __future__ import annotations



from sqlalchemy import String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["BankAccountSubtype"]





class BankAccountSubtype(TenantModel):

    """One row of the Bank Account Subtype lookup."""



    __tablename__ = "bank_account_subtypes"

    __table_args__ = (

        UniqueConstraint("business_id", "account_subtype", name="uq_bank_account_subtypes_business_id_account_subtype"),

    )



    #: ``autoname: field:account_subtype`` upstream -- the label is the document name.

    name: Mapped[str] = mapped_column(String(140), nullable=False)

    account_subtype: Mapped[str] = mapped_column(String(140), nullable=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<BankAccountSubtype id={self.id} {self.account_subtype!r}>"
