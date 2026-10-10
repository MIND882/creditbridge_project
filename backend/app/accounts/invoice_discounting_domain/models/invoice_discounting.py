"""

Invoice Discounting -- converted from ``erpnext/accounts/doctype/invoice_discounting``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Date, Enum as SAEnum, ForeignKey, Integer, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.discounted_invoice_domain.models.discounted_invoice import DiscountedInvoice



from app.accounts.account_domain.models.account import Account  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["InvoiceDiscounting", "InvoiceDiscountingStatus"]







class InvoiceDiscountingStatus(str, enum.Enum):

    DRAFT = "Draft"

    SANCTIONED = "Sanctioned"

    DISBURSED = "Disbursed"

    SETTLED = "Settled"

    CANCELLED = "Cancelled"









class InvoiceDiscounting(SubmittableModel, TenantModel):

    __tablename__ = "invoice_discountings"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_invoice_discountings_business_name"),

    )



    #: ``autoname`` = 'ACC-INV-DISC-.YYYY.-.#####'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    posting_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    loan_start_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    loan_period: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    loan_end_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    status: Mapped[Optional[InvoiceDiscountingStatus]] = mapped_column(

        SAEnum(InvoiceDiscountingStatus, native_enum=False, length=10, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    total_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    bank_charges: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    short_term_loan_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    short_term_loan = relationship("Account", foreign_keys=[short_term_loan_id])

    bank_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    bank_account = relationship("Account", foreign_keys=[bank_account_id])

    bank_charges_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    bank_charges_account = relationship("Account", foreign_keys=[bank_charges_account_id])

    accounts_receivable_credit_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    accounts_receivable_credit = relationship("Account", foreign_keys=[accounts_receivable_credit_id])

    accounts_receivable_discounted_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    accounts_receivable_discounted = relationship("Account", foreign_keys=[accounts_receivable_discounted_id])

    accounts_receivable_unpaid_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    accounts_receivable_unpaid = relationship("Account", foreign_keys=[accounts_receivable_unpaid_id])

    amended_from: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    invoices = relationship(

        DiscountedInvoice,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=DiscountedInvoice.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<InvoiceDiscounting id={self.id}>"
