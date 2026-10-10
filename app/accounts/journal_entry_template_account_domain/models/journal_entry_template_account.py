"""

Journal Entry Template Account -- converted from

``erpnext/accounts/doctype/journal_entry_template_account``.



A Frappe child table (``istable: 1``): one row of a template, naming an account

and optionally the party and cost centre to prefill. Upstream the controller is

empty; ``JournalEntryTemplate.validate_party`` and ``validate_account_company``

govern these rows.



``party_type`` and ``party`` are upstream a Link to DocType plus a Dynamic Link.

Neither Customer nor Supplier is converted, so both stay strings -- the service

checks the *combination* (the part upstream actually validates) rather than

resolving a party row that does not exist yet.



``project`` stays a string for the same reason: the Projects module is out of

scope.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import ForeignKey, String

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["JournalEntryTemplateAccount"]





class JournalEntryTemplateAccount(ChildTableModel, TenantModel):

    """One row of ``JournalEntryTemplate.accounts``."""



    __tablename__ = "journal_entry_template_accounts"



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("journal_entry_templates.id", ondelete="CASCADE"),

        nullable=True,

        index=True,

    )

    parent = relationship(

        "JournalEntryTemplate", back_populates="accounts", foreign_keys=[parent_id]

    )



    account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"), nullable=False, index=True

    )

    account = relationship("Account", foreign_keys=[account_id])



    #: Upstream a Link to DocType, naming Customer or Supplier.

    party_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    #: Upstream a Dynamic Link resolved through ``party_type``.

    party: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"), nullable=True, index=True

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])



    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<JournalEntryTemplateAccount id={self.id} idx={self.idx}>"
