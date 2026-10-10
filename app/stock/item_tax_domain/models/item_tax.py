"""

Item Tax -- converted from ``erpnext/stock/doctype/item_tax``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Item).

"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Date, ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["ItemTax"]







class ItemTax(ChildTableModel, TenantModel):

    __tablename__ = "item_taxs"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_item_taxs_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "Item",

        back_populates="taxes",

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



    item_tax_template_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("item_tax_templates.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    item_tax_template = relationship("ItemTaxTemplate", foreign_keys=[item_tax_template_id])

    tax_category_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("tax_categories.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    tax_category = relationship("TaxCategory", foreign_keys=[tax_category_id])

    valid_from: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    maximum_net_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    minimum_net_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ItemTax id={self.id}>"
