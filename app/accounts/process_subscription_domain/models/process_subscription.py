"""

Process Subscription -- converted from ``erpnext/accounts/doctype/process_subscription``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

from typing import Optional

import uuid



from sqlalchemy import Date, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["ProcessSubscription"]







class ProcessSubscription(SubmittableModel, TenantModel):

    __tablename__ = "process_subscriptions"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_process_subscriptions_business_name"),

    )



    #: Upstream declares no ``autoname``; Frappe mints a hash.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    amended_from: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    posting_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    subscription: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ProcessSubscription id={self.id}>"
