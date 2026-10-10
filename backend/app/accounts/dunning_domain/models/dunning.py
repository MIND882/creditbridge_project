"""

Dunning -- converted from ``erpnext/accounts/doctype/dunning``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Date, Enum as SAEnum, ForeignKey, Numeric, String, Text, Time, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.overdue_payment_domain.models.overdue_payment import OverduePayment



from app.accounts.account_domain.models.account import Account  # noqa: F401

from app.accounts.cost_center_domain.models.cost_center import CostCenter  # noqa: F401

from app.accounts.dunning_type_domain.models.dunning_type import DunningType  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["Dunning", "DunningNamingSeries", "DunningStatus"]







class DunningNamingSeries(str, enum.Enum):

    DUNN_MM_YY = "DUNN-.MM.-.YY.-"





class DunningStatus(str, enum.Enum):

    DRAFT = "Draft"

    RESOLVED = "Resolved"

    UNRESOLVED = "Unresolved"

    CANCELLED = "Cancelled"









class Dunning(SubmittableModel, TenantModel):

    __tablename__ = "dunnings"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_dunnings_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    naming_series: Mapped[Optional[DunningNamingSeries]] = mapped_column(

        SAEnum(DunningNamingSeries, native_enum=False, length=15, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    customer_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    posting_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    dunning_type_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("dunning_types.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    dunning_type = relationship("DunningType", foreign_keys=[dunning_type_id])

    dunning_fee: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    language: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    letter_head: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    amended_from: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    body_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    closing_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    posting_time: Mapped[Optional[dt.time]] = mapped_column(Time, nullable=True)

    rate_of_interest: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    address_display: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    contact_display: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    contact_mobile: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    company_address_display: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    contact_email: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    customer: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    grand_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    status: Mapped[Optional[DunningStatus]] = mapped_column(

        SAEnum(DunningStatus, native_enum=False, length=10, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    income_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    income_account = relationship("Account", foreign_keys=[income_account_id])

    total_interest: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_outstanding: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    customer_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    contact_person: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    dunning_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])

    spacer: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    company_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    conversion_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_dunning_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    overdue_payments = relationship(

        OverduePayment,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=OverduePayment.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<Dunning id={self.id}>"
