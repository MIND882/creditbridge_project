"""

Workstation Working Hour -- converted from ``erpnext/manufacturing/doctype/workstation_working_hour``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Workstation).

"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, ForeignKey, Numeric, String, Time, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["WorkstationWorkingHour"]







class WorkstationWorkingHour(ChildTableModel, TenantModel):

    __tablename__ = "workstation_working_hours"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_workstation_working_hours_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("workstations.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "app.manufacturing.workstation_domain.models.workstation.Workstation",

        back_populates="working_hours",

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



    start_time: Mapped[dt.time] = mapped_column(Time, nullable=False)

    hours: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    end_time: Mapped[dt.time] = mapped_column(Time, nullable=False)

    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<WorkstationWorkingHour id={self.id}>"
