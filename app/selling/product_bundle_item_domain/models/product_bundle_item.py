"""

Product Bundle Item -- converted from ``erpnext/selling/doctype/product_bundle_item``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Product Bundle).

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import ForeignKey, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["ProductBundleItem"]







class ProductBundleItem(ChildTableModel, TenantModel):

    __tablename__ = "product_bundle_items"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_product_bundle_items_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("product_bundles.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "app.selling.product_bundle_domain.models.product_bundle.ProductBundle",

        back_populates="items",

        # explicit: a child can carry a second FK to its own parent

        # (item_variant_attribute.variant_of -> items), which would

        # otherwise make the join ambiguous

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



    item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    item_code = relationship("app.stock.item_domain.models.item.Item", foreign_keys=[item_code_id])

    qty: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    uom = relationship("app.stock.uom_domain.models.uom.Uom", foreign_keys=[uom_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ProductBundleItem id={self.id}>"
