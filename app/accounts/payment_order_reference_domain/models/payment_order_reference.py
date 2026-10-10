"""

Payment Order Reference -- converted from ``erpnext/accounts/doctype/payment_order_reference``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import ForeignKey, Numeric, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.account_domain.models.account import Account  # noqa: F401

from app.accounts.bank_account_domain.models.bank_account import BankAccount  # noqa: F401

from app.accounts.mode_of_payment_domain.models.mode_of_payment import ModeOfPayment  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["PaymentOrderReference"]







class PaymentOrderReference(ChildTableModel, TenantModel):

    __tablename__ = "payment_order_references"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("payment_orders.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("PaymentOrder", back_populates="references", foreign_keys=[parent_id])



    reference_doctype: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    reference_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    amount: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    supplier: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    payment_request: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    mode_of_payment_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("mode_of_payments.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    mode_of_payment = relationship("ModeOfPayment", foreign_keys=[mode_of_payment_id])

    bank_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("acc_bank_accounts.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    bank_account = relationship("app.accounts.bank_account_domain.models.bank_account.BankAccount", foreign_keys=[bank_account_id])

    account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    account = relationship("Account", foreign_keys=[account_id])

    payment_reference: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PaymentOrderReference id={self.id}>"
