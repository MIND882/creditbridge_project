"""

Journal Entry -- converted from ``erpnext/accounts/doctype/journal_entry``.



Submittable, ``autoname`` is ``naming_series`` (``ACC-JV-.YYYY.-#####``). Posting

writes a balanced set of GL Entries and cancellation reverses them.



JSON field              Type here          Notes

----------------------  -----------------  --------------------------------

voucher_type            Enum reqd          Journal Entry / Bank Entry / ...

posting_date            Date      reqd

accounts                Table     reqd     -> JournalEntryAccount

cheque_no / cheque_date String/Date        required for Bank Entry

is_opening              Enum               forced to Yes for Opening Entry

multi_currency          Boolean

write_off_based_on      Enum

company                 *collapsed*        -> business_id

total_debit / total_credit / difference    derived, read-only



Not ported (upstream features that depend on unconverted doctypes):

inter-company entries, invoice discounting, asset depreciation rows, tax

withholding, stock accounts and periodic-entry difference rows. Each is noted at

the point where the call would have been.

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
from app.accounts.journal_entry_account_domain.models.journal_entry_account import JournalEntryAccount



__all__ = [

    "JournalEntry",

    "JournalVoucherType",

    "WriteOffBasedOn",

    "YesNo",

    "NAMING_SERIES",

]



NAMING_SERIES = "ACC-JV-.YYYY.-"





class JournalVoucherType(str, enum.Enum):

    """

    The subset of upstream's ``voucher_type`` Select that this conversion

    enforces. The full upstream list includes Opening Entry, Credit Note, Debit

    Note, Bank Entry, Cash Entry, Exchange Gain Or Loss, Depreciation Entry and

    Inter Company Journal Entry; the ones needing unconverted doctypes are kept

    as values but their special handling is not ported.

    """



    JOURNAL_ENTRY = "Journal Entry"

    OPENING_ENTRY = "Opening Entry"

    BANK_ENTRY = "Bank Entry"

    CASH_ENTRY = "Cash Entry"

    CREDIT_NOTE = "Credit Note"

    DEBIT_NOTE = "Debit Note"

    EXCHANGE_GAIN_OR_LOSS = "Exchange Gain Or Loss"

    DEPRECIATION_ENTRY = "Depreciation Entry"





class WriteOffBasedOn(str, enum.Enum):

    ACCOUNTS_RECEIVABLE = "Accounts Receivable"

    ACCOUNTS_PAYABLE = "Accounts Payable"





class YesNo(str, enum.Enum):

    NO = "No"

    YES = "Yes"





class JournalEntry(SubmittableModel, TenantModel):

    """A manual double-entry voucher."""



    __tablename__ = "journal_entries"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_journal_entries_business_id_name"),

        tenant_index("ix_journal_entries_business_posting_date", "posting_date"),

        tenant_index("ix_journal_entries_business_voucher_type", "voucher_type"),

    )



    #: ``ACC-JV-<year>-<#####>``, scoped per tenant and year.

    name: Mapped[str] = mapped_column(String(140), nullable=False)

    naming_series: Mapped[str] = mapped_column(

        String(140), nullable=False, default=NAMING_SERIES

    )

    title: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    voucher_type: Mapped[JournalVoucherType] = mapped_column(
        SAEnum(
            JournalVoucherType,
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
            length=40,
            validate_strings=True,
        ),
        nullable=False,
        default=JournalVoucherType.JOURNAL_ENTRY,
    )

    posting_date: Mapped[date] = mapped_column(Date, nullable=False)

    cheque_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)
    cheque_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    user_remark: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    remark: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    bill_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)
    bill_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    due_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    multi_currency: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    pay_to_recd_from: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)
    mode_of_payment: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_opening: Mapped[YesNo] = mapped_column(
        SAEnum(
            YesNo,
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
            length=10,
            validate_strings=True,
        ),
        nullable=False,
        default=YesNo.NO,
    )

    write_off_based_on: Mapped[WriteOffBasedOn] = mapped_column(
        SAEnum(
            WriteOffBasedOn,
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
            length=30,
            validate_strings=True,
        ),
        nullable=False,
        default=WriteOffBasedOn.ACCOUNTS_RECEIVABLE,
    )

    write_off_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    #: Upstream's ``party_not_required`` lets Payroll Entry skip the party rule.

    party_not_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    custom_remark: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    apply_tds: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    #: Derived by ``set_total_debit_credit``; never taken from input.

    total_debit: Mapped[Decimal] = mapped_column(

        Numeric(21, 9), nullable=False, default=Decimal("0")

    )

    total_credit: Mapped[Decimal] = mapped_column(

        Numeric(21, 9), nullable=False, default=Decimal("0")

    )

    difference: Mapped[Decimal] = mapped_column(

        Numeric(21, 9), nullable=False, default=Decimal("0")

    )



    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("journal_entries.id", ondelete="SET NULL"), nullable=True

    )



    accounts: Mapped[list["JournalEntryAccount"]] = relationship(  # noqa: F821

        "JournalEntryAccount",

        back_populates="parent",

        cascade="all, delete-orphan",

        passive_deletes=True,

        order_by="JournalEntryAccount.idx",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<JournalEntry id={self.id} name={self.name!r}>"
