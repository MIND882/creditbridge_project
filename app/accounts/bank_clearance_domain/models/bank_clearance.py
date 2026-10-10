"""

Bank Clearance -- converted from ``erpnext/accounts/doctype/bank_clearance``.



A *tool*, not a ledger document: it lists unreconciled payment entries against a

bank account for a date range and lets the user stamp clearance dates on them.

It is not submittable and has no ``autoname`` upstream, so ``name`` here is a

generated label.



JSON field                  Type here         Notes

--------------------------  ----------------  ----------------------------

account                     FK -> accounts reqd

account_currency            String(140)

from_date / to_date         Date      reqd

bank_account                FK -> acc_bank_accounts

include_reconciled_entries  Boolean   def False

include_pos_transactions    Boolean   def False

payment_entries             Table -> BankClearanceDetail

"""



from __future__ import annotations



import uuid

from datetime import date

from typing import Optional



from sqlalchemy import Boolean, Date, ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel, tenant_index



__all__ = ["BankClearance"]





class BankClearance(TenantModel):

    """One run of the bank-clearance tool over a date range."""



    __tablename__ = "bank_clearances"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_bank_clearances_business_id_name"),

        tenant_index("ix_bank_clearances_business_dates", "from_date", "to_date"),

    )



    #: Not derived from a field upstream; a readable label for the run.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    account_id: Mapped[uuid.UUID] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"), nullable=False, index=True

    )

    account = relationship("Account", foreign_keys=[account_id])



    account_currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    from_date: Mapped[date] = mapped_column(Date, nullable=False)

    to_date: Mapped[date] = mapped_column(Date, nullable=False)



    bank_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("acc_bank_accounts.id", ondelete="RESTRICT"), nullable=True, index=True

    )

    bank_account = relationship("app.accounts.bank_account_domain.models.bank_account.BankAccount", foreign_keys=[bank_account_id])



    include_reconciled_entries: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    include_pos_transactions: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    payment_entries: Mapped[list["BankClearanceDetail"]] = relationship(  # noqa: F821

        "BankClearanceDetail",

        back_populates="parent",

        cascade="all, delete-orphan",

        passive_deletes=True,

        order_by="BankClearanceDetail.idx",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<BankClearance id={self.id} name={self.name!r}>"
