"""

Payment Reconciliation -- converted from ``erpnext/accounts/doctype/payment_reconciliation``.





"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.payment_reconciliation_allocation_domain.models.payment_reconciliation_allocation import PaymentReconciliationAllocation

from app.accounts.payment_reconciliation_invoice_domain.models.payment_reconciliation_invoice import PaymentReconciliationInvoice

from app.accounts.payment_reconciliation_payment_domain.models.payment_reconciliation_payment import PaymentReconciliationPayment



from app.accounts.account_domain.models.account import Account  # noqa: F401

from app.accounts.cost_center_domain.models.cost_center import CostCenter  # noqa: F401



from app.core.base_model import TenantModel



__all__ = ["PaymentReconciliation"]







class PaymentReconciliation(TenantModel):

    __tablename__ = "payment_reconciliations"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_payment_reconciliations_business_name"),

    )



    #: Upstream declares no ``autoname``; Frappe mints a hash.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    party_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    party: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    receivable_payable_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    receivable_payable_account = relationship("Account", foreign_keys=[receivable_payable_account_id])

    bank_cash_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    bank_cash_account = relationship("Account", foreign_keys=[bank_cash_account_id])

    from_invoice_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    to_invoice_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    minimum_invoice_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    invoice_limit: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    from_payment_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    to_payment_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    minimum_payment_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    maximum_payment_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    payment_limit: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    maximum_invoice_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    default_advance_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    default_advance_account = relationship("Account", foreign_keys=[default_advance_account_id])

    invoice_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    payment_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    payments = relationship(

        PaymentReconciliationPayment,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=PaymentReconciliationPayment.idx,

        passive_deletes=True,

    )

    invoices = relationship(

        PaymentReconciliationInvoice,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=PaymentReconciliationInvoice.idx,

        passive_deletes=True,

    )

    allocation = relationship(

        PaymentReconciliationAllocation,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=PaymentReconciliationAllocation.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PaymentReconciliation id={self.id}>"
