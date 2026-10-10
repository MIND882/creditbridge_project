"""

Bank Account Type -- converted from ``erpnext/accounts/doctype/bank_account_type``.



A single-field lookup doctype. ``autoname`` is ``field:account_type``, so the label

*is* the identity upstream; here it is a unique column and ``id`` is the key.

"""



from __future__ import annotations



from sqlalchemy import String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["BankAccountType"]





class BankAccountType(TenantModel):

    """One row of the Bank Account Type lookup."""



    __tablename__ = "bank_account_types"

    __table_args__ = (

        UniqueConstraint("business_id", "account_type", name="uq_bank_account_types_business_id_account_type"),

    )



    #: ``autoname: field:account_type`` upstream -- the label is the document name.

    name: Mapped[str] = mapped_column(String(140), nullable=False)

    account_type: Mapped[str] = mapped_column(String(140), nullable=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<BankAccountType id={self.id} {self.account_type!r}>"
