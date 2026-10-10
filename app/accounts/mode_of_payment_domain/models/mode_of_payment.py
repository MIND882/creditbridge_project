"""

Mode of Payment -- converted from ``erpnext/accounts/doctype/mode_of_payment``.



A named way money moves (Cash, Bank, Phone, ...) plus the account each company

books it to. ``autoname`` is ``field:mode_of_payment``, so the name is the label.



Upstream ``validate()`` runs three checks, in this order:



    validate_accounts()             -> the row's account must belong to the row's

                                       company

    validate_repeating_companies()  -> the same company twice is an error

    validate_pos_mode_of_payment()  -> a mode referenced by a POS Profile cannot

                                       be disabled



``accounts.company`` stays a plain string rather than collapsing into

``business_id``. It is a *data* value here, not the tenancy key: the whole point

of the child table is to hold one row per company, and

``validate_repeating_companies`` only means anything when two rows can carry

different company values. The same call is made for

``accounting_dimension_detail.company``.



``validate_accounts`` cannot be ported literally, because ``Account.company``

collapsed into ``business_id`` -- there is no company string left to compare

against. What survives is the intent: the referenced account must belong here.

That is enforced by resolving the account through the tenant-scoped repository,

so a foreign or missing account fails the same way. See the service.



``validate_pos_mode_of_payment`` needs ``Sales Invoice Payment`` and

``POS Profile``, neither of which is converted yet. It is a stub that fails

open, with a TODO.

"""



from __future__ import annotations



import enum

from typing import Optional



from sqlalchemy import Boolean, String, UniqueConstraint

from sqlalchemy import Enum as SAEnum

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.mode_of_payment_account_domain.models.mode_of_payment_account import (

    ModeOfPaymentAccount,

)

from app.core.base_model import TenantModel, tenant_index



__all__ = ["ModeOfPayment", "ModeOfPaymentType"]





class ModeOfPaymentType(str, enum.Enum):

    CASH = "Cash"

    BANK = "Bank"

    GENERAL = "General"

    PHONE = "Phone"





class ModeOfPayment(TenantModel):

    """``autoname = field:mode_of_payment``."""



    __tablename__ = "mode_of_payments"

    __table_args__ = (

        UniqueConstraint(

            "business_id", "name", name="uq_mode_of_payments_business_name"

        ),

        tenant_index("ix_mode_of_payments_business_type", "type"),

    )



    name: Mapped[str] = mapped_column(String(140), nullable=False)

    mode_of_payment: Mapped[str] = mapped_column(String(140), nullable=False)



    type: Mapped[Optional[ModeOfPaymentType]] = mapped_column(

        SAEnum(ModeOfPaymentType, name="mode_of_payment_type"), nullable=True

    )



    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)



    accounts = relationship(

        ModeOfPaymentAccount,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=ModeOfPaymentAccount.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:

        return f"<ModeOfPayment id={self.id} name={self.name!r} type={self.type}>"
