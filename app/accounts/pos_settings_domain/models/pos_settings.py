"""

POS Settings -- converted from ``erpnext/accounts/doctype/pos_settings``.





"""



from __future__ import annotations



import enum

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.pos_field_domain.models.pos_field import POSField

from app.accounts.pos_search_fields_domain.models.pos_search_fields import POSSearchFields



from app.core.base_model import TenantModel



__all__ = ["POSSettings", "POSSettingsInvoiceType"]







class POSSettingsInvoiceType(str, enum.Enum):

    SALES_INVOICE = "Sales Invoice"

    POS_INVOICE = "POS Invoice"









class POSSettings(TenantModel):

    __tablename__ = "pos_settings"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_pos_settings_business_name"),

    )



    #: Upstream declares no ``autoname``; Frappe mints a hash.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    invoice_type: Mapped[Optional[POSSettingsInvoiceType]] = mapped_column(

        SAEnum(POSSettingsInvoiceType, native_enum=False, length=13, validate_strings=True),

        nullable=True,

    )

    post_change_gl_entries: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)



    invoice_fields = relationship(

        POSField,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=POSField.idx,

        passive_deletes=True,

    )

    pos_search_fields = relationship(

        POSSearchFields,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=POSSearchFields.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<POSSettings id={self.id}>"
