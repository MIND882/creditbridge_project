"""

Workstation Operating Component -- converted from ``erpnext/manufacturing/doctype/workstation_operating_component``.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.manufacturing.workstation_operating_component_account_domain.models.workstation_operating_component_account import WorkstationOperatingComponentAccount



from app.core.base_model import TenantModel



__all__ = ["WorkstationOperatingComponent"]







class WorkstationOperatingComponent(TenantModel):

    __tablename__ = "workstation_operating_components"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_workstation_operating_components_business_name"),

    )



    #: ``autoname`` = 'field:component_name' -- derived in the service at create time.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    component_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    accounts: Mapped[list["WorkstationOperatingComponentAccount"]] = relationship(  # noqa: F821

        "app.manufacturing.workstation_operating_component_account_domain.models.workstation_operating_component_account.WorkstationOperatingComponentAccount",

        back_populates="parent",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        cascade="all, delete-orphan",

        foreign_keys=[WorkstationOperatingComponentAccount.parent_id],

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<WorkstationOperatingComponent id={self.id}>"
