"""

Supplier Scorecard Scoring Standing -- converted from ``erpnext/buying/doctype/supplier_scorecard_scoring_standing``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Supplier Scorecard).

"""



from __future__ import annotations



import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["SupplierScorecardScoringStanding", "SupplierScorecardScoringStandingStandingColor"]





class SupplierScorecardScoringStandingStandingColor(str, enum.Enum):

    BLUE = "Blue"

    PURPLE = "Purple"

    GREEN = "Green"

    YELLOW = "Yellow"

    ORANGE = "Orange"

    RED = "Red"





class SupplierScorecardScoringStanding(ChildTableModel, TenantModel):

    __tablename__ = "supplier_scorecard_scoring_standings"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_supplier_scorecard_scoring_standings_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("supplier_scorecards.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "SupplierScorecard",

        back_populates="standings",

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



    standing_name_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("supplier_scorecard_standings.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    standing_name = relationship("app.buying.supplier_scorecard_standing_domain.models.supplier_scorecard_standing.SupplierScorecardStanding", foreign_keys=[standing_name_id])

    standing_color: Mapped[Optional[str]] = mapped_column(SAEnum(SupplierScorecardScoringStandingStandingColor, native_enum=False, length=10, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    min_grade: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    max_grade: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    warn_rfqs: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    warn_pos: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    prevent_rfqs: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    prevent_pos: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    notify_supplier: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    notify_employee: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    employee_link: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SupplierScorecardScoringStanding id={self.id}>"
