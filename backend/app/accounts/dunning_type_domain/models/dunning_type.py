"""

Dunning Type -- converted from ``erpnext/accounts/doctype/dunning_type``.



A chase-up policy for late payers: the fee charged, the interest rate applied,

and the letter text to send.



Upstream's ``autoname`` is ``f"{dunning_type} - {company_abbr}"`` -- the label

plus the company's abbreviation. There is no Company doctype here, so ``name``

is the ``dunning_type`` label, unique per tenant.

"""



from __future__ import annotations



import uuid

from decimal import Decimal

from typing import Optional



from sqlalchemy import Boolean, ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel, tenant_index



__all__ = ["DunningType"]





class DunningType(TenantModel):

    __tablename__ = "dunning_types"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_dunning_type_business_name"),

        # Upstream keeps exactly one default per company; enforced in the

        # service, and this index makes the lookup cheap.

        tenant_index("ix_dunning_type_is_default", "is_default"),

    )



    name: Mapped[str] = mapped_column(String(140), nullable=False)

    dunning_type: Mapped[str] = mapped_column(String(140), nullable=False)



    dunning_fee: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rate_of_interest: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    #: Setting this clears the flag on every other row for the tenant.

    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    #: Must be a non-group, enabled Income account.

    income_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"), nullable=True, index=True

    )

    income_account = relationship("Account", foreign_keys=[income_account_id])



    #: Must be a non-group, enabled cost centre.

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"), nullable=True, index=True

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])



    dunning_letter_text: Mapped[list["DunningLetterText"]] = relationship(  # noqa: F821

        "DunningLetterText",

        cascade="all, delete-orphan",

        passive_deletes=True,

        order_by="DunningLetterText.idx",

    )



    def __repr__(self) -> str:

        return f"<DunningType id={self.id} name={self.name!r}>"
