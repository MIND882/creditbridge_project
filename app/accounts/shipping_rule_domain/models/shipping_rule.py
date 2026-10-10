"""

Shipping Rule -- converted from ``erpnext/accounts/doctype/shipping_rule``.





"""



from __future__ import annotations



import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.shipping_rule_condition_domain.models.shipping_rule_condition import ShippingRuleCondition

from app.accounts.shipping_rule_country_domain.models.shipping_rule_country import ShippingRuleCountry



from app.accounts.account_domain.models.account import Account  # noqa: F401

from app.accounts.cost_center_domain.models.cost_center import CostCenter  # noqa: F401



from app.core.base_model import TenantModel



__all__ = ["ShippingRule", "ShippingRuleShippingRuleType", "ShippingRuleCalculateBasedOn"]







class ShippingRuleShippingRuleType(str, enum.Enum):

    SELLING = "Selling"

    BUYING = "Buying"





class ShippingRuleCalculateBasedOn(str, enum.Enum):

    FIXED = "Fixed"

    NET_TOTAL = "Net Total"

    NET_WEIGHT = "Net Weight"









class ShippingRule(TenantModel):

    __tablename__ = "shipping_rules"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_shipping_rules_business_name"),

    )



    #: ``autoname`` = 'field:label'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    label: Mapped[str] = mapped_column(String(140), nullable=False)

    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    shipping_rule_type: Mapped[Optional[ShippingRuleShippingRuleType]] = mapped_column(

        SAEnum(ShippingRuleShippingRuleType, native_enum=False, length=7, validate_strings=True),

        nullable=True,

    )

    account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    account = relationship("Account", foreign_keys=[account_id])

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])

    calculate_based_on: Mapped[Optional[ShippingRuleCalculateBasedOn]] = mapped_column(

        SAEnum(ShippingRuleCalculateBasedOn, native_enum=False, length=10, validate_strings=True),

        nullable=True,

    )

    shipping_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    conditions = relationship(

        ShippingRuleCondition,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=ShippingRuleCondition.idx,

        passive_deletes=True,

    )

    countries = relationship(

        ShippingRuleCountry,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=ShippingRuleCountry.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ShippingRule id={self.id}>"
