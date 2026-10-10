"""

Promotional Scheme Product Discount -- converted from ``erpnext/accounts/doctype/promotional_scheme_product_discount``.



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



__all__ = ["PromotionalSchemeProductDiscount", "PromotionalSchemeProductDiscountPriority"]







class PromotionalSchemeProductDiscountPriority(str, enum.Enum):

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









class PromotionalSchemeProductDiscount(ChildTableModel, TenantModel):

    __tablename__ = "promotional_scheme_product_discounts"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("promotional_schemes.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("PromotionalScheme", back_populates="product_discount_slabs", foreign_keys=[parent_id])



    disable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    rule_description: Mapped[str] = mapped_column(String(140), nullable=False)

    min_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    max_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    min_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    max_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    same_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    free_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    free_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    free_item_uom: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    free_item_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    warehouse: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    threshold_percentage: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    priority: Mapped[Optional[PromotionalSchemeProductDiscountPriority]] = mapped_column(

        SAEnum(PromotionalSchemeProductDiscountPriority, native_enum=False, length=3, validate_strings=True),

        nullable=True,

    )

    apply_multiple_pricing_rules: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    is_recursive: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    recurse_for: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    apply_recursion_over: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    round_free_qty: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PromotionalSchemeProductDiscount id={self.id}>"
