"""

Landed Cost Purchase Receipt -- converted from ``erpnext/stock/doctype/landed_cost_purchase_receipt``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Landed Cost Voucher).

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Date, Enum as SAEnum, ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["LandedCostPurchaseReceipt", "LandedCostPurchaseReceiptReceiptDocumentType"]





class LandedCostPurchaseReceiptReceiptDocumentType(str, enum.Enum):

    PURCHASE_INVOICE = "Purchase Invoice"

    PURCHASE_RECEIPT = "Purchase Receipt"

    STOCK_ENTRY = "Stock Entry"

    SUBCONTRACTING_RECEIPT = "Subcontracting Receipt"





class LandedCostPurchaseReceipt(ChildTableModel, TenantModel):

    __tablename__ = "landed_cost_purchase_receipts"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_landed_cost_purchase_receipts_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("landed_cost_vouchers.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "LandedCostVoucher",

        back_populates="purchase_receipts",

        # explicit: a child can carry a second FK to its own parent

        # (item_variant_attribute.variant_of -> items), which would

        # otherwise make the join ambiguous

        foreign_keys=[parent_id],

    )



    #: ``autoname`` = 'hash'.

    #: Upstream ``autoname = 'hash'``: Frappe assigns an opaque random hash.

    #: There is no content to hash here, so a UUID4 is the faithful

    #: equivalent -- unique, opaque, and not user-visible. Without a

    #: default the column is NOT NULL and every insert fails.

    name: Mapped[str] = mapped_column(

        String(140), nullable=False, default=lambda: uuid.uuid4().hex

    )



    receipt_document_type: Mapped[str] = mapped_column(SAEnum(LandedCostPurchaseReceiptReceiptDocumentType, native_enum=False, length=26, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=False)

    receipt_document: Mapped[str] = mapped_column(String(140), nullable=False)

    supplier: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    posting_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    grand_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<LandedCostPurchaseReceipt id={self.id}>"
