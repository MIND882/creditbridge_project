"""Pydantic v2 schemas for CouponCode."""





from __future__ import annotations

from app.accounts.coupon_code_domain.models.coupon_code import (

    CouponCodeCouponType,

)

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "CouponCodeCreate",

    "CouponCodeUpdate",

    "CouponCodeRead",

    "CouponCodeListResponse",

]





class CouponCodeBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    coupon_name: str

    coupon_type: CouponCodeCouponType

    customer: Optional[str] = None

    coupon_code: Optional[str] = None

    pricing_rule: Optional[str] = None

    valid_from: Optional[dt.date] = None

    valid_upto: Optional[dt.date] = None

    maximum_use: Optional[int] = None

    used: Optional[int] = None

    description: Optional[str] = None

    amended_from: Optional[str] = None

    from_external_ecomm_platform: Optional[bool] = None





class CouponCodeCreate(CouponCodeBase):

    pass





class CouponCodeUpdate(InputSchema):

    """A partial update."""



    coupon_name: Optional[str] = None

    coupon_type: Optional[CouponCodeCouponType] = None

    customer: Optional[str] = None

    coupon_code: Optional[str] = None

    pricing_rule: Optional[str] = None

    valid_from: Optional[dt.date] = None

    valid_upto: Optional[dt.date] = None

    maximum_use: Optional[int] = None

    used: Optional[int] = None

    description: Optional[str] = None

    amended_from: Optional[str] = None

    from_external_ecomm_platform: Optional[bool] = None





class CouponCodeRead(ReadSchema):

    id: uuid.UUID

    name: str

    coupon_name: str

    coupon_type: CouponCodeCouponType

    customer: Optional[str] = None

    coupon_code: Optional[str] = None

    pricing_rule: Optional[str] = None

    valid_from: Optional[dt.date] = None

    valid_upto: Optional[dt.date] = None

    maximum_use: Optional[int] = None

    used: Optional[int] = None

    description: Optional[str] = None

    amended_from: Optional[str] = None

    from_external_ecomm_platform: bool





CouponCodeListResponse = Page[CouponCodeRead]
