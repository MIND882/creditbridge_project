"""

Landed Cost Vendor Invoice -- converted from ``erpnext/stock/doctype/landed_cost_vendor_invoice``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Landed Cost Voucher).

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["LandedCostVendorInvoice"]







class LandedCostVendorInvoice(ChildTableModel, TenantModel):

    __tablename__ = "landed_cost_vendor_invoices"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_landed_cost_vendor_invoices_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("landed_cost_vouchers.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "LandedCostVoucher",

        back_populates="vendor_invoices",

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



    vendor_invoice_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("purchase_invoices.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    vendor_invoice = relationship("PurchaseInvoice", foreign_keys=[vendor_invoice_id])

    amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<LandedCostVendorInvoice id={self.id}>"
