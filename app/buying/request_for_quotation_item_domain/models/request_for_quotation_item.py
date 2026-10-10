"""

Request for Quotation Item -- converted from ``erpnext/buying/doctype/request_for_quotation_item``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Request For Quotation).

"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, ForeignKey, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["RequestForQuotationItem"]







class RequestForQuotationItem(ChildTableModel, TenantModel):

    __tablename__ = "request_for_quotation_items"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_request_for_quotation_items_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("request_for_quotations.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "RequestForQuotation",

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

    supplier_part_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    image: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    image_view: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    qty: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    schedule_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    uom = relationship("app.stock.uom_domain.models.uom.Uom", foreign_keys=[uom_id])

    warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[warehouse_id])

    project_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    material_request_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("material_requests.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    material_request = relationship("app.stock.material_request_domain.models.material_request.MaterialRequest", foreign_keys=[material_request_id])

    material_request_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    brand_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("brands.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    brand = relationship("app.stock.brand_domain.models.brand.Brand", foreign_keys=[brand_id])

    item_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("item_groups.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item_group = relationship("app.stock.item_group_domain.models.item_group.ItemGroup", foreign_keys=[item_group_id])

    page_break: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    stock_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    stock_uom = relationship("app.stock.uom_domain.models.uom.Uom", foreign_keys=[stock_uom_id])

    conversion_factor: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    stock_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("app.accounts.cost_center_domain.models.cost_center.CostCenter", foreign_keys=[cost_center_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<RequestForQuotationItem id={self.id}>"
