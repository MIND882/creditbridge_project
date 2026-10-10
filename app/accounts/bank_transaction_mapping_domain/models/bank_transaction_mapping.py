"""

Bank Transaction Mapping -- converted from ``erpnext/accounts/doctype/bank_transaction_mapping``.



A Frappe child table (``istable: 1``): no independent identity, owned by a

Bank, ordered by ``idx``, never addressed by its own write API.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import ForeignKey, String

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["BankTransactionMapping"]





class BankTransactionMapping(ChildTableModel, TenantModel):

    """One row of a Bank."""



    __tablename__ = "bank_transaction_mappings"



    #: Re-declared from the mixin with a concrete FK so the constraint is real.

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("banks.id", ondelete="CASCADE"), nullable=True, index=True

    )

    parent = relationship("Bank", back_populates="bank_transaction_mapping")



    bank_transaction_field: Mapped[str] = mapped_column(String(140), nullable=False)

    file_field: Mapped[str] = mapped_column(String(140), nullable=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<BankTransactionMapping id={self.id}>"
