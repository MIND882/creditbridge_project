"""

Journal Entry Template -- converted from

``erpnext/accounts/doctype/journal_entry_template``.



A reusable set of accounts for a recurring voucher, so a monthly accrual does

not have to be re-typed. ``autoname`` is ``field:template_title``.



Upstream ``validate()`` runs:



    validate_party()            -> a row may only name a party_type when its

                                   account is Receivable or Payable, and may only

                                   name a party when it also names a party_type

    validate_account_company()  -> every row's account must belong to the

                                   template's company



``company`` collapses into ``business_id`` here (see the Account model note), so

``validate_account_company`` becomes a tenant check: the account is resolved

through the tenant-scoped repository, which fails on a foreign or missing

account. That preserves the intent -- a row cannot reach outside this tenant --

without a company column that no longer exists.



``voucher_type`` reuses ``JournalVoucherType`` from the journal entry model so a

template can only name a voucher type an actual journal entry accepts.

"""



from __future__ import annotations



from typing import Optional



from sqlalchemy import Boolean, String, UniqueConstraint

from sqlalchemy import Enum as SAEnum

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.journal_entry_domain.models.journal_entry import (

    NAMING_SERIES as JV_NAMING_SERIES,

)

from app.accounts.journal_entry_domain.models.journal_entry import JournalVoucherType, YesNo

from app.accounts.journal_entry_template_account_domain.models.journal_entry_template_account import (

    JournalEntryTemplateAccount,

)

from app.core.base_model import TenantModel, tenant_index



__all__ = ["JournalEntryTemplate", "NAMING_SERIES"]



#: Upstream borrows Journal Entry's series options for this field.

NAMING_SERIES = JV_NAMING_SERIES





class JournalEntryTemplate(TenantModel):

    """``autoname = field:template_title``."""



    __tablename__ = "journal_entry_templates"

    __table_args__ = (

        UniqueConstraint(

            "business_id", "name", name="uq_journal_entry_templates_business_name"

        ),

        tenant_index("ix_journal_entry_templates_business_voucher_type", "voucher_type"),

    )



    name: Mapped[str] = mapped_column(String(140), nullable=False)

    template_title: Mapped[str] = mapped_column(String(140), nullable=False)



    voucher_type: Mapped[JournalVoucherType] = mapped_column(

        SAEnum(JournalVoucherType, native_enum=False, length=40, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=False,

        default=JournalVoucherType.JOURNAL_ENTRY,

    )



    naming_series: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    is_opening: Mapped[YesNo] = mapped_column(

        SAEnum(YesNo, native_enum=False, length=3, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=False,

        default=YesNo.NO,

    )



    multi_currency: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    accounts = relationship(

        JournalEntryTemplateAccount,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=JournalEntryTemplateAccount.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:

        return f"<JournalEntryTemplate id={self.id} name={self.name!r}>"
