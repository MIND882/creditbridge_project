"""

TaxWithholdingAccount -- converted from

``erpnext/accounts/doctype/tax_withholding_account``.



One row of ``TaxWithholdingCategory.accounts``: the ledger account the withheld

tax is booked to.



Upstream keys this row on ``company``. Tenancy here is ``business_id``, which is

already on the row via ``TenantModel``, so the company column is collapsed

rather than duplicated -- one row per account is the meaningful shape.



Rows only ever exist inside a category, so the API is read-only.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["TaxWithholdingAccount"]





class TaxWithholdingAccount(ChildTableModel, TenantModel):

    """One row of ``TaxWithholdingCategory.accounts``."""



    __tablename__ = "tax_withholding_accounts"



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("tax_withholding_categories.id", ondelete="CASCADE"), nullable=True, index=True

    )



    account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"), nullable=False, index=True

    )

    account = relationship("Account", foreign_keys=[account_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<TaxWithholdingAccount id={self.id} account={self.account_id}>"
