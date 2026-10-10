"""

Process Statement Of Accounts Cc -- converted from ``erpnext/accounts/doctype/process_statement_of_accounts_cc``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import ForeignKey, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["ProcessStatementOfAccountsCc"]







class ProcessStatementOfAccountsCc(ChildTableModel, TenantModel):

    __tablename__ = "process_statement_of_accounts_ccs"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("process_statement_of_accounts.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("ProcessStatementOfAccounts", back_populates="cc_to", foreign_keys=[parent_id])



    cc: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ProcessStatementOfAccountsCc id={self.id}>"
