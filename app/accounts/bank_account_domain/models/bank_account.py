"""

Bank Account -- converted from ``erpnext/accounts/doctype/bank_account``.



JSON field               Type here            Notes

-----------------------  -------------------  -------------------------------

account_name             String(140) reqd     part of the autoname

account                  account_id           Link Account (the GL account)

bank                     bank_id       reqd   Link Bank

account_type             String(140)          Link Bank Account Type, by label

account_subtype          String(140)          Link Bank Account Subtype, by label

is_default / is_company_account / is_credit_card / disabled   Boolean

company                  *collapsed*          -> business_id

party_type / party       String(140)          Dynamic Link -> label + value pair

iban / bank_account_no / mask / branch_code / integration_id  String(140)

statement_password       *omitted*            credential, see note

last_integration_date    Date



``statement_password`` is dropped. ERPNext's ``Password`` fieldtype is

write-only and masked in the UI; carrying it as a plain column here would put a

bank-statement credential in every SELECT. TODO(security): if statement import

needs it, store it via ``app.utils.encryption`` and never expose it on a schema.



``autoname`` upstream is ``account_name + " - " + bank``.

"""



from __future__ import annotations



import uuid

from datetime import date

from typing import Optional



from sqlalchemy import Boolean, Date, ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel, tenant_index



__all__ = ["BankAccount"]





class BankAccount(TenantModel):

    """A bank account the tenant holds, optionally tied to a GL account."""



    # `acc_bank_accounts`, not `bank_accounts`: the repository already owns a

    # `bank_accounts` table in app/models/bank_data.py -- CreditBridge's

    # borrower bank-analytics table (IFSC, avg monthly balance, bounce count),

    # which is a different concept from ERPNext's Bank Account doctype. Both

    # share one MetaData, so the names must differ or `app.main` cannot import.

    # TODO(accounts-conversion): revisit if the two are ever merged.

    __tablename__ = "acc_bank_accounts"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_acc_bank_accounts_business_id_name"),

        tenant_index("ix_acc_bank_accounts_business_bank", "bank_id"),

        tenant_index("ix_acc_bank_accounts_business_party", "party_type", "party"),

    )



    name: Mapped[str] = mapped_column(String(255), nullable=False)

    account_name: Mapped[str] = mapped_column(String(140), nullable=False)



    bank_id: Mapped[uuid.UUID] = mapped_column(

        ForeignKey("banks.id", ondelete="RESTRICT"), nullable=False, index=True

    )

    bank = relationship("Bank", foreign_keys=[bank_id])



    #: The GL account this bank account posts through. Optional upstream too --

    #: a bank account with no GL account simply cannot be used in entries.

    account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"), nullable=True, index=True

    )

    account = relationship("Account", foreign_keys=[account_id])



    #: Links by label to the two lookup doctypes converted alongside this one.

    account_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    account_subtype: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    is_company_account: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    is_credit_card: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    #: ERPNext's Dynamic Link, flattened to a label + value pair.

    party_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    party: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    iban: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    bank_account_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    mask: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    branch_code: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    integration_id: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    last_integration_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)



    balances: Mapped[list["BankAccountBalance"]] = relationship(  # noqa: F821

        "BankAccountBalance",

        back_populates="parent",

        cascade="all, delete-orphan",

        passive_deletes=True,

        order_by="BankAccountBalance.idx",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<BankAccount id={self.id} name={self.name!r}>"
