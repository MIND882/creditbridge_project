"""

Sales Forecast -- converted from ``erpnext/manufacturing/doctype/sales_forecast``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from typing import Optional

import uuid



from sqlalchemy import Date, Enum as SAEnum, ForeignKey, Integer, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.manufacturing.sales_forecast_item_domain.models.sales_forecast_item import SalesForecastItem

from app.manufacturing.sales_forecast_item_domain.models.sales_forecast_item import SalesForecastItem



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["SalesForecast", "SalesForecastNamingSeries", "SalesForecastFrequency", "SalesForecastStatus"]





class SalesForecastNamingSeries(str, enum.Enum):

    SF_YY = "SF.YY.-.######"



class SalesForecastFrequency(str, enum.Enum):

    WEEKLY = "Weekly"

    MONTHLY = "Monthly"



class SalesForecastStatus(str, enum.Enum):

    PLANNED = "Planned"

    MPS_GENERATED = "MPS Generated"

    CANCELLED = "Cancelled"





class SalesForecast(SubmittableModel, TenantModel):

    __tablename__ = "sales_forecasts"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_sales_forecasts_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    naming_series: Mapped[str] = mapped_column(SAEnum(SalesForecastNamingSeries, native_enum=False, length=18, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=False)

    company: Mapped[str] = mapped_column(String(140), nullable=False)

    posting_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    from_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    frequency: Mapped[str] = mapped_column(SAEnum(SalesForecastFrequency, native_enum=False, length=11, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=False)

    demand_number: Mapped[int] = mapped_column(Integer, nullable=False, default=6)

    parent_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    parent_warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[parent_warehouse_id])

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("sales_forecasts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("app.manufacturing.sales_forecast_domain.models.sales_forecast.SalesForecast", foreign_keys=[amended_from_id])

    status: Mapped[Optional[str]] = mapped_column(SAEnum(SalesForecastStatus, native_enum=False, length=17, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)



    selected_items: Mapped[list["SalesForecastItem"]] = relationship(  # noqa: F821

        "app.manufacturing.sales_forecast_item_domain.models.sales_forecast_item.SalesForecastItem",

        primaryjoin="and_(SalesForecast.id == SalesForecastItem.parent_id, SalesForecastItem.parentfield == 'selected_items')",

        overlaps="items",

        # shared child doctype: rows are separated by parentfield

        cascade="all, delete-orphan",

        foreign_keys=[SalesForecastItem.parent_id],

    )



    items: Mapped[list["SalesForecastItem"]] = relationship(  # noqa: F821

        "app.manufacturing.sales_forecast_item_domain.models.sales_forecast_item.SalesForecastItem",

        primaryjoin="and_(SalesForecast.id == SalesForecastItem.parent_id, SalesForecastItem.parentfield == 'items')",

        overlaps="selected_items",

        # shared child doctype: rows are separated by parentfield

        cascade="all, delete-orphan",

        foreign_keys=[SalesForecastItem.parent_id],

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SalesForecast id={self.id}>"
