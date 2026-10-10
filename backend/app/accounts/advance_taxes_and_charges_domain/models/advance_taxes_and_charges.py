"""

AdvanceTaxesAndCharges -- converted from

``erpnext/accounts/doctype/advance_taxes_and_charges``.



One row of ``PaymentEntry.taxes``: a tax charge carried on an advance.



Rows only ever exist inside a payment entry, so the API is read-only.

"""



from __future__ import annotations



import uuid

from decimal import Decimal

from typing import Optional



from sqlalchemy import Boolean, ForeignKey, Numeric, String, Text

from sqlalchemy import Enum as SAEnum

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.tax_enums import AddDeductTax, ChargeType

from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["AdvanceTaxesAndCharges"]





class AdvanceTaxesAndCharges(ChildTableModel, TenantModel):

    """One row of ``PaymentEntry.taxes``."""



    __tablename__ = "advance_taxes_and_charges"



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("payment_entries.id", ondelete="CASCADE"), nullable=True, index=True

    )

    parent = relationship("PaymentEntry", back_populates="taxes", foreign_keys=[parent_id])



    charge_type: Mapped[Optional[ChargeType]] = mapped_column(

        SAEnum(ChargeType, name="atc_charge_type"), nullable=False

    )

    add_deduct_tax: Mapped[Optional[AddDeductTax]] = mapped_column(

        SAEnum(AddDeductTax, name="atc_add_deduct_tax"), nullable=False

    )



    #: Set only for the "On Previous Row ..." charge types.

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

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    tax_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    base_tax_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    included_in_paid_amount: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    net_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_net_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    set_by_item_tax_template: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    is_tax_withholding_account: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<AdvanceTaxesAndCharges id={self.id} idx={self.idx}>"
