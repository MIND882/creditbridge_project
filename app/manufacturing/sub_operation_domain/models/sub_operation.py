"""

Sub Operation -- converted from ``erpnext/manufacturing/doctype/sub_operation``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Operation).

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["SubOperation"]







class SubOperation(ChildTableModel, TenantModel):

    __tablename__ = "sub_operations"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_sub_operations_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("operations.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "app.manufacturing.operation_domain.models.operation.Operation",

        back_populates="sub_operations",

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



    operation_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("operations.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    operation = relationship("app.manufacturing.operation_domain.models.operation.Operation", foreign_keys=[operation_id])

    time_in_mins: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0)

    description: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SubOperation id={self.id}>"
