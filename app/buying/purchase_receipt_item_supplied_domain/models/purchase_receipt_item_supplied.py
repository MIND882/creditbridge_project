"""

Purchase Receipt Item Supplied -- converted from ``erpnext/buying/doctype/purchase_receipt_item_supplied``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Purchase Receipt).

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import ForeignKey, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.stock.purchase_receipt_domain.models.purchase_receipt import PurchaseReceipt



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["PurchaseReceiptItemSupplied"]







class PurchaseReceiptItemSupplied(ChildTableModel, TenantModel):

    __tablename__ = "purchase_receipt_item_supplieds"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_purchase_receipt_item_supplieds_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("purchase_receipts.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(

        PurchaseReceipt,

        foreign_keys=[parent_id],

    )

    parenttype: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    parentfield: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    #: ``autoname`` = 'hash'.

    #: Upstream ``autoname = 'hash'``: Frappe assigns an opaque random hash.

    #: There is no content to hash here, so a UUID4 is the faithful

    #: equivalent -- unique, opaque, and not user-visible. Without a

    #: default the column is NOT NULL and every insert fails.

    name: Mapped[str] = mapped_column(

        String(140), nullable=False, default=lambda: uuid.uuid4().hex

    )



    main_item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    main_item_code = relationship("app.stock.item_domain.models.item.Item", foreign_keys=[main_item_code_id])

    rm_item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    rm_item_code = relationship("app.stock.item_domain.models.item.Item", foreign_keys=[rm_item_code_id])

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    batch_no_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("batchs.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    batch_no = relationship("app.stock.batch_domain.models.batch.Batch", foreign_keys=[batch_no_id])

    serial_no: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    required_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    consumed_qty: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    stock_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    stock_uom = relationship("app.stock.uom_domain.models.uom.Uom", foreign_keys=[stock_uom_id])

    rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    conversion_factor: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    current_stock: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    reference_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    bom_detail_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    purchase_order_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("purchase_orders.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    purchase_order = relationship("app.buying.purchase_order_domain.models.purchase_order.PurchaseOrder", foreign_keys=[purchase_order_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PurchaseReceiptItemSupplied id={self.id}>"
