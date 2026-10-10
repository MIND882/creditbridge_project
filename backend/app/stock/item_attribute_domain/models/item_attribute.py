"""

Item Attribute -- converted from ``erpnext/stock/doctype/item_attribute``.

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.stock.item_attribute_value_domain.models.item_attribute_value import ItemAttributeValue



from app.core.base_model import TenantModel



__all__ = ["ItemAttribute"]







class ItemAttribute(TenantModel):

    __tablename__ = "item_attributes"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_item_attributes_business_name"),

    )



    #: ``autoname`` = 'field:attribute_name' -- derived in the service at create time.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    attribute_name: Mapped[str] = mapped_column(String(140), nullable=False)

    numeric_values: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    from_range: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0)

    increment: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0)

    to_range: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0)

    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    item_attribute_values: Mapped[list["ItemAttributeValue"]] = relationship(  # noqa: F821

        "ItemAttributeValue",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[ItemAttributeValue.parent_id]",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ItemAttribute id={self.id}>"
