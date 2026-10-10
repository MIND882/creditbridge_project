"""

Payment Terms Template -- converted from

``erpnext/accounts/doctype/payment_terms_template``.



A named set of instalment rules that an invoice points at. ``autoname`` is

``field:template_name``, so ``name`` is that field verbatim.



Validation is ported from ``payment_terms_template.py``: the portions across all

rows must total 100, and no two rows may repeat the same term/credit window.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import Boolean, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel, tenant_index



__all__ = ["PaymentTermsTemplate"]





class PaymentTermsTemplate(TenantModel):

    __tablename__ = "payment_terms_templates"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_payment_terms_template_business_name"),

        tenant_index("ix_payment_terms_template_name", "name"),

    )



    #: ``autoname = field:template_name``.

    name: Mapped[str] = mapped_column(String(140), nullable=False)

    template_name: Mapped[str] = mapped_column(String(140), nullable=False)



    #: When set, a payment against the invoice is matched to a specific term

    #: row rather than applied to the invoice as a whole -- which makes

    #: ``payment_term`` mandatory on every row.

    allocate_payment_based_on_payment_terms: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )



    terms: Mapped[list["PaymentTermsTemplateDetail"]] = relationship(  # noqa: F821

        "PaymentTermsTemplateDetail",

        back_populates="parent",

        cascade="all, delete-orphan",

        passive_deletes=True,

        order_by="PaymentTermsTemplateDetail.idx",

    )



    def __repr__(self) -> str:

        return f"<PaymentTermsTemplate id={self.id} name={self.name!r}>"
