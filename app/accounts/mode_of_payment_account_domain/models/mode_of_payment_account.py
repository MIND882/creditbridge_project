"""

Mode of Payment Account -- converted from

``erpnext/accounts/doctype/mode_of_payment_account``.



A Frappe child table (``istable: 1``): one row per company naming the account

that mode of payment books to there. Upstream the controller is empty; the

checks that govern these rows live on ``ModeOfPayment``.



``company`` is a plain string, not the tenancy key -- see the note on

``ModeOfPayment``. The rows are only meaningful if two of them can name

different companies.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import ForeignKey, String

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["ModeOfPaymentAccount"]





class ModeOfPaymentAccount(ChildTableModel, TenantModel):

    """One row of ``ModeOfPayment.accounts``."""



    __tablename__ = "mode_of_payment_accounts"



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("mode_of_payments.id", ondelete="CASCADE"), nullable=True, index=True

    )

    parent = relationship(

        "ModeOfPayment", back_populates="accounts", foreign_keys=[parent_id]

    )



    #: Which company this row applies to. Not the tenant -- see the model note.

    company: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    default_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"), nullable=True, index=True

    )

    default_account = relationship("Account", foreign_keys=[default_account_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ModeOfPaymentAccount id={self.id} idx={self.idx} company={self.company!r}>"
