"""Pydantic v2 schemas for POSProfile."""





from __future__ import annotations

from app.accounts.pos_profile_domain.models.pos_profile import (

    POSProfileActionOnNewInvoice,

    POSProfileApplyDiscountOn,

)

from decimal import Decimal

from typing import Optional

import uuid



from app.accounts.pos_payment_method_domain.schemas.pos_payment_method import (

    POSPaymentMethodCreate,

    POSPaymentMethodRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.pos_profile_user_domain.schemas.pos_profile_user import (

    POSProfileUserCreate,

    POSProfileUserRead,

)

from app.accounts.cashier_closing_payments_domain.schemas.cashier_closing_payments import (

    CashierClosingPaymentsCreate,

    CashierClosingPaymentsRead,

)

from app.accounts.pos_item_group_domain.schemas.pos_item_group import (

    POSItemGroupCreate,

    POSItemGroupRead,

)

from app.accounts.pos_customer_group_domain.schemas.pos_customer_group import (

    POSCustomerGroupCreate,

    POSCustomerGroupRead,

)



__all__ = [

    "POSProfileCreate",

    "POSProfileUpdate",

    "POSProfileRead",

    "POSProfileListResponse",

]





class POSProfileBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    disabled: Optional[bool] = None

    customer: Optional[str] = None

    country: Optional[str] = None

    company_address: Optional[str] = None

    letter_head: Optional[str] = None

    tc_name: Optional[str] = None

    select_print_heading: Optional[str] = None

    selling_price_list: Optional[str] = None

    currency: str

    write_off_account_id: uuid.UUID

    write_off_cost_center_id: uuid.UUID

    account_for_change_amount_id: Optional[uuid.UUID] = None

    income_account_id: Optional[uuid.UUID] = None

    expense_account_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    taxes_and_charges: Optional[str] = None

    apply_discount_on: Optional[POSProfileApplyDiscountOn] = None

    tax_category_id: Optional[uuid.UUID] = None

    print_format: Optional[str] = None

    warehouse: str

    ignore_pricing_rule: Optional[bool] = None

    update_stock: Optional[bool] = None

    hide_unavailable_items: Optional[bool] = None

    hide_images: Optional[bool] = None

    auto_add_item_to_cart: Optional[bool] = None

    allow_rate_change: Optional[bool] = None

    allow_discount_change: Optional[bool] = None

    validate_stock_on_save: Optional[bool] = None

    write_off_limit: Optional[Decimal] = None

    disable_rounded_total: Optional[bool] = None

    utm_campaign: Optional[str] = None

    utm_source: Optional[str] = None

    utm_medium: Optional[str] = None

    print_receipt_on_order_complete: Optional[bool] = None

    project: Optional[str] = None

    set_grand_total_to_default_mop: Optional[bool] = None

    action_on_new_invoice: Optional[POSProfileActionOnNewInvoice] = None

    allow_partial_payment: Optional[bool] = None

    allow_warehouse_change: Optional[bool] = None



    applicable_for_users: list[POSProfileUserCreate] = []



    payments: list[POSPaymentMethodCreate] = []



    item_groups: list[POSItemGroupCreate] = []



    customer_groups: list[POSCustomerGroupCreate] = []





class POSProfileCreate(POSProfileBase):

    pass





class POSProfileUpdate(InputSchema):

    """A partial update."""



    disabled: Optional[bool] = None

    customer: Optional[str] = None

    country: Optional[str] = None

    company_address: Optional[str] = None

    letter_head: Optional[str] = None

    tc_name: Optional[str] = None

    select_print_heading: Optional[str] = None

    selling_price_list: Optional[str] = None

    currency: Optional[str] = None

    write_off_account_id: Optional[uuid.UUID] = None

    write_off_cost_center_id: Optional[uuid.UUID] = None

    account_for_change_amount_id: Optional[uuid.UUID] = None

    income_account_id: Optional[uuid.UUID] = None

    expense_account_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    taxes_and_charges: Optional[str] = None

    apply_discount_on: Optional[POSProfileApplyDiscountOn] = None

    tax_category_id: Optional[uuid.UUID] = None

    print_format: Optional[str] = None

    warehouse: Optional[str] = None

    ignore_pricing_rule: Optional[bool] = None

    update_stock: Optional[bool] = None

    hide_unavailable_items: Optional[bool] = None

    hide_images: Optional[bool] = None

    auto_add_item_to_cart: Optional[bool] = None

    allow_rate_change: Optional[bool] = None

    allow_discount_change: Optional[bool] = None

    validate_stock_on_save: Optional[bool] = None

    write_off_limit: Optional[Decimal] = None

    disable_rounded_total: Optional[bool] = None

    utm_campaign: Optional[str] = None

    utm_source: Optional[str] = None

    utm_medium: Optional[str] = None

    print_receipt_on_order_complete: Optional[bool] = None

    project: Optional[str] = None

    set_grand_total_to_default_mop: Optional[bool] = None

    action_on_new_invoice: Optional[POSProfileActionOnNewInvoice] = None

    allow_partial_payment: Optional[bool] = None

    allow_warehouse_change: Optional[bool] = None

    applicable_for_users: Optional[list[POSProfileUserCreate]] = None

    payments: Optional[list[POSPaymentMethodCreate]] = None

    item_groups: Optional[list[POSItemGroupCreate]] = None

    customer_groups: Optional[list[POSCustomerGroupCreate]] = None





class POSProfileRead(ReadSchema):

    id: uuid.UUID

    name: str

    disabled: bool

    customer: Optional[str] = None

    country: Optional[str] = None

    company_address: Optional[str] = None

    letter_head: Optional[str] = None

    tc_name: Optional[str] = None

    select_print_heading: Optional[str] = None

    selling_price_list: Optional[str] = None

    currency: str

    write_off_account_id: uuid.UUID

    write_off_cost_center_id: uuid.UUID

    account_for_change_amount_id: Optional[uuid.UUID] = None

    income_account_id: Optional[uuid.UUID] = None

    expense_account_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    taxes_and_charges: Optional[str] = None

    apply_discount_on: Optional[POSProfileApplyDiscountOn] = None

    tax_category_id: Optional[uuid.UUID] = None

    print_format: Optional[str] = None

    warehouse: str

    ignore_pricing_rule: bool

    update_stock: bool

    hide_unavailable_items: bool

    hide_images: bool

    auto_add_item_to_cart: bool

    allow_rate_change: bool

    allow_discount_change: bool

    validate_stock_on_save: bool

    write_off_limit: Decimal

    disable_rounded_total: bool

    utm_campaign: Optional[str] = None

    utm_source: Optional[str] = None

    utm_medium: Optional[str] = None

    print_receipt_on_order_complete: bool

    project: Optional[str] = None

    set_grand_total_to_default_mop: bool

    action_on_new_invoice: Optional[POSProfileActionOnNewInvoice] = None

    allow_partial_payment: bool

    allow_warehouse_change: bool

    applicable_for_users: list[POSProfileUserRead] = []

    payments: list[POSPaymentMethodRead] = []

    item_groups: list[POSItemGroupRead] = []

    customer_groups: list[POSCustomerGroupRead] = []





POSProfileListResponse = Page[POSProfileRead]
