"""

Payment Entry -- converted from ``erpnext/accounts/doctype/payment_entry``.



Submittable, ``autoname`` is ``naming_series`` (``ACC-PAY-.YYYY.-#####``).

Records money received from a customer, paid to a supplier, or moved between two

of the tenant's own accounts.



JSON field               Type here          Notes

-----------------------  -----------------  -------------------------------

payment_type             Enum reqd          Receive / Pay / Internal Transfer

posting_date             Date      reqd

paid_from / paid_to      FK -> accounts reqd

paid_amount / received_amount  Numeric(21,9)

source/target_exchange_rate    Float  reqd

references               Table -> PaymentEntryReference

deductions               Table -> PaymentEntryDeduction

party_type / party       String(140)        Dynamic Link flattened

unallocated_amount       Numeric(21,9)      derived

difference_amount        Numeric(21,9)      derived; must be zero to submit

company                  *collapsed*        -> business_id



Upstream's controller is ~3,300 lines, most of it reconciling this payment

against Sales/Purchase Invoices and Payment Requests. Those doctypes are not

converted, so the invoice-allocation half is a documented stub

(:meth:`PaymentEntryService.sync_reference_outstandings`); the arithmetic,

duplicate and allocation guards that protect the ledger are ported in full.

"""



from __future__ import annotations



import enum

import uuid

from datetime import date

from decimal import Decimal

from typing import Optional



from sqlalchemy import (

    Boolean,

    Date,

    ForeignKey,

    Numeric,

    Float,

    String,

    Text,

    UniqueConstraint,

)

from sqlalchemy import Enum as SAEnum

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel, tenant_index

from app.core.docstatus import SubmittableModel



__all__ = ["PaymentEntry", "PaymentType", "NAMING_SERIES"]



NAMING_SERIES = "ACC-PAY-.YYYY.-"





class PaymentType(str, enum.Enum):

    RECEIVE = "Receive"

    PAY = "Pay"

    INTERNAL_TRANSFER = "Internal Transfer"





class PaymentEntry(SubmittableModel, TenantModel):

    """A receipt, payment, or internal transfer."""



    __tablename__ = "payment_entries"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_payment_entries_business_id_name"),

        tenant_index("ix_payment_entries_business_posting_date", "posting_date"),

        tenant_index("ix_payment_entries_business_party", "party_type", "party"),

    )



    #: ``ACC-PAY-<year>-<#####>``, scoped per tenant and year.

    name: Mapped[str] = mapped_column(String(140), nullable=False)

    naming_series: Mapped[str] = mapped_column(

        String(140), nullable=False, default=NAMING_SERIES

    )



    payment_type: Mapped[PaymentType] = mapped_column(

        SAEnum(PaymentType, native_enum=False, length=20, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=False,

    )

    posting_date: Mapped[date] = mapped_column(Date, nullable=False)



    paid_from_id: Mapped[uuid.UUID] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"), nullable=False, index=True

    )

    paid_from = relationship("Account", foreign_keys=[paid_from_id])



    paid_to_id: Mapped[uuid.UUID] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"), nullable=False, index=True

    )

    paid_to = relationship("Account", foreign_keys=[paid_to_id])



    paid_amount: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False)

    received_amount: Mapped[Optional[Decimal]] = mapped_column(

        Numeric(21, 9), nullable=True, default=Decimal("0")

    )

    source_exchange_rate: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)

    target_exchange_rate: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)



    paid_from_account_currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    paid_to_account_currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    party_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    party: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    party_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"), nullable=True, index=True

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])



    mode_of_payment: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    bank_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("acc_bank_accounts.id", ondelete="RESTRICT"), nullable=True, index=True

    )

    bank_account = relationship("app.accounts.bank_account_domain.models.bank_account.BankAccount", foreign_keys=[bank_account_id])

    party_bank_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("acc_bank_accounts.id", ondelete="RESTRICT"), nullable=True

    )



    reference_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    reference_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    remarks: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    title: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_opening: Mapped[str] = mapped_column(String(3), nullable=False, default="No")

    apply_tds: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    #: Derived; never taken from input.

    unallocated_amount: Mapped[Optional[Decimal]] = mapped_column(

        Numeric(21, 9), nullable=True, default=Decimal("0")

    )

    total_allocated_amount: Mapped[Optional[Decimal]] = mapped_column(

        Numeric(21, 9), nullable=True, default=Decimal("0")

    )

    total_deduction_amount: Mapped[Optional[Decimal]] = mapped_column(

        Numeric(21, 9), nullable=True, default=Decimal("0")

    )

    difference_amount: Mapped[Optional[Decimal]] = mapped_column(

        Numeric(21, 9), nullable=True, default=Decimal("0")

    )

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Draft")



    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("payment_entries.id", ondelete="SET NULL"), nullable=True

    )



    references: Mapped[list["PaymentEntryReference"]] = relationship(  # noqa: F821

        "PaymentEntryReference",

        back_populates="parent",

        cascade="all, delete-orphan",

        passive_deletes=True,

        order_by="PaymentEntryReference.idx",

    )

    deductions: Mapped[list["PaymentEntryDeduction"]] = relationship(  # noqa: F821

        "PaymentEntryDeduction",

        back_populates="parent",

        cascade="all, delete-orphan",

        passive_deletes=True,

        order_by="PaymentEntryDeduction.idx",

    )

    #: Upstream's ``taxes`` grid. Added in batch 7 once the child doctype

    #: existed; it was absent from the batch-5b model.

    taxes: Mapped[list["AdvanceTaxesAndCharges"]] = relationship(  # noqa: F821

        "AdvanceTaxesAndCharges",

        back_populates="parent",

        cascade="all, delete-orphan",

        passive_deletes=True,

        order_by="AdvanceTaxesAndCharges.idx",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PaymentEntry id={self.id} name={self.name!r} type={self.payment_type!r}>"
