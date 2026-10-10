"""

Psoa Cost Center -- converted from ``erpnext/accounts/doctype/psoa_cost_center``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import ForeignKey, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.cost_center_domain.models.cost_center import CostCenter  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["PsoaCostCenter"]







class PsoaCostCenter(ChildTableModel, TenantModel):

    __tablename__ = "psoa_cost_centers"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("process_statement_of_accounts.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("ProcessStatementOfAccounts", back_populates="cost_center", foreign_keys=[parent_id])



    cost_center_name_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    cost_center_name = relationship("CostCenter", foreign_keys=[cost_center_name_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PsoaCostCenter id={self.id}>"
