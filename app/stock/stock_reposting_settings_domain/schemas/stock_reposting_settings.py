"""Pydantic v2 schemas for StockRepostingSettings."""





from __future__ import annotations

from app.stock.stock_reposting_settings_domain.models.stock_reposting_settings import (

    StockRepostingSettingsLimitsDontApplyOn,

)

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "StockRepostingSettingsUpdate",

    "StockRepostingSettingsRead",

]





class StockRepostingSettingsUpdate(InputSchema):

    """A partial update of the tenant settings row."""



    start_time: Optional[dt.time] = None

    end_time: Optional[dt.time] = None

    limits_dont_apply_on: Optional[StockRepostingSettingsLimitsDontApplyOn] = None

    limit_reposting_timeslot: Optional[bool] = None

    item_based_reposting: Optional[bool] = None

    notify_reposting_error_to_role: Optional[str] = None

    enable_parallel_reposting: Optional[bool] = None

    no_of_parallel_reposting: Optional[int] = None

    enable_separate_reposting_for_gl: Optional[bool] = None

    do_not_fetch_incoming_rate_from_serial_no: Optional[bool] = None

    repost_incorrect_valuation_entries: Optional[bool] = None





class StockRepostingSettingsRead(ReadSchema):

    id: uuid.UUID

    start_time: Optional[dt.time] = None

    end_time: Optional[dt.time] = None

    limits_dont_apply_on: Optional[StockRepostingSettingsLimitsDontApplyOn] = None

    limit_reposting_timeslot: Optional[bool] = None

    item_based_reposting: Optional[bool] = None

    notify_reposting_error_to_role: Optional[str] = None

    enable_parallel_reposting: Optional[bool] = None

    no_of_parallel_reposting: Optional[int] = None

    enable_separate_reposting_for_gl: Optional[bool] = None

    do_not_fetch_incoming_rate_from_serial_no: Optional[bool] = None

    repost_incorrect_valuation_entries: Optional[bool] = None


