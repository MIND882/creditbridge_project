"""

Item Variant Settings -- converted from ``erpnext/stock/doctype/item_variant_settings``.



A Frappe Single (``issingle: 1``): one row per ``business_id``, enforced by a unique constraint on ``business_id`` alone.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import Boolean, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.stock.variant_field_domain.models.variant_field import VariantField



from app.core.base_model import TenantModel



__all__ = ["ItemVariantSettings"]







class ItemVariantSettings(TenantModel):

    __tablename__ = "item_variant_settingss"

    __table_args__ = (

        UniqueConstraint("business_id", name="uq_item_variant_settingss_business"),

    )



    do_not_update_variants: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    allow_rename_attribute_value: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    allow_different_uom: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    fields: Mapped[list["VariantField"]] = relationship(  # noqa: F821

        "VariantField",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[VariantField.parent_id]",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ItemVariantSettings id={self.id}>"
