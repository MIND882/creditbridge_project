"""

Purchase Taxes and Charges Template -- converted from

``erpnext/accounts/doctype/purchase_taxes_and_charges_template``.



A reusable set of purchase tax lines. Same shape as the sales template; the

upstream controller is thinner because the purchase row carries its own

``category``/``add_deduct_tax`` defaults rather than inheriting them.



``autoname`` upstream is ``f"{title} - {company_abbr}"``; with no Company doctype

here, ``name`` is the title, unique per tenant.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel, tenant_index



__all__ = ["PurchaseTaxesAndChargesTemplate"]





class PurchaseTaxesAndChargesTemplate(TenantModel):

    __tablename__ = "purchase_taxes_and_charges_templates"

    __table_args__ = (

        UniqueConstraint(

            "business_id", "name", name="uq_purchase_taxes_template_business_name"

        ),

        tenant_index("ix_purchase_taxes_template_tax_category", "tax_category_id"),

    )



    name: Mapped[str] = mapped_column(String(140), nullable=False)

    title: Mapped[str] = mapped_column(String(140), nullable=False)



    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    tax_category_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("tax_categories.id", ondelete="RESTRICT"), nullable=True, index=True

    )

    tax_category = relationship("TaxCategory", foreign_keys=[tax_category_id])



    taxes: Mapped[list["PurchaseTaxesAndCharges"]] = relationship(  # noqa: F821

        "PurchaseTaxesAndCharges",

        back_populates="parent",

        cascade="all, delete-orphan",

        passive_deletes=True,

        order_by="PurchaseTaxesAndCharges.idx",

    )



    def __repr__(self) -> str:

        return f"<PurchaseTaxesAndChargesTemplate id={self.id} name={self.name!r}>"
