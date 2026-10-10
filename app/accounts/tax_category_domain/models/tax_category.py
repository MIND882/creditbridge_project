"""

Tax Category -- converted from ``erpnext/accounts/doctype/tax_category``.



A label that ties a transaction to a tax template, so an invoice can say "this

is an export" without repeating the tax rows.



``autoname`` is ``field:title``. Upstream's controller is empty -- there is no

validation to port.

"""



from __future__ import annotations



from sqlalchemy import Boolean, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel, tenant_index



__all__ = ["TaxCategory"]





class TaxCategory(TenantModel):

    __tablename__ = "tax_categories"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_tax_category_business_name"),

        tenant_index("ix_tax_category_name", "name"),

    )



    #: ``autoname = field:title``.

    name: Mapped[str] = mapped_column(String(140), nullable=False)

    title: Mapped[str] = mapped_column(String(140), nullable=False)

    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    def __repr__(self) -> str:

        return f"<TaxCategory id={self.id} name={self.name!r}>"
