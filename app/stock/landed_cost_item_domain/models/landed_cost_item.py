"""

Landed Cost Item -- converted from ``erpnext/stock/doctype/landed_cost_item``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Landed Cost Voucher).

"""



from __future__ import annotations



import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, ForeignKey, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["LandedCostItem", "LandedCostItemReceiptDocumentType"]





class LandedCostItemReceiptDocumentType(str, enum.Enum):

    PURCHASE_INVOICE = "Purchase Invoice"

    PURCHASE_RECEIPT = "Purchase Receipt"

    STOCK_ENTRY = "Stock Entry"

    SUBCONTRACTING_RECEIPT = "Subcontracting Receipt"





class LandedCostItem(ChildTableModel, TenantModel):

    __tablename__ = "landed_cost_items"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_landed_cost_items_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("landed_cost_vouchers.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "LandedCostVoucher",

        back_populates="items",

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



    item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    item_code = relationship("Item", foreign_keys=[item_code_id])

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    receipt_document_type: Mapped[Optional[str]] = mapped_column(SAEnum(LandedCostItemReceiptDocumentType, native_enum=False, length=26, validate_strings=True), nullable=True)

    receipt_document: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    amount: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    applicable_charges: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    purchase_receipt_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])

    is_fixed_asset: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    stock_entry_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<LandedCostItem id={self.id}>"
