"""

Supplier Scorecard Scoring Criteria -- converted from ``erpnext/buying/doctype/supplier_scorecard_scoring_criteria``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Supplier Scorecard).

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["SupplierScorecardScoringCriteria"]







class SupplierScorecardScoringCriteria(ChildTableModel, TenantModel):

    __tablename__ = "supplier_scorecard_scoring_criterias"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_supplier_scorecard_scoring_criterias_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("supplier_scorecards.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "SupplierScorecard",

        back_populates="criteria",

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



    criteria_name_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("supplier_scorecard_criterias.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    criteria_name = relationship("app.buying.supplier_scorecard_criteria_domain.models.supplier_scorecard_criteria.SupplierScorecardCriteria", foreign_keys=[criteria_name_id])

    score: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    weight: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    max_score: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=100)

    formula: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SupplierScorecardScoringCriteria id={self.id}>"
