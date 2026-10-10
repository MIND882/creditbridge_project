"""

Payment Gateway Account -- converted from ``erpnext/accounts/doctype/payment_gateway_account``.





"""



from __future__ import annotations



import enum

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.account_domain.models.account import Account  # noqa: F401



from app.core.base_model import TenantModel



__all__ = ["PaymentGatewayAccount", "PaymentGatewayAccountPaymentChannel"]







class PaymentGatewayAccountPaymentChannel(str, enum.Enum):

    EMAIL = "Email"

    PHONE = "Phone"

    OTHER = "Other"









class PaymentGatewayAccount(TenantModel):

    __tablename__ = "payment_gateway_accounts"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_payment_gateway_accounts_business_name"),

    )



    #: Upstream declares no ``autoname``; Frappe mints a hash.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    payment_gateway: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    payment_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    payment_account = relationship("Account", foreign_keys=[payment_account_id])

    currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    message: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    payment_channel: Mapped[Optional[PaymentGatewayAccountPaymentChannel]] = mapped_column(

        SAEnum(PaymentGatewayAccountPaymentChannel, native_enum=False, length=5, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PaymentGatewayAccount id={self.id}>"
