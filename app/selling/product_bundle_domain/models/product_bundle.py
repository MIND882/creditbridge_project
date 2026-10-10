"""

Product Bundle -- converted from ``erpnext/selling/doctype/product_bundle``.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.selling.product_bundle_item_domain.models.product_bundle_item import ProductBundleItem



from app.core.base_model import TenantModel



__all__ = ["ProductBundle"]







class ProductBundle(TenantModel):

    __tablename__ = "product_bundles"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_product_bundles_business_name"),

    )



    #: Upstream declares no ``autoname``; Frappe mints a hash.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    new_item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    new_item_code = relationship("app.stock.item_domain.models.item.Item", foreign_keys=[new_item_code_id])

    description: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("product_bundles.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("app.selling.product_bundle_domain.models.product_bundle.ProductBundle", foreign_keys=[amended_from_id])



    items: Mapped[list["ProductBundleItem"]] = relationship(  # noqa: F821

        "app.selling.product_bundle_item_domain.models.product_bundle_item.ProductBundleItem",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys=[ProductBundleItem.parent_id],

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ProductBundle id={self.id}>"
