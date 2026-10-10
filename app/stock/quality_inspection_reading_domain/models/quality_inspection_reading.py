"""

Quality Inspection Reading -- converted from ``erpnext/stock/doctype/quality_inspection_reading``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Quality Inspection).

"""



from __future__ import annotations



import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, ForeignKey, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["QualityInspectionReading", "QualityInspectionReadingStatus"]





class QualityInspectionReadingStatus(str, enum.Enum):

    ACCEPTED = "Accepted"

    REJECTED = "Rejected"





class QualityInspectionReading(ChildTableModel, TenantModel):

    __tablename__ = "quality_inspection_readings"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_quality_inspection_readings_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("quality_inspections.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "QualityInspection",

        back_populates="readings",

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

    reading_1: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    reading_2: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    reading_3: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    reading_4: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    reading_5: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    reading_6: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    reading_7: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    reading_8: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    reading_9: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    reading_10: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    status: Mapped[Optional[str]] = mapped_column(SAEnum(QualityInspectionReadingStatus, native_enum=False, length=12, validate_strings=True), nullable=True)

    acceptance_formula: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    formula_based_criteria: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    min_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    max_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    reading_value: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    manual_inspection: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    numeric: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    parameter_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("quality_inspection_parameter_groups.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    parameter_group = relationship("QualityInspectionParameterGroup", foreign_keys=[parameter_group_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<QualityInspectionReading id={self.id}>"
