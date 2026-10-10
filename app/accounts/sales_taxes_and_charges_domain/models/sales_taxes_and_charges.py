"""

SalesTaxesAndCharges -- converted from

``erpnext/accounts/doctype/sales_taxes_and_charges``.



One tax line: which account it posts to, how it is computed, and the resulting

amount.



Upstream this table serves two parents -- Sales Taxes and Charges Template and

Sales Invoice. Only the template is converted, so ``parent_id`` points there.

When Sales Invoice lands it becomes a polymorphic parent, which is a matter of

adding a discriminator column rather than restructuring this model.

"""



from __future__ import annotations



import uuid

from decimal import Decimal

from typing import Optional



from sqlalchemy import Boolean, ForeignKey, Numeric, String, Text

from sqlalchemy import Enum as SAEnum

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.tax_enums import ChargeType

from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["SalesTaxesAndCharges"]





class SalesTaxesAndCharges(ChildTableModel, TenantModel):

    """One row of ``SalesTaxesAndChargesTemplate.taxes``."""



    __tablename__ = "sales_taxes_and_charges"



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("sales_taxes_and_charges_templates.id", ondelete="CASCADE"),

        nullable=True,

        index=True,

    )

    parent = relationship(

        "SalesTaxesAndChargesTemplate", back_populates="taxes", foreign_keys=[parent_id]

    )



    charge_type: Mapped[Optional[ChargeType]] = mapped_column(

        SAEnum(ChargeType, name="stc_charge_type"), nullable=False

    )



    #: Referenced by the "On Previous Row ..." charge types.

    row_id: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    account_head_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"), nullable=False, index=True

    )

    account_head = relationship("Account", foreign_keys=[account_head_id])



    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"), nullable=True, index=True

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])



    description: Mapped[Optional[str]] = mapped_column(Text, nullable=False)



    included_in_print_rate: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    tax_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    tax_amount_after_discount_amount: Mapped[Optional[Decimal]] = mapped_column(

        Numeric(21, 9), nullable=True

    )



    base_tax_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_tax_amount_after_discount_amount: Mapped[Optional[Decimal]] = mapped_column(

        Numeric(21, 9), nullable=True

    )



    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    included_in_paid_amount: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    dont_recompute_tax: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    account_currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    net_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_net_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    set_by_item_tax_template: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    is_tax_withholding_account: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SalesTaxesAndCharges id={self.id} idx={self.idx}>"
