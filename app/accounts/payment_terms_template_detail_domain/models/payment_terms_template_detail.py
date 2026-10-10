"""

PaymentTermsTemplateDetail -- converted from

``erpnext/accounts/doctype/payment_terms_template_detail``.



One instalment row of ``PaymentTermsTemplate.terms``. Rows only ever exist

inside a template, so the API is read-only.

"""



from __future__ import annotations



import uuid

from decimal import Decimal

from typing import Optional



from sqlalchemy import ForeignKey, Integer, Numeric, String, Text

from sqlalchemy import Enum as SAEnum

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.payment_term_domain.models.payment_term import DiscountType, DueDateBasedOn

from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["PaymentTermsTemplateDetail"]





class PaymentTermsTemplateDetail(ChildTableModel, TenantModel):

    """One row of ``PaymentTermsTemplate.terms``."""



    __tablename__ = "payment_terms_template_details"



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("payment_terms_templates.id", ondelete="CASCADE"), nullable=True, index=True

    )

    parent = relationship(

        "PaymentTermsTemplate", back_populates="terms", foreign_keys=[parent_id]

    )



    payment_term_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("payment_terms.id", ondelete="RESTRICT"), nullable=True, index=True

    )

    payment_term = relationship("PaymentTerm", foreign_keys=[payment_term_id])



    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)



    #: Required and must total 100 across the template's rows.

    invoice_portion: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=False)



    due_date_based_on: Mapped[Optional[DueDateBasedOn]] = mapped_column(

        SAEnum(DueDateBasedOn, name="due_date_based_on"), nullable=False

    )

    credit_days: Mapped[Optional[int]] = mapped_column(Integer, default=0, nullable=True)

    credit_months: Mapped[Optional[int]] = mapped_column(Integer, default=0, nullable=True)



    #: Mode of Payment is its own doctype and is not converted.

    mode_of_payment: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    discount_type: Mapped[Optional[DiscountType]] = mapped_column(

        SAEnum(DiscountType, name="discount_type"), default=DiscountType.PERCENTAGE, nullable=True

    )

    discount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    discount_validity_based_on: Mapped[Optional[DueDateBasedOn]] = mapped_column(

        SAEnum(DueDateBasedOn, name="discount_validity_based_on"),

        default=DueDateBasedOn.DAYS_AFTER_INVOICE_DATE,

        nullable=True,

    )

    discount_validity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PaymentTermsTemplateDetail id={self.id} idx={self.idx}>"
