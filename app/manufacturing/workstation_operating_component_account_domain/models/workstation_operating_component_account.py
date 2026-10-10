"""

Workstation Operating Component Account -- converted from ``erpnext/manufacturing/doctype/workstation_operating_component_account``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Workstation Operating Component).

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["WorkstationOperatingComponentAccount"]







class WorkstationOperatingComponentAccount(ChildTableModel, TenantModel):

    __tablename__ = "workstation_operating_component_accounts"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_workstation_operating_component_accounts_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("workstation_operating_components.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "app.manufacturing.workstation_operating_component_domain.models.workstation_operating_component.WorkstationOperatingComponent",

        back_populates="accounts",

        # explicit: a child can carry a second FK to its own parent

        # (item_variant_attribute.variant_of -> items), which would

        # otherwise make the join ambiguous

        foreign_keys=[parent_id],

    )

    parenttype: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    parentfield: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    #: ``autoname`` = 'hash'.

    #: Upstream ``autoname = 'hash'``: Frappe assigns an opaque random hash.

    #: There is no content to hash here, so a UUID4 is the faithful

    #: equivalent -- unique, opaque, and not user-visible. Without a

    #: default the column is NOT NULL and every insert fails.

    name: Mapped[str] = mapped_column(

        String(140), nullable=False, default=lambda: uuid.uuid4().hex

    )



    company: Mapped[str] = mapped_column(String(140), nullable=False)

    expense_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    expense_account = relationship("app.accounts.account_domain.models.account.Account", foreign_keys=[expense_account_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<WorkstationOperatingComponentAccount id={self.id}>"
