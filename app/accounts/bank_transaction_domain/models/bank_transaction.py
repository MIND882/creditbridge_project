"""

Bank Transaction -- converted from ``erpnext/accounts/doctype/bank_transaction``.



Submittable, ``autoname`` is ``naming_series`` (``ACC-BTN-.YYYY.-#####``).



JSON field               Type here          Notes

-----------------------  -----------------  -------------------------------

naming_series            String(140) reqd

date                     Date

status                   Enum                derived, never taken from input

bank_account             FK -> acc_bank_accounts

company                  *collapsed*         -> business_id

currency                 String(140)         Link to Currency kept as a code

deposit / withdrawal     Numeric(21,9)

included_fee / excluded_fee  Numeric(21,9)   excluded_fee is consumed on save

allocated_amount         Numeric(21,9)       derived from the child table

unallocated_amount       Numeric(21,9)       derived

payment_entries          Table -> BankTransactionPayment

party_type / party       String(140)         Dynamic Link flattened

is_rule_evaluated        Boolean

matched_transaction_rule FK -> bank_transaction_rules



``transaction_id`` and ``reference_number`` stay as plain strings: upstream they

are the bank's own identifiers and carry no FK.

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

    String,

    Text,

    UniqueConstraint,

)

from sqlalchemy import Enum as SAEnum

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel, tenant_index

from app.core.docstatus import SubmittableModel



__all__ = ["BankTransaction", "BankTransactionStatus"]



#: ``naming_series`` is a single-option Select upstream; kept as a constant so

#: the series is discoverable rather than buried in the service.

NAMING_SERIES = "ACC-BTN-.YYYY.-"





class BankTransactionStatus(str, enum.Enum):

    """``status`` Select. Derived by :meth:`set_status`, never supplied by a client."""



    PENDING = "Pending"

    SETTLED = "Settled"

    UNRECONCILED = "Unreconciled"

    RECONCILED = "Reconciled"

    CANCELLED = "Cancelled"





class BankTransaction(SubmittableModel, TenantModel):

    """One line from a bank statement, plus its reconciliation allocations."""



    # `acc_bank_transactions`, not `bank_transactions`: the repository already

    # owns a `bank_transactions` table in app/models/bank_data.py (CreditBridge's

    # statement-ingest table). Both share one MetaData, so the names must differ

    # or `app.main` cannot import. Same reason BankAccount is `acc_bank_accounts`.

    __tablename__ = "acc_bank_transactions"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_acc_bank_txn_business_id_name"),

        tenant_index("ix_acc_bank_txn_business_date", "date"),

        tenant_index("ix_acc_bank_txn_business_status", "status"),

    )



    #: ``ACC-BTN-<year>-<#####>``, scoped per tenant and year.

    name: Mapped[str] = mapped_column(String(140), nullable=False)

    naming_series: Mapped[str] = mapped_column(

        String(140), nullable=False, default=NAMING_SERIES

    )



    date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    status: Mapped[BankTransactionStatus] = mapped_column(

        SAEnum(

            BankTransactionStatus, native_enum=False, length=20, validate_strings=True

        ),

        nullable=False,

        default=BankTransactionStatus.PENDING,

    )



    bank_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("acc_bank_accounts.id", ondelete="RESTRICT"), nullable=True, index=True

    )

    bank_account = relationship("app.accounts.bank_account_domain.models.bank_account.BankAccount", foreign_keys=[bank_account_id])



    currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    reference_number: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    transaction_id: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    deposit: Mapped[Optional[Decimal]] = mapped_column(

        Numeric(21, 9), nullable=True, default=Decimal("0")

    )

    withdrawal: Mapped[Optional[Decimal]] = mapped_column(

        Numeric(21, 9), nullable=True, default=Decimal("0")

    )

    included_fee: Mapped[Optional[Decimal]] = mapped_column(

        Numeric(21, 9), nullable=True, default=Decimal("0")

    )

    #: Consumed by ``handle_excluded_fee`` on save and zeroed out.

    excluded_fee: Mapped[Optional[Decimal]] = mapped_column(

        Numeric(21, 9), nullable=True, default=Decimal("0")

    )



    #: Derived from the child table by ``update_allocated_amount``.

    allocated_amount: Mapped[Optional[Decimal]] = mapped_column(

        Numeric(21, 9), nullable=True, default=Decimal("0")

    )

    unallocated_amount: Mapped[Optional[Decimal]] = mapped_column(

        Numeric(21, 9), nullable=True, default=Decimal("0")

    )



    party_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    party: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    transaction_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    bank_party_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    bank_party_iban: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    bank_party_account_number: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    is_rule_evaluated: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    matched_transaction_rule_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("bank_transaction_rules.id", ondelete="SET NULL"), nullable=True, index=True

    )

    matched_transaction_rule = relationship(

        "BankTransactionRule", foreign_keys=[matched_transaction_rule_id]

    )



    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("acc_bank_transactions.id", ondelete="SET NULL"), nullable=True

    )



    payment_entries: Mapped[list["BankTransactionPayment"]] = relationship(  # noqa: F821

        "BankTransactionPayment",

        back_populates="parent",

        cascade="all, delete-orphan",

        passive_deletes=True,

        order_by="BankTransactionPayment.idx",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<BankTransaction id={self.id} name={self.name!r} status={self.status!r}>"
