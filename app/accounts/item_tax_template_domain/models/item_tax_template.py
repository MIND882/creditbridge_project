"""

Item Tax Template -- converted from

``erpnext/accounts/doctype/item_tax_template``.



The tax treatment attached to an item, so a line on an invoice can override the

template's rates for that particular product.



``autoname`` upstream is ``f"{title} - {company_abbr}"``; with no Company doctype

here, ``name`` is the title, unique per tenant.

"""



from __future__ import annotations



from sqlalchemy import Boolean, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel, tenant_index



__all__ = ["ItemTaxTemplate"]





class ItemTaxTemplate(TenantModel):

    __tablename__ = "item_tax_templates"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_item_tax_template_business_name"),

        tenant_index("ix_item_tax_template_name", "name"),

    )



    name: Mapped[str] = mapped_column(String(140), nullable=False)

    title: Mapped[str] = mapped_column(String(140), nullable=False)

    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    taxes: Mapped[list["ItemTaxTemplateDetail"]] = relationship(  # noqa: F821

        "ItemTaxTemplateDetail",

        back_populates="parent",

        cascade="all, delete-orphan",

        passive_deletes=True,

        order_by="ItemTaxTemplateDetail.idx",

    )



    def __repr__(self) -> str:

        return f"<ItemTaxTemplate id={self.id} name={self.name!r}>"
