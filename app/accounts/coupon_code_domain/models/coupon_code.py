"""

Coupon Code -- converted from ``erpnext/accounts/doctype/coupon_code``.





"""



from __future__ import annotations



import datetime as dt

import enum

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, Enum as SAEnum, Integer, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["CouponCode", "CouponCodeCouponType"]







class CouponCodeCouponType(str, enum.Enum):

    PROMOTIONAL = "Promotional"

    GIFT_CARD = "Gift Card"









class CouponCode(TenantModel):

    __tablename__ = "coupon_codes"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_coupon_codes_business_name"),

    )



    #: ``autoname`` = 'field:coupon_name'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    coupon_name: Mapped[str] = mapped_column(String(140), nullable=False)

    coupon_type: Mapped[CouponCodeCouponType] = mapped_column(

        SAEnum(CouponCodeCouponType, native_enum=False, length=11, validate_strings=True),

        nullable=False,

    )

    customer: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    coupon_code: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    pricing_rule: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    valid_from: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    valid_upto: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    maximum_use: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    used: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    amended_from: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    from_external_ecomm_platform: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<CouponCode id={self.id}>"
