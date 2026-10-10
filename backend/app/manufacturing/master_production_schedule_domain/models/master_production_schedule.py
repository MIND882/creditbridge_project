"""

Master Production Schedule -- converted from ``erpnext/manufacturing/doctype/master_production_schedule``.

"""



from __future__ import annotations



import datetime as dt

import enum

from typing import Optional

import uuid



from sqlalchemy import Date, Enum as SAEnum, ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.manufacturing.production_plan_sales_order_domain.models.production_plan_sales_order import ProductionPlanSalesOrder

from app.manufacturing.production_plan_material_request_domain.models.production_plan_material_request import ProductionPlanMaterialRequest

from app.manufacturing.master_production_schedule_item_domain.models.master_production_schedule_item import MasterProductionScheduleItem



from app.core.base_model import TenantModel



__all__ = ["MasterProductionSchedule", "MasterProductionScheduleNamingSeries"]





class MasterProductionScheduleNamingSeries(str, enum.Enum):

    MPS_YY = "MPS.YY.-.######"





class MasterProductionSchedule(TenantModel):

    __tablename__ = "master_production_schedules"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_master_production_schedules_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    naming_series: Mapped[str] = mapped_column(SAEnum(MasterProductionScheduleNamingSeries, native_enum=False, length=19, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=False)

    company: Mapped[str] = mapped_column(String(140), nullable=False)

    posting_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    from_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    to_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    parent_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    parent_warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[parent_warehouse_id])

    sales_forecast_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("sales_forecasts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    sales_forecast = relationship("app.manufacturing.sales_forecast_domain.models.sales_forecast.SalesForecast", foreign_keys=[sales_forecast_id])

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("master_production_schedules.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("app.manufacturing.master_production_schedule_domain.models.master_production_schedule.MasterProductionSchedule", foreign_keys=[amended_from_id])



    sales_orders: Mapped[list["ProductionPlanSalesOrder"]] = relationship(  # noqa: F821

        "app.manufacturing.production_plan_sales_order_domain.models.production_plan_sales_order.ProductionPlanSalesOrder",

        back_populates="parent",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        cascade="all, delete-orphan",

        foreign_keys=[ProductionPlanSalesOrder.parent_id],

    )



    material_requests: Mapped[list["ProductionPlanMaterialRequest"]] = relationship(  # noqa: F821

        "app.manufacturing.production_plan_material_request_domain.models.production_plan_material_request.ProductionPlanMaterialRequest",

        back_populates="parent",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        cascade="all, delete-orphan",

        foreign_keys=[ProductionPlanMaterialRequest.parent_id],

    )



    items: Mapped[list["MasterProductionScheduleItem"]] = relationship(  # noqa: F821

        "app.manufacturing.master_production_schedule_item_domain.models.master_production_schedule_item.MasterProductionScheduleItem",

        back_populates="parent",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        cascade="all, delete-orphan",

        foreign_keys=[MasterProductionScheduleItem.parent_id],

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<MasterProductionSchedule id={self.id}>"
