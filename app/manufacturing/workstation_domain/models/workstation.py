"""

Workstation -- converted from ``erpnext/manufacturing/doctype/workstation``.

"""



from __future__ import annotations



import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.manufacturing.workstation_cost_domain.models.workstation_cost import WorkstationCost

from app.manufacturing.workstation_working_hour_domain.models.workstation_working_hour import WorkstationWorkingHour



from app.core.base_model import TenantModel



__all__ = ["Workstation", "WorkstationStatus"]





class WorkstationStatus(str, enum.Enum):

    PRODUCTION = "Production"

    OFF = "Off"

    IDLE = "Idle"

    PROBLEM = "Problem"

    MAINTENANCE = "Maintenance"

    SETUP = "Setup"





class Workstation(TenantModel):

    __tablename__ = "workstations"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_workstations_business_name"),

    )



    #: ``autoname`` = 'field:workstation_name' -- derived in the service at create time.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    workstation_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    workstation_type_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("workstation_types.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    workstation_type = relationship("app.manufacturing.workstation_type_domain.models.workstation_type.WorkstationType", foreign_keys=[workstation_type_id])

    plant_floor_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("plant_floors.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    plant_floor = relationship("app.manufacturing.plant_floor_domain.models.plant_floor.PlantFloor", foreign_keys=[plant_floor_id])

    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    production_capacity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[warehouse_id])

    status: Mapped[Optional[str]] = mapped_column(SAEnum(WorkstationStatus, native_enum=False, length=15, validate_strings=True), nullable=True)

    on_status_image: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    off_status_image: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    hour_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    holiday_list: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    total_working_hours: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    workstation_costs: Mapped[list["WorkstationCost"]] = relationship(  # noqa: F821

        "app.manufacturing.workstation_cost_domain.models.workstation_cost.WorkstationCost",

        back_populates="parent",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        cascade="all, delete-orphan",

        foreign_keys=[WorkstationCost.parent_id],

    )



    working_hours: Mapped[list["WorkstationWorkingHour"]] = relationship(  # noqa: F821

        "app.manufacturing.workstation_working_hour_domain.models.workstation_working_hour.WorkstationWorkingHour",

        back_populates="parent",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        cascade="all, delete-orphan",

        foreign_keys=[WorkstationWorkingHour.parent_id],

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<Workstation id={self.id}>"
