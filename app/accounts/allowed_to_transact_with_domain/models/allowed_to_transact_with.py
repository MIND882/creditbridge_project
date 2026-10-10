"""

Allowed To Transact With -- converted from ``erpnext/accounts/doctype/allowed_to_transact_with``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import String

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["AllowedToTransactWith"]







class AllowedToTransactWith(ChildTableModel, TenantModel):

    __tablename__ = "allowed_to_transact_withs"



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<AllowedToTransactWith id={self.id}>"
