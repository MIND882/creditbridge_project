"""

Psoa Project -- converted from ``erpnext/accounts/doctype/psoa_project``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import ForeignKey, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["PsoaProject"]







class PsoaProject(ChildTableModel, TenantModel):

    __tablename__ = "psoa_projects"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("process_statement_of_accounts.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("ProcessStatementOfAccounts", back_populates="project", foreign_keys=[parent_id])



    project_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PsoaProject id={self.id}>"
