"""

Supplier Scorecard Scoring Variable -- converted from ``erpnext/buying/doctype/supplier_scorecard_scoring_variable``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Supplier Scorecard Period).

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["SupplierScorecardScoringVariable"]







class SupplierScorecardScoringVariable(ChildTableModel, TenantModel):

    __tablename__ = "supplier_scorecard_scoring_variables"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_supplier_scorecard_scoring_variables_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("supplier_scorecard_periods.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "SupplierScorecardPeriod",

        back_populates="variables",

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



    variable_label_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("supplier_scorecard_variables.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    variable_label = relationship("app.buying.supplier_scorecard_variable_domain.models.supplier_scorecard_variable.SupplierScorecardVariable", foreign_keys=[variable_label_id])

    description: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    value: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    param_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    path: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SupplierScorecardScoringVariable id={self.id}>"
