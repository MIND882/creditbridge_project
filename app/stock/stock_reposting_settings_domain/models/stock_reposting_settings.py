"""

Stock Reposting Settings -- converted from ``erpnext/stock/doctype/stock_reposting_settings``.



A Frappe Single (``issingle: 1``): one row per ``business_id``, enforced by a unique constraint on ``business_id`` alone.

"""



from __future__ import annotations



import datetime as dt

import enum

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, Integer, String, Time, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["StockRepostingSettings", "StockRepostingSettingsLimitsDontApplyOn"]





class StockRepostingSettingsLimitsDontApplyOn(str, enum.Enum):

    MONDAY = "Monday"

    TUESDAY = "Tuesday"

    WEDNESDAY = "Wednesday"

    THURSDAY = "Thursday"

    FRIDAY = "Friday"

    SATURDAY = "Saturday"

    SUNDAY = "Sunday"





class StockRepostingSettings(TenantModel):

    __tablename__ = "stock_reposting_settingss"

    __table_args__ = (

        UniqueConstraint("business_id", name="uq_stock_reposting_settingss_business"),

    )



    start_time: Mapped[Optional[dt.time]] = mapped_column(Time, nullable=True)

    end_time: Mapped[Optional[dt.time]] = mapped_column(Time, nullable=True)

    limits_dont_apply_on: Mapped[Optional[str]] = mapped_column(SAEnum(StockRepostingSettingsLimitsDontApplyOn, native_enum=False, length=13, validate_strings=True), nullable=True)

    limit_reposting_timeslot: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    item_based_reposting: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    notify_reposting_error_to_role: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    enable_parallel_reposting: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    no_of_parallel_reposting: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=4)

    enable_separate_reposting_for_gl: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    do_not_fetch_incoming_rate_from_serial_no: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    repost_incorrect_valuation_entries: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<StockRepostingSettings id={self.id}>"
