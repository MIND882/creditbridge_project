"""

Payment Ledger Entry -- converted from

``erpnext/accounts/doctype/payment_ledger_entry``.



A party's running balance. Where GL Entry answers "what happened to this

account", a Payment Ledger Entry answers "what does this party still owe on this

invoice". One row per receivable/payable movement, written by Payment Entry,

Sales Invoice and the like when they post.



Submittable, but unlike the other vouchers here it has no ``autoname`` upstream

-- ERPNext lets Frappe mint a hash. This port gives it a readable sequence

instead so the rows are addressable in an API: ``ACC-PLE-.#####``.



JSON field                     Type here         Notes

-----------------------------  ----------------  --------------------------

posting_date                   Date

account_type                   Select            Receivable | Payable

account                        FK -> accounts

party_type / party             String(140)       Dynamic Link flattened

voucher_type / voucher_no      String(140)       Dynamic Link flattened

against_voucher_type / _no     String(140)       Dynamic Link flattened

amount                         Numeric(21,9)     +ve owed, -ve paid

account_currency               String(140)

amount_in_account_currency     Numeric(21,9)

delinked                       Boolean           excluded from outstanding

due_date                       Date

cost_center                    FK -> cost_centers

finance_book                   FK -> finance_books

project                        String(140)

voucher_detail_no              String(140)

remarks                        Text

company                        *collapsed*       -> business_id

"""



from __future__ import annotations



import enum

import uuid

from datetime import date

from decimal import Decimal

from typing import Optional



from sqlalchemy import Boolean, Date, ForeignKey, Numeric, String, Text, UniqueConstraint

from sqlalchemy import Enum as SAEnum

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel, tenant_index

from app.core.docstatus import SubmittableModel



__all__ = ["PaymentLedgerEntry", "PLEAccountType"]





class PLEAccountType(str, enum.Enum):

    """The ``account_type`` Select. Only these two kinds of account are tracked."""



    RECEIVABLE = "Receivable"

    PAYABLE = "Payable"





class PaymentLedgerEntry(SubmittableModel, TenantModel):

    __tablename__ = "payment_ledger_entries"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_payment_ledger_entry_business_name"),

        # Upstream's on_doctype_update() indexes both lookup directions.

        tenant_index("against_voucher_no", "against_voucher_type"),

        tenant_index("voucher_no", "voucher_type"),

        tenant_index("posting_date"),

        tenant_index("party_type", "party"),

    )



    name: Mapped[str] = mapped_column(String(255), nullable=False)



    posting_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)



    account_type: Mapped[Optional[PLEAccountType]] = mapped_column(

        SAEnum(PLEAccountType, name="ple_account_type"), nullable=True

    )



    #: The receivable/payable account holding the party's balance.

    account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"), nullable=True

    )



    # Dynamic Links flattened to plain strings.

    party_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    party: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    voucher_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    voucher_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    #: The invoice this row settles against.

    against_voucher_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    against_voucher_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    #: Company currency. Positive means the party owes it.

    amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    account_currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    amount_in_account_currency: Mapped[Optional[Decimal]] = mapped_column(

        Numeric(21, 9), nullable=True

    )



    #: Set when the row has been written off or is otherwise out of the running

    #: balance. Upstream skips most validation for a delinked row.

    delinked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"), nullable=True

    )

    finance_book_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("finance_books.id", ondelete="RESTRICT"), nullable=True

    )



    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    due_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    voucher_detail_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    remarks: Mapped[Optional[str]] = mapped_column(Text, nullable=True)



    def __repr__(self) -> str:

        return (

            f"<PaymentLedgerEntry id={self.id} name={self.name!r} "

            f"account={self.account_id} amount={self.amount}>"

        )
