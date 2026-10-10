"""

Item Barcode -- converted from ``erpnext/stock/doctype/item_barcode``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Item).

"""



from __future__ import annotations



import enum

from typing import Optional

import uuid



from sqlalchemy import Enum as SAEnum, ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["ItemBarcode", "ItemBarcodeBarcodeType"]





class ItemBarcodeBarcodeType(str, enum.Enum):

    EAN = "EAN"

    UPC_A = "UPC-A"

    CODE_39 = "CODE-39"

    EAN_13 = "EAN-13"

    EAN_8 = "EAN-8"

    GS1 = "GS1"

    GTIN = "GTIN"

    GTIN_14 = "GTIN-14"

    ISBN = "ISBN"

    ISBN_10 = "ISBN-10"

    ISBN_13 = "ISBN-13"

    ISSN = "ISSN"

    JAN = "JAN"

    PZN = "PZN"

    UPC = "UPC"





class ItemBarcode(ChildTableModel, TenantModel):

    __tablename__ = "item_barcodes"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_item_barcodes_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "Item",

        back_populates="barcodes",

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



    barcode: Mapped[str] = mapped_column(String(140), nullable=False)

    barcode_type: Mapped[Optional[str]] = mapped_column(SAEnum(ItemBarcodeBarcodeType, native_enum=False, length=11, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    uom = relationship("Uom", foreign_keys=[uom_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ItemBarcode id={self.id}>"
