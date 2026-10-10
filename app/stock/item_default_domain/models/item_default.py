"""

Item Default -- converted from ``erpnext/stock/doctype/item_default``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Item).

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["ItemDefault"]







class ItemDefault(ChildTableModel, TenantModel):

    __tablename__ = "item_defaults"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_item_defaults_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "Item",

        back_populates="item_defaults",

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



    company: Mapped[str] = mapped_column(String(140), nullable=False)

    default_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    default_warehouse = relationship("Warehouse", foreign_keys=[default_warehouse_id])

    default_price_list_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("price_lists.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    default_price_list = relationship("PriceList", foreign_keys=[default_price_list_id])

    default_discount_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    default_discount_account = relationship("Account", foreign_keys=[default_discount_account_id])

    default_inventory_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    default_inventory_account = relationship("Account", foreign_keys=[default_inventory_account_id])

    inventory_account_currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    vf_default_warehouse: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    vf_default_price_list: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    vf_default_discount_account: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    vf_default_inventory_account: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    buying_cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    buying_cost_center = relationship("CostCenter", foreign_keys=[buying_cost_center_id])

    default_supplier: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    expense_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    expense_account = relationship("Account", foreign_keys=[expense_account_id])

    default_provisional_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    default_provisional_account = relationship("Account", foreign_keys=[default_provisional_account_id])

    purchase_expense_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    purchase_expense_account = relationship("Account", foreign_keys=[purchase_expense_account_id])

    purchase_expense_contra_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    purchase_expense_contra_account = relationship("Account", foreign_keys=[purchase_expense_contra_account_id])

    expenses_added_to_stock_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    expenses_added_to_stock_account = relationship("Account", foreign_keys=[expenses_added_to_stock_account_id])

    expenses_added_to_stock_contra_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    expenses_added_to_stock_contra_account = relationship("Account", foreign_keys=[expenses_added_to_stock_contra_account_id])

    purchase_price_variance_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    purchase_price_variance_account = relationship("Account", foreign_keys=[purchase_price_variance_account_id])

    manufacturing_variance_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    manufacturing_variance_account = relationship("Account", foreign_keys=[manufacturing_variance_account_id])

    vf_buying_cost_center: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    vf_default_supplier: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    vf_expense_account: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    vf_default_provisional_account: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    vf_purchase_expense_account: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    vf_purchase_expense_contra_account: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    vf_expenses_added_to_stock_account: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    vf_expenses_added_to_stock_contra_account: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    selling_cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    selling_cost_center = relationship("CostCenter", foreign_keys=[selling_cost_center_id])

    income_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    income_account = relationship("Account", foreign_keys=[income_account_id])

    vf_selling_cost_center: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    vf_income_account: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    default_cogs_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    default_cogs_account = relationship("Account", foreign_keys=[default_cogs_account_id])

    vf_default_cogs_account: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    deferred_expense_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    deferred_expense_account = relationship("Account", foreign_keys=[deferred_expense_account_id])

    deferred_revenue_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    deferred_revenue_account = relationship("Account", foreign_keys=[deferred_revenue_account_id])

    vf_deferred_expense_account: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    vf_deferred_revenue_account: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ItemDefault id={self.id}>"
