"""

Sales Team -- converted from ``erpnext/selling/doctype/sales_team``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Customer).

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["SalesTeam"]







class SalesTeam(ChildTableModel, TenantModel):

    __tablename__ = "sales_teams"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_sales_teams_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("selling_customers.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "app.selling.customer_domain.models.customer.Customer",

        back_populates="sales_team",

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



    sales_person: Mapped[str] = mapped_column(String(140), nullable=False)

    contact_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    allocated_percentage: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    allocated_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    commission_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    incentives: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SalesTeam id={self.id}>"
