"""

Transaction Deletion Record Details -- converted from ``erpnext/accounts/doctype/transaction_deletion_record_details``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import Boolean, Integer, String

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["TransactionDeletionRecordDetails"]







class TransactionDeletionRecordDetails(ChildTableModel, TenantModel):

    __tablename__ = "transaction_deletion_record_details"

    doctype_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    docfield_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    no_of_docs: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    done: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<TransactionDeletionRecordDetails id={self.id}>"
