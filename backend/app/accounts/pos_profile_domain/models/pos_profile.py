"""

POS Profile -- converted from ``erpnext/accounts/doctype/pos_profile``.





"""



from __future__ import annotations



import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.pos_customer_group_domain.models.pos_customer_group import POSCustomerGroup

from app.accounts.pos_item_group_domain.models.pos_item_group import POSItemGroup

from app.accounts.pos_payment_method_domain.models.pos_payment_method import POSPaymentMethod

from app.accounts.pos_profile_user_domain.models.pos_profile_user import POSProfileUser



from app.accounts.account_domain.models.account import Account  # noqa: F401

from app.accounts.cost_center_domain.models.cost_center import CostCenter  # noqa: F401

from app.accounts.tax_category_domain.models.tax_category import TaxCategory  # noqa: F401



from app.core.base_model import TenantModel



__all__ = ["POSProfile", "POSProfileApplyDiscountOn", "POSProfileActionOnNewInvoice"]







class POSProfileApplyDiscountOn(str, enum.Enum):

    GRAND_TOTAL = "Grand Total"

    NET_TOTAL = "Net Total"





class POSProfileActionOnNewInvoice(str, enum.Enum):

    ALWAYS_ASK = "Always Ask"

    SAVE_CHANGES_AND_LOAD_NEW_INVOICE = "Save Changes and Load New Invoice"

    DISCARD_CHANGES_AND_LOAD_NEW_INVOICE = "Discard Changes and Load New Invoice"









class POSProfile(TenantModel):

    __tablename__ = "pos_profiles"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_pos_profiles_business_name"),

    )



    #: ``autoname`` = 'Prompt'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    customer: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    country: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    company_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    letter_head: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    tc_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    select_print_heading: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    selling_price_list: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    write_off_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    write_off_account = relationship("Account", foreign_keys=[write_off_account_id])

    write_off_cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    write_off_cost_center = relationship("CostCenter", foreign_keys=[write_off_cost_center_id])

    account_for_change_amount_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    account_for_change_amount = relationship("Account", foreign_keys=[account_for_change_amount_id])

    income_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    income_account = relationship("Account", foreign_keys=[income_account_id])

    expense_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    expense_account = relationship("Account", foreign_keys=[expense_account_id])

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])

    taxes_and_charges: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    apply_discount_on: Mapped[Optional[POSProfileApplyDiscountOn]] = mapped_column(

        SAEnum(POSProfileApplyDiscountOn, native_enum=False, length=11, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    tax_category_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("tax_categories.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    tax_category = relationship("TaxCategory", foreign_keys=[tax_category_id])

    print_format: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    warehouse: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    ignore_pricing_rule: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    update_stock: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    hide_unavailable_items: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    hide_images: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    auto_add_item_to_cart: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    allow_rate_change: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    allow_discount_change: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    validate_stock_on_save: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    write_off_limit: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    disable_rounded_total: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    utm_campaign: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    utm_source: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    utm_medium: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    print_receipt_on_order_complete: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    set_grand_total_to_default_mop: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    action_on_new_invoice: Mapped[Optional[POSProfileActionOnNewInvoice]] = mapped_column(

        SAEnum(POSProfileActionOnNewInvoice, native_enum=False, length=36, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    allow_partial_payment: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    allow_warehouse_change: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)



    applicable_for_users = relationship(

        POSProfileUser,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=POSProfileUser.idx,

        passive_deletes=True,

    )

    payments = relationship(

        POSPaymentMethod,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=POSPaymentMethod.idx,

        passive_deletes=True,

    )

    item_groups = relationship(

        POSItemGroup,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=POSItemGroup.idx,

        passive_deletes=True,

    )

    customer_groups = relationship(

        POSCustomerGroup,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=POSCustomerGroup.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<POSProfile id={self.id}>"
