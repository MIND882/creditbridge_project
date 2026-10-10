"""

Item Quality Inspection Parameter -- converted from ``erpnext/stock/doctype/item_quality_inspection_parameter``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Quality Inspection Template).

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, ForeignKey, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["ItemQualityInspectionParameter"]







class ItemQualityInspectionParameter(ChildTableModel, TenantModel):

    __tablename__ = "item_quality_inspection_parameters"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_item_quality_inspection_parameters_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("quality_inspection_templates.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "QualityInspectionTemplate",

        back_populates="item_quality_inspection_parameter",

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



    specification_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("quality_inspection_parameters.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    specification = relationship("QualityInspectionParameter", foreign_keys=[specification_id])

    value: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    acceptance_formula: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    formula_based_criteria: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    min_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    max_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    numeric: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    parameter_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("quality_inspection_parameter_groups.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    parameter_group = relationship("QualityInspectionParameterGroup", foreign_keys=[parameter_group_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ItemQualityInspectionParameter id={self.id}>"
