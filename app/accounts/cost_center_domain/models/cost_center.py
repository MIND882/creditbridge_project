"""

Cost Center -- converted from ``erpnext/accounts/doctype/cost_center``.



JSON field            Type here                Notes

--------------------  -----------------------  -----------------------------

cost_center_name      String(140) NOT NULL     reqd=1

cost_center_number    String(140)

parent_cost_center    parent_cost_center_id    self-FK, nullable = root

company               *collapsed*              -> business_id (see Account model)

is_group              Boolean

lft / rgt / old_parent *omitted*               adjacency list replaces NestedSet

disabled              Boolean



ERPNext identifies the root cost centre by ``cost_center_name == company``,

because the root is created with the company's name. There is no Company

doctype here, so "root" is simply ``parent_cost_center_id IS NULL`` -- the same

distinction ``validate_mandatory`` is actually drawing.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel, tenant_index



__all__ = ["CostCenter"]





class CostCenter(TenantModel):

    """One node of a tenant's cost-centre tree."""



    __tablename__ = "cost_centers"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_cost_centers_business_id_name"),

        tenant_index("ix_cost_centers_business_parent", "parent_cost_center_id"),

        tenant_index("ix_cost_centers_business_is_group", "is_group"),

    )



    #: The ERPNext document name, from ``get_autoname_with_number``.

    name: Mapped[str] = mapped_column(String(255), nullable=False)



    cost_center_name: Mapped[str] = mapped_column(String(140), nullable=False)

    cost_center_number: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    parent_cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"), nullable=True, index=True

    )

    parent_cost_center: Mapped[Optional["CostCenter"]] = relationship(

        "CostCenter",

        remote_side="CostCenter.id",

        back_populates="children",

        foreign_keys=[parent_cost_center_id],

    )

    children: Mapped[list["CostCenter"]] = relationship(

        "CostCenter",

        back_populates="parent_cost_center",

        foreign_keys=[parent_cost_center_id],

        passive_deletes=True,

    )



    is_group: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<CostCenter id={self.id} name={self.name!r} is_group={self.is_group}>"
