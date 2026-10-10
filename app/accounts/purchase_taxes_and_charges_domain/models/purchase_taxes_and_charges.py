"""

PurchaseTaxesAndCharges -- converted from

``erpnext/accounts/doctype/purchase_taxes_and_charges``.



The purchase-side tax line. Compared with the sales row it adds ``category``

(whether the charge is capitalised into stock valuation) and ``add_deduct_tax``,

and drops the discount columns.



Upstream this table serves both Purchase Taxes and Charges Template and Purchase

Invoice; only the template is converted, so ``parent_id`` points there.

"""



from __future__ import annotations



import uuid

from decimal import Decimal

from typing import Optional



from sqlalchemy import Boolean, ForeignKey, Numeric, String, Text

from sqlalchemy import Enum as SAEnum

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.tax_enums import AddDeductTax, ChargeType, PurchaseTaxCategory

from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["PurchaseTaxesAndCharges"]





class PurchaseTaxesAndCharges(ChildTableModel, TenantModel):

    """One row of ``PurchaseTaxesAndChargesTemplate.taxes``."""



    __tablename__ = "purchase_taxes_and_charges"



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("purchase_taxes_and_charges_templates.id", ondelete="CASCADE"),

        nullable=True,

        index=True,

    )

    parent = relationship(

        "PurchaseTaxesAndChargesTemplate", back_populates="taxes", foreign_keys=[parent_id]

    )



    category: Mapped[Optional[PurchaseTaxCategory]] = mapped_column(

        SAEnum(PurchaseTaxCategory, name="ptc_category"),

        default=PurchaseTaxCategory.TOTAL,

        nullable=False,

    )

    add_deduct_tax: Mapped[Optional[AddDeductTax]] = mapped_column(

        SAEnum(AddDeductTax, name="ptc_add_deduct_tax"),

        default=AddDeductTax.ADD,

        nullable=False,

    )

    charge_type: Mapped[Optional[ChargeType]] = mapped_column(

        SAEnum(ChargeType, name="ptc_charge_type"),

        default=ChargeType.ON_NET_TOTAL,

        nullable=False,

    )



    row_id: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    allocate_full_amount_to_stock_items: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=True

    )

    included_in_print_rate: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    account_head_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"), nullable=False, index=True

    )

    account_head = relationship("Account", foreign_keys=[account_head_id])



    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"), nullable=True, index=True

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])



    description: Mapped[Optional[str]] = mapped_column(Text, nullable=False)



    rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    tax_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    tax_amount_after_discount_amount: Mapped[Optional[Decimal]] = mapped_column(

        Numeric(21, 9), nullable=True

    )

    total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    base_tax_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_tax_amount_after_discount_amount: Mapped[Optional[Decimal]] = mapped_column(

        Numeric(21, 9), nullable=True

    )



    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    included_in_paid_amount: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    account_currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    net_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_net_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    is_tax_withholding_account: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    set_by_item_tax_template: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    dont_recompute_tax: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PurchaseTaxesAndCharges id={self.id} idx={self.idx}>"
