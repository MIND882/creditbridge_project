"""

Tax Withholding Entry -- converted from ``erpnext/accounts/doctype/tax_withholding_entry``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, Enum as SAEnum, ForeignKey, Numeric, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.tax_withholding_category_domain.models.tax_withholding_category import TaxWithholdingCategory  # noqa: F401

from app.accounts.tax_withholding_group_domain.models.tax_withholding_group import TaxWithholdingGroup  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["TaxWithholdingEntry", "TaxWithholdingEntryStatus", "TaxWithholdingEntryUnderWithheldReason"]







class TaxWithholdingEntryStatus(str, enum.Enum):

    SETTLED = "Settled"

    UNDER_WITHHELD = "Under Withheld"

    OVER_WITHHELD = "Over Withheld"

    DUPLICATE = "Duplicate"

    CANCELLED = "Cancelled"





class TaxWithholdingEntryUnderWithheldReason(str, enum.Enum):

    THRESHOLD_EXEMPTION = "Threshold Exemption"

    LOWER_DEDUCTION_CERTIFICATE = "Lower Deduction Certificate"









class TaxWithholdingEntry(ChildTableModel, TenantModel):

    __tablename__ = "tax_withholding_entries"

    #: Polymorphic parent -- purchase_invoice, sales_invoice, journal_entry, payment_entry

    #: all use this doctype as a Table, so there is no single

    #: foreign key to point at. ``parenttype`` says which.

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        Uuid, nullable=True, index=True

    )

    parenttype: Mapped[Optional[str]] = mapped_column(

        String(140), nullable=True, index=True

    )



    party_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    party: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    tax_id: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    tax_withholding_category_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("tax_withholding_categories.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    tax_withholding_category = relationship("TaxWithholdingCategory", foreign_keys=[tax_withholding_category_id])

    tax_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    taxable_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    lower_deduction_certificate: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    status: Mapped[Optional[TaxWithholdingEntryStatus]] = mapped_column(

        SAEnum(TaxWithholdingEntryStatus, native_enum=False, length=14, validate_strings=True),

        nullable=True,

    )

    currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    conversion_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    withholding_doctype: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    withholding_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    taxable_doctype: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    taxable_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    taxable_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    withholding_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    under_withheld_reason: Mapped[Optional[TaxWithholdingEntryUnderWithheldReason]] = mapped_column(

        SAEnum(TaxWithholdingEntryUnderWithheldReason, native_enum=False, length=27, validate_strings=True),

        nullable=True,

    )

    withholding_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    tax_withholding_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("tax_withholding_groups.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    tax_withholding_group = relationship("TaxWithholdingGroup", foreign_keys=[tax_withholding_group_id])

    created_by_migration: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<TaxWithholdingEntry id={self.id}>"
