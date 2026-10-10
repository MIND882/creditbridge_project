"""

Tax Withholding Category -- converted from

``erpnext/accounts/doctype/tax_withholding_category``.



A named withholding rule: a set of dated rates plus the ledger accounts the

withheld tax lands in.



``autoname`` is ``Prompt``, i.e. the user types the name. ``category_name`` is

the label, so ``name`` is taken from it rather than generated.

"""



from __future__ import annotations



import enum

import uuid

from typing import Optional



from sqlalchemy import Boolean, String, UniqueConstraint

from sqlalchemy import Enum as SAEnum

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel, tenant_index



__all__ = ["TaxWithholdingCategory", "TaxDeductionBasis"]





class TaxDeductionBasis(str, enum.Enum):

    GROSS_TOTAL = "Gross Total"

    NET_TOTAL = "Net Total"





class TaxWithholdingCategory(TenantModel):

    __tablename__ = "tax_withholding_categories"

    __table_args__ = (

        UniqueConstraint(

            "business_id", "name", name="uq_tax_withholding_category_business_name"

        ),

        tenant_index("ix_tax_withholding_category_name", "name"),

    )



    #: ``autoname = Prompt``; ``category_name`` is the label the user types.

    name: Mapped[str] = mapped_column(String(140), nullable=False)

    category_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    #: Withhold on the amount above the threshold rather than on the whole

    #: amount once the threshold is crossed.

    tax_on_excess_amount: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    round_off_tax_amount: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    tax_deduction_basis: Mapped[Optional[TaxDeductionBasis]] = mapped_column(

        SAEnum(TaxDeductionBasis, name="tax_deduction_basis"),

        default=TaxDeductionBasis.NET_TOTAL,

        nullable=False,

    )



    disable_cumulative_threshold: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    disable_transaction_threshold: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )



    rates: Mapped[list["TaxWithholdingRate"]] = relationship(  # noqa: F821

        "TaxWithholdingRate",

        cascade="all, delete-orphan",

        passive_deletes=True,

        order_by="TaxWithholdingRate.idx",

    )

    accounts: Mapped[list["TaxWithholdingAccount"]] = relationship(  # noqa: F821

        "TaxWithholdingAccount",

        cascade="all, delete-orphan",

        passive_deletes=True,

        order_by="TaxWithholdingAccount.idx",

    )



    def __repr__(self) -> str:

        return f"<TaxWithholdingCategory id={self.id} name={self.name!r}>"
