"""

Customer Number At Supplier -- converted from ``erpnext/buying/doctype/customer_number_at_supplier``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Supplier).

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["CustomerNumberAtSupplier"]







class CustomerNumberAtSupplier(ChildTableModel, TenantModel):

    __tablename__ = "customer_number_at_suppliers"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_customer_number_at_suppliers_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("suppliers.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "Supplier",

        back_populates="customer_numbers",

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



    company: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    customer_number: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<CustomerNumberAtSupplier id={self.id}>"
