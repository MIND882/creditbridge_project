"""

Item Variant Attribute -- converted from ``erpnext/stock/doctype/item_variant_attribute``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Item).

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["ItemVariantAttribute"]







class ItemVariantAttribute(ChildTableModel, TenantModel):

    __tablename__ = "item_variant_attributes"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_item_variant_attributes_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "Item",

        back_populates="attributes",

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



    variant_of_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    variant_of = relationship("Item", foreign_keys=[variant_of_id])

    attribute_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("item_attributes.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    attribute = relationship("ItemAttribute", foreign_keys=[attribute_id])

    attribute_value: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    numeric_values: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    from_range: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    increment: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    to_range: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ItemVariantAttribute id={self.id}>"
