"""

Bank Guarantee -- converted from ``erpnext/accounts/doctype/bank_guarantee``.



Submittable (``is_submittable: 1``), so it carries ``docstatus`` plus the

submit / cancel / amend lifecycle. ``autoname`` is ``ACC-BG-.YYYY.-.#####``.



JSON field               Type here            Notes

-----------------------  -------------------  ---------------------------

bg_type                  Enum                 Receiving / Providing, reqd

amount                   Numeric(21,9) reqd

start_date               Date        reqd

validity                 Integer              days

end_date                 Date

customer / supplier / project   String(140)   Links kept as labels

reference_doctype / reference_docname  String(140)  Dynamic Link flattened

bank / bank_account / account   FK            real FKs, not labels

margin_money / charges   Numeric(21,9)

amended_from             self-FK



``more_information`` is ERPNext ``Text Editor`` (HTML). Stored as Text and

returned raw; sanitisation is a presentation concern and is not done here.

"""



from __future__ import annotations



import enum

import uuid

from datetime import date

from decimal import Decimal

from typing import Optional



from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint

from sqlalchemy import Enum as SAEnum

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel, tenant_index

from app.core.docstatus import SubmittableModel



__all__ = ["BankGuarantee", "BGType"]





class BGType(str, enum.Enum):

    """``bg_type`` Select: whether we receive the guarantee or provide it."""



    RECEIVING = "Receiving"

    PROVIDING = "Providing"





class BankGuarantee(SubmittableModel, TenantModel):

    """A bank guarantee received from a customer or provided to a supplier."""



    __tablename__ = "bank_guarantees"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_bank_guarantees_business_id_name"),

        tenant_index("ix_bank_guarantees_business_dates", "start_date", "end_date"),

    )



    #: ``ACC-BG-<year>-<#####>``, scoped per tenant.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    bg_type: Mapped[BGType] = mapped_column(

        SAEnum(BGType, native_enum=False, length=10, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=False

    )



    amount: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False)

    start_date: Mapped[date] = mapped_column(Date, nullable=False)

    validity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)



    #: Counterparty links, kept as labels (Customer/Supplier/Project are not

    #: converted yet).

    customer: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    supplier: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    #: ERPNext Dynamic Link flattened to a label + value pair.

    reference_doctype: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    reference_docname: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    bank_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("banks.id", ondelete="RESTRICT"), nullable=True, index=True

    )

    bank = relationship("Bank", foreign_keys=[bank_id])



    bank_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("acc_bank_accounts.id", ondelete="RESTRICT"), nullable=True, index=True

    )

    bank_account = relationship("app.accounts.bank_account_domain.models.bank_account.BankAccount", foreign_keys=[bank_account_id])



    account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"), nullable=True, index=True

    )

    account = relationship("Account", foreign_keys=[account_id])



    bank_account_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    iban: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    branch_code: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    swift_number: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    bank_guarantee_number: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    name_of_beneficiary: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    fixed_deposit_number: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    margin_money: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    charges: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    more_information: Mapped[Optional[str]] = mapped_column(Text, nullable=True)



    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("bank_guarantees.id", ondelete="SET NULL"), nullable=True

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<BankGuarantee id={self.id} name={self.name!r}>"
