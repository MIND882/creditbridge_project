"""

Loyalty Program -- converted from ``erpnext/accounts/doctype/loyalty_program``.





"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, Enum as SAEnum, ForeignKey, Integer, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.loyalty_program_collection_domain.models.loyalty_program_collection import LoyaltyProgramCollection



from app.accounts.account_domain.models.account import Account  # noqa: F401

from app.accounts.cost_center_domain.models.cost_center import CostCenter  # noqa: F401



from app.core.base_model import TenantModel



__all__ = ["LoyaltyProgram", "LoyaltyProgramLoyaltyProgramType"]







class LoyaltyProgramLoyaltyProgramType(str, enum.Enum):

    SINGLE_TIER_PROGRAM = "Single Tier Program"

    MULTIPLE_TIER_PROGRAM = "Multiple Tier Program"









class LoyaltyProgram(TenantModel):

    __tablename__ = "loyalty_programs"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_loyalty_programs_business_name"),

    )



    #: ``autoname`` = 'field:loyalty_program_name'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    loyalty_program_name: Mapped[str] = mapped_column(String(140), nullable=False)

    loyalty_program_type: Mapped[Optional[LoyaltyProgramLoyaltyProgramType]] = mapped_column(

        SAEnum(LoyaltyProgramLoyaltyProgramType, native_enum=False, length=21, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    from_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    to_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    customer_group: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    customer_territory: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    auto_opt_in: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    conversion_factor: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    expiry_duration: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    expense_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    expense_account = relationship("Account", foreign_keys=[expense_account_id])

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    collection_rules = relationship(

        LoyaltyProgramCollection,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=LoyaltyProgramCollection.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<LoyaltyProgram id={self.id}>"
