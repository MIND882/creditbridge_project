"""

Sales Taxes and Charges Template -- converted from

``erpnext/accounts/doctype/sales_taxes_and_charges_template``.



A reusable set of sales tax lines.



``autoname`` upstream is ``f"{title} - {company_abbr}"``; with no Company doctype

here, ``name`` is the title, unique per tenant.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel, tenant_index



__all__ = ["SalesTaxesAndChargesTemplate"]





class SalesTaxesAndChargesTemplate(TenantModel):

    __tablename__ = "sales_taxes_and_charges_templates"

    __table_args__ = (

        UniqueConstraint(

            "business_id", "name", name="uq_sales_taxes_template_business_name"

        ),

        # Upstream allows only one enabled template per tax category.

        tenant_index("ix_sales_taxes_template_tax_category", "tax_category_id"),

    )



    name: Mapped[str] = mapped_column(String(140), nullable=False)

    title: Mapped[str] = mapped_column(String(140), nullable=False)



    #: Setting this clears the flag on every other template for the tenant.

    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    tax_category_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("tax_categories.id", ondelete="RESTRICT"), nullable=True, index=True

    )

    tax_category = relationship("TaxCategory", foreign_keys=[tax_category_id])



    taxes: Mapped[list["SalesTaxesAndCharges"]] = relationship(  # noqa: F821

        "SalesTaxesAndCharges",

        back_populates="parent",

        cascade="all, delete-orphan",

        passive_deletes=True,

        order_by="SalesTaxesAndCharges.idx",

    )



    def __repr__(self) -> str:

        return f"<SalesTaxesAndChargesTemplate id={self.id} name={self.name!r}>"
