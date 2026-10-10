"""

Opening Invoice Creation Tool -- converted from ``erpnext/accounts/doctype/opening_invoice_creation_tool``.





"""



from __future__ import annotations



import enum

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.opening_invoice_creation_tool_item_domain.models.opening_invoice_creation_tool_item import OpeningInvoiceCreationToolItem



from app.accounts.cost_center_domain.models.cost_center import CostCenter  # noqa: F401



from app.core.base_model import TenantModel



__all__ = ["OpeningInvoiceCreationTool", "OpeningInvoiceCreationToolInvoiceType"]







class OpeningInvoiceCreationToolInvoiceType(str, enum.Enum):

    SALES = "Sales"

    PURCHASE = "Purchase"









class OpeningInvoiceCreationTool(TenantModel):

    __tablename__ = "opening_invoice_creation_tools"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_opening_invoice_creation_tools_business_name"),

    )



    #: Upstream declares no ``autoname``; Frappe mints a hash.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    create_missing_party: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    invoice_type: Mapped[OpeningInvoiceCreationToolInvoiceType] = mapped_column(

        SAEnum(OpeningInvoiceCreationToolInvoiceType, native_enum=False, length=8, validate_strings=True),

        nullable=False,

    )

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    invoices = relationship(

        OpeningInvoiceCreationToolItem,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=OpeningInvoiceCreationToolItem.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<OpeningInvoiceCreationTool id={self.id}>"
