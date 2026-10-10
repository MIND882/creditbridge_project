"""

Promotional Scheme Price Discount -- converted from ``erpnext/accounts/doctype/promotional_scheme_price_discount``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, ForeignKey, Numeric, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["PromotionalSchemePriceDiscount", "PromotionalSchemePriceDiscountRateOrDiscount", "PromotionalSchemePriceDiscountPriority"]







class PromotionalSchemePriceDiscountRateOrDiscount(str, enum.Enum):

    RATE = "Rate"

    DISCOUNT_PERCENTAGE = "Discount Percentage"

    DISCOUNT_AMOUNT = "Discount Amount"





class PromotionalSchemePriceDiscountPriority(str, enum.Enum):

    _1 = "1"

    _2 = "2"

    _3 = "3"

    _4 = "4"

    _5 = "5"

    _6 = "6"

    _7 = "7"

    _8 = "8"

    _9 = "9"

    _10 = "10"

    _11 = "11"

    _12 = "12"

    _13 = "13"

    _14 = "14"

    _15 = "15"

    _16 = "16"

    _17 = "17"

    _18 = "18"

    _19 = "19"

    _20 = "20"









class PromotionalSchemePriceDiscount(ChildTableModel, TenantModel):

    __tablename__ = "promotional_scheme_price_discounts"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("promotional_schemes.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("PromotionalScheme", back_populates="price_discount_slabs", foreign_keys=[parent_id])



    disable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    rule_description: Mapped[str] = mapped_column(String(140), nullable=False)

    min_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    max_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    min_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    max_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rate_or_discount: Mapped[Optional[PromotionalSchemePriceDiscountRateOrDiscount]] = mapped_column(

        SAEnum(PromotionalSchemePriceDiscountRateOrDiscount, native_enum=False, length=19, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    discount_percentage: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    for_price_list: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    warehouse: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    threshold_percentage: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    validate_applied_rule: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    priority: Mapped[Optional[PromotionalSchemePriceDiscountPriority]] = mapped_column(

        SAEnum(PromotionalSchemePriceDiscountPriority, native_enum=False, length=3, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    apply_multiple_pricing_rules: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    apply_discount_on_rate: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PromotionalSchemePriceDiscount id={self.id}>"
