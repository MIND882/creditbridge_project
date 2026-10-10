"""

Bank Transaction Rule -- converted from

``erpnext/accounts/doctype/bank_transaction_rule``.



A rule auto-classifies incoming bank transactions: it matches on direction,

amount range and description, then says how to book the match. ``autoname`` is

``field:rule_name`` and ``priority`` orders evaluation within a tenant.



JSON field          Type here         Notes

------------------  ----------------  ----------------------------------

rule_name           String(140) reqd  also the document name

transaction_type    Enum reqd         Any / Withdrawal / Deposit

min_amount / max_amount  Numeric(21,9)

classify_as         Enum reqd         Bank Entry / Payment Entry / Transfer

bank_entry_type     Enum              Single Account / Multiple Accounts

account             FK -> accounts

party_type / party  String(140)       Dynamic Link flattened

priority            Integer reqd      auto-assigned on create

company             *collapsed*       -> business_id

description_rules   Table REQD

accounts            Table



``debit``/``credit`` on the child rows are *formula strings*, not amounts --

upstream evaluates them with ``transaction_amount`` bound. They stay strings

here for the same reason.

"""



from __future__ import annotations



import enum

import uuid

from decimal import Decimal

from typing import Optional



from sqlalchemy import (

    ForeignKey,

    Integer,

    Numeric,

    String,

    Text,

    UniqueConstraint,

)

from sqlalchemy import Enum as SAEnum

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel, tenant_index



__all__ = [

    "BankTransactionRule",

    "RuleTransactionType",

    "RuleClassifyAs",

    "RuleBankEntryType",

]





class RuleTransactionType(str, enum.Enum):

    ANY = "Any"

    WITHDRAWAL = "Withdrawal"

    DEPOSIT = "Deposit"





class RuleClassifyAs(str, enum.Enum):

    BANK_ENTRY = "Bank Entry"

    PAYMENT_ENTRY = "Payment Entry"

    TRANSFER = "Transfer"





class RuleBankEntryType(str, enum.Enum):

    SINGLE_ACCOUNT = "Single Account"

    MULTIPLE_ACCOUNTS = "Multiple Accounts"





class BankTransactionRule(TenantModel):

    """An auto-classification rule, evaluated in ``priority`` order."""



    __tablename__ = "bank_transaction_rules"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_bank_txn_rules_business_id_name"),

        tenant_index("ix_bank_txn_rules_business_priority", "priority"),

    )



    #: ``autoname: field:rule_name``.

    name: Mapped[str] = mapped_column(String(140), nullable=False)

    rule_name: Mapped[str] = mapped_column(String(140), nullable=False)



    transaction_type: Mapped[RuleTransactionType] = mapped_column(

        SAEnum(RuleTransactionType, native_enum=False, length=20, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=False,

        default=RuleTransactionType.ANY,

    )



    min_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    max_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rule_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)



    classify_as: Mapped[RuleClassifyAs] = mapped_column(

        SAEnum(RuleClassifyAs, native_enum=False, length=20, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=False,

    )

    bank_entry_type: Mapped[Optional[RuleBankEntryType]] = mapped_column(

        SAEnum(RuleBankEntryType, native_enum=False, length=20, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )



    account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"), nullable=True, index=True

    )

    account = relationship("Account", foreign_keys=[account_id])



    party_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    party: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    #: Evaluation order within the tenant; auto-assigned and renumbered on delete.

    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=1)



    description_rules: Mapped[list["BankTransactionRuleDescriptionCondition"]] = relationship(  # noqa: F821

        "BankTransactionRuleDescriptionCondition",

        back_populates="parent",

        cascade="all, delete-orphan",

        passive_deletes=True,

        order_by="BankTransactionRuleDescriptionCondition.idx",

    )

    accounts: Mapped[list["BankTransactionRuleAccount"]] = relationship(  # noqa: F821

        "BankTransactionRuleAccount",

        back_populates="parent",

        cascade="all, delete-orphan",

        passive_deletes=True,

        order_by="BankTransactionRuleAccount.idx",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<BankTransactionRule id={self.id} name={self.name!r} priority={self.priority}>"
