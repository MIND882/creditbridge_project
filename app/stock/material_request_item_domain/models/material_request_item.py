"""

Material Request Item -- converted from ``erpnext/stock/doctype/material_request_item``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Material Request).

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



__all__ = ["MaterialRequestItem"]







class MaterialRequestItem(ChildTableModel, TenantModel):

    __tablename__ = "material_request_items"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_material_request_items_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("material_requests.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "MaterialRequest",

        back_populates="items",

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



    item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    item_code = relationship("Item", foreign_keys=[item_code_id])

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    image: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    qty: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    uom = relationship("Uom", foreign_keys=[uom_id])

    conversion_factor: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    stock_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    stock_uom = relationship("Uom", foreign_keys=[stock_uom_id])

    warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    warehouse = relationship("Warehouse", foreign_keys=[warehouse_id])

    schedule_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    stock_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    item_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("item_groups.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item_group = relationship("ItemGroup", foreign_keys=[item_group_id])

    brand_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("brands.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    brand = relationship("Brand", foreign_keys=[brand_id])

    lead_time_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    sales_order: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    sales_order_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    production_plan: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    material_request_plan_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    min_order_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    projected_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    actual_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    ordered_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    expense_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    expense_account = relationship("Account", foreign_keys=[expense_account_id])

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])

    page_break: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    received_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    manufacturer_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("manufacturers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    manufacturer = relationship("Manufacturer", foreign_keys=[manufacturer_id])

    manufacturer_part_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    from_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    from_warehouse = relationship("Warehouse", foreign_keys=[from_warehouse_id])

    bom_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    job_card_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    wip_composite_asset: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    price_list_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    reorder_level: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    reorder_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    projected_on_hand: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    picked_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    packed_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<MaterialRequestItem id={self.id}>"
