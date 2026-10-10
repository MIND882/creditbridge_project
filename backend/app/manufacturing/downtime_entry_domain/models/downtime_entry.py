"""

Downtime Entry -- converted from ``erpnext/manufacturing/doctype/downtime_entry``.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel



__all__ = ["DowntimeEntry", "DowntimeEntryNamingSeries", "DowntimeEntryStopReason"]





class DowntimeEntryNamingSeries(str, enum.Enum):

    DT = "DT-"



class DowntimeEntryStopReason(str, enum.Enum):

    EXCESSIVE_MACHINE_SET_UP_TIME = "Excessive machine set up time"

    UNPLANNED_MACHINE_MAINTENANCE = "Unplanned machine maintenance"

    ON_MACHINE_PRESS_CHECKS = "On-machine press checks"

    MACHINE_OPERATOR_ERRORS = "Machine operator errors"

    MACHINE_MALFUNCTION = "Machine malfunction"

    ELECTRICITY_DOWN = "Electricity down"

    OTHER = "Other"





class DowntimeEntry(TenantModel):

    __tablename__ = "downtime_entries"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_downtime_entrys_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    naming_series: Mapped[str] = mapped_column(SAEnum(DowntimeEntryNamingSeries, native_enum=False, length=7, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=False)

    workstation_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("workstations.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    workstation = relationship("app.manufacturing.workstation_domain.models.workstation.Workstation", foreign_keys=[workstation_id])

    operator: Mapped[str] = mapped_column(String(140), nullable=False)

    from_time: Mapped[dt.datetime] = mapped_column(DateTime, nullable=False)

    to_time: Mapped[dt.datetime] = mapped_column(DateTime, nullable=False)

    downtime: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    stop_reason: Mapped[str] = mapped_column(SAEnum(DowntimeEntryStopReason, native_enum=False, length=33, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=False)

    remarks: Mapped[Optional[str]] = mapped_column(Text, nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<DowntimeEntry id={self.id}>"
