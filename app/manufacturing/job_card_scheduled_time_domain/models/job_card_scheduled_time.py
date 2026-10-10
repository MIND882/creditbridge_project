"""

Job Card Scheduled Time -- converted from ``erpnext/manufacturing/doctype/job_card_scheduled_time``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Job Card).

"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import DateTime, ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["JobCardScheduledTime"]







class JobCardScheduledTime(ChildTableModel, TenantModel):

    __tablename__ = "job_card_scheduled_times"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_job_card_scheduled_times_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("job_cards.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "app.manufacturing.job_card_domain.models.job_card.JobCard",

        back_populates="scheduled_time_logs",

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



    from_time: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)

    to_time: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)

    time_in_mins: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<JobCardScheduledTime id={self.id}>"
