"""

GL Entry -- converted from ``erpnext/accounts/doctype/gl_entry``.



The double-entry ledger. Every accounting voucher posts a balanced set of these.

``autoname`` is ``ACC-GLE-.YYYY.-.#####``.



Two things make this model different from the other doctypes here:



**``is_cancelled`` is not ``docstatus``.** Upstream keeps them separate: a

cancelled GL Entry sets ``is_cancelled = 1`` *and* ``docstatus = 2``, and every

balance query filters on ``is_cancelled == 0`` rather than on docstatus. Both

columns are kept, and balance reads filter on ``is_cancelled`` to match.



**Rows are append-only.** Upstream never edits a GL Entry; a correction is a

reversal. So there is no update path here -- only create, cancel and list.



JSON field                        Type here         Notes

--------------------------------  ----------------  --------------------------

posting_date / transaction_date   Date

account                           FK -> accounts

cost_center                       FK -> cost_centers

finance_book                      FK -> finance_books

debit / credit                    Numeric(21,9)     company currency

debit_in_account_currency / ...   Numeric(21,9)     account currency

transaction_* / reporting_*       Numeric/Float     multi-currency columns

party_type / party                String(140)       Dynamic Link flattened

voucher_type / voucher_no         String(140)       Dynamic Link flattened

against_voucher_type / _voucher   String(140)       Dynamic Link flattened

company                           *collapsed*       -> business_id

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

    Float,

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



__all__ = ["GLEntry", "YesNo"]





class YesNo(str, enum.Enum):

    """ERPNext's ``No``/``Yes`` Select, used for ``is_opening`` and ``is_advance``."""



    NO = "No"

    YES = "Yes"





class GLEntry(SubmittableModel, TenantModel):

    """One line of the general ledger."""



    __tablename__ = "gl_entries"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_gl_entries_business_id_name"),

        tenant_index("ix_gl_entries_business_posting_date", "posting_date"),

        tenant_index("ix_gl_entries_business_account", "account_id"),

        tenant_index("ix_gl_entries_business_voucher", "voucher_type", "voucher_no"),

        tenant_index("ix_gl_entries_business_party", "party_type", "party"),

    )



    #: ``ACC-GLE-<year>-<#####>``, scoped per tenant and year.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    posting_date: Mapped[date] = mapped_column(Date, nullable=False)

    transaction_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)



    account_id: Mapped[uuid.UUID] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"), nullable=False, index=True

    )

    account = relationship("Account", foreign_keys=[account_id])



    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"), nullable=True, index=True

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])



    finance_book_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("finance_books.id", ondelete="RESTRICT"), nullable=True, index=True

    )

    finance_book = relationship("FinanceBook", foreign_keys=[finance_book_id])



    party_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    party: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    #: Company currency. Exactly one side is non-zero for a real entry.

    debit: Mapped[Decimal] = mapped_column(

        Numeric(21, 9), nullable=False, default=Decimal("0")

    )

    credit: Mapped[Decimal] = mapped_column(

        Numeric(21, 9), nullable=False, default=Decimal("0")

    )



    account_currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    debit_in_account_currency: Mapped[Optional[Decimal]] = mapped_column(

        Numeric(21, 9), nullable=True

    )

    credit_in_account_currency: Mapped[Optional[Decimal]] = mapped_column(

        Numeric(21, 9), nullable=True

    )



    transaction_currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    transaction_exchange_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    debit_in_transaction_currency: Mapped[Optional[Decimal]] = mapped_column(

        Numeric(21, 9), nullable=True

    )

    credit_in_transaction_currency: Mapped[Optional[Decimal]] = mapped_column(

        Numeric(21, 9), nullable=True

    )



    debit_in_reporting_currency: Mapped[Optional[Decimal]] = mapped_column(

        Numeric(21, 9), nullable=True

    )

    credit_in_reporting_currency: Mapped[Optional[Decimal]] = mapped_column(

        Numeric(21, 9), nullable=True

    )

    reporting_currency_exchange_rate: Mapped[Optional[float]] = mapped_column(

        Float, nullable=True

    )



    #: Comma-joined counter-account names, as upstream stores them.

    against: Mapped[Optional[str]] = mapped_column(Text, nullable=True)



    voucher_type: Mapped[str] = mapped_column(String(140), nullable=False)

    voucher_no: Mapped[str] = mapped_column(String(140), nullable=False)

    voucher_detail_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    voucher_subtype: Mapped[Optional[str]] = mapped_column(Text, nullable=True)



    against_voucher_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    against_voucher: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    remarks: Mapped[Optional[str]] = mapped_column(Text, nullable=True)



    is_opening: Mapped[YesNo] = mapped_column(

        SAEnum(YesNo, native_enum=False, length=3, validate_strings=True),

        nullable=False,

        default=YesNo.NO,

    )

    is_advance: Mapped[YesNo] = mapped_column(

        SAEnum(YesNo, native_enum=False, length=3, validate_strings=True),

        nullable=False,

        default=YesNo.NO,

    )



    fiscal_year: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    to_rename: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    due_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)



    #: The operative cancellation flag for balance queries -- see module docstring.

    is_cancelled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return (

            f"<GLEntry id={self.id} account={self.account_id} "

            f"dr={self.debit} cr={self.credit}>"

        )
