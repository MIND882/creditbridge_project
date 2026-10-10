"""Pydantic v2 schemas for ItemDefault."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ItemDefaultCreate",

    "ItemDefaultRead",

    "ItemDefaultListResponse",

]





class ItemDefaultBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    company: str

    default_warehouse_id: Optional[uuid.UUID] = None

    default_price_list_id: Optional[uuid.UUID] = None

    default_discount_account_id: Optional[uuid.UUID] = None

    default_inventory_account_id: Optional[uuid.UUID] = None

    inventory_account_currency: Optional[str] = None

    vf_default_warehouse: Optional[str] = None

    vf_default_price_list: Optional[str] = None

    vf_default_discount_account: Optional[str] = None

    vf_default_inventory_account: Optional[str] = None

    buying_cost_center_id: Optional[uuid.UUID] = None

    default_supplier: Optional[str] = None

    expense_account_id: Optional[uuid.UUID] = None

    default_provisional_account_id: Optional[uuid.UUID] = None

    purchase_expense_account_id: Optional[uuid.UUID] = None

    purchase_expense_contra_account_id: Optional[uuid.UUID] = None

    expenses_added_to_stock_account_id: Optional[uuid.UUID] = None

    expenses_added_to_stock_contra_account_id: Optional[uuid.UUID] = None

    purchase_price_variance_account_id: Optional[uuid.UUID] = None

    manufacturing_variance_account_id: Optional[uuid.UUID] = None

    vf_buying_cost_center: Optional[str] = None

    vf_default_supplier: Optional[str] = None

    vf_expense_account: Optional[str] = None

    vf_default_provisional_account: Optional[str] = None

    vf_purchase_expense_account: Optional[str] = None

    vf_purchase_expense_contra_account: Optional[str] = None

    vf_expenses_added_to_stock_account: Optional[str] = None

    vf_expenses_added_to_stock_contra_account: Optional[str] = None

    selling_cost_center_id: Optional[uuid.UUID] = None

    income_account_id: Optional[uuid.UUID] = None

    vf_selling_cost_center: Optional[str] = None

    vf_income_account: Optional[str] = None

    default_cogs_account_id: Optional[uuid.UUID] = None

    vf_default_cogs_account: Optional[str] = None

    deferred_expense_account_id: Optional[uuid.UUID] = None

    deferred_revenue_account_id: Optional[uuid.UUID] = None

    vf_deferred_expense_account: Optional[str] = None

    vf_deferred_revenue_account: Optional[str] = None





class ItemDefaultCreate(ItemDefaultBase):

    pass





class ItemDefaultUpdate(InputSchema):

    """A partial update."""



    company: Optional[str] = None

    default_warehouse_id: Optional[uuid.UUID] = None

    default_price_list_id: Optional[uuid.UUID] = None

    default_discount_account_id: Optional[uuid.UUID] = None

    default_inventory_account_id: Optional[uuid.UUID] = None

    inventory_account_currency: Optional[str] = None

    vf_default_warehouse: Optional[str] = None

    vf_default_price_list: Optional[str] = None

    vf_default_discount_account: Optional[str] = None

    vf_default_inventory_account: Optional[str] = None

    buying_cost_center_id: Optional[uuid.UUID] = None

    default_supplier: Optional[str] = None

    expense_account_id: Optional[uuid.UUID] = None

    default_provisional_account_id: Optional[uuid.UUID] = None

    purchase_expense_account_id: Optional[uuid.UUID] = None

    purchase_expense_contra_account_id: Optional[uuid.UUID] = None

    expenses_added_to_stock_account_id: Optional[uuid.UUID] = None

    expenses_added_to_stock_contra_account_id: Optional[uuid.UUID] = None

    purchase_price_variance_account_id: Optional[uuid.UUID] = None

    manufacturing_variance_account_id: Optional[uuid.UUID] = None

    vf_buying_cost_center: Optional[str] = None

    vf_default_supplier: Optional[str] = None

    vf_expense_account: Optional[str] = None

    vf_default_provisional_account: Optional[str] = None

    vf_purchase_expense_account: Optional[str] = None

    vf_purchase_expense_contra_account: Optional[str] = None

    vf_expenses_added_to_stock_account: Optional[str] = None

    vf_expenses_added_to_stock_contra_account: Optional[str] = None

    selling_cost_center_id: Optional[uuid.UUID] = None

    income_account_id: Optional[uuid.UUID] = None

    vf_selling_cost_center: Optional[str] = None

    vf_income_account: Optional[str] = None

    default_cogs_account_id: Optional[uuid.UUID] = None

    vf_default_cogs_account: Optional[str] = None

    deferred_expense_account_id: Optional[uuid.UUID] = None

    deferred_revenue_account_id: Optional[uuid.UUID] = None

    vf_deferred_expense_account: Optional[str] = None

    vf_deferred_revenue_account: Optional[str] = None





class ItemDefaultRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    company: str

    default_warehouse_id: Optional[uuid.UUID] = None

    default_price_list_id: Optional[uuid.UUID] = None

    default_discount_account_id: Optional[uuid.UUID] = None

    default_inventory_account_id: Optional[uuid.UUID] = None

    inventory_account_currency: Optional[str] = None

    vf_default_warehouse: Optional[str] = None

    vf_default_price_list: Optional[str] = None

    vf_default_discount_account: Optional[str] = None

    vf_default_inventory_account: Optional[str] = None

    buying_cost_center_id: Optional[uuid.UUID] = None

    default_supplier: Optional[str] = None

    expense_account_id: Optional[uuid.UUID] = None

    default_provisional_account_id: Optional[uuid.UUID] = None

    purchase_expense_account_id: Optional[uuid.UUID] = None

    purchase_expense_contra_account_id: Optional[uuid.UUID] = None

    expenses_added_to_stock_account_id: Optional[uuid.UUID] = None

    expenses_added_to_stock_contra_account_id: Optional[uuid.UUID] = None

    purchase_price_variance_account_id: Optional[uuid.UUID] = None

    manufacturing_variance_account_id: Optional[uuid.UUID] = None

    vf_buying_cost_center: Optional[str] = None

    vf_default_supplier: Optional[str] = None

    vf_expense_account: Optional[str] = None

    vf_default_provisional_account: Optional[str] = None

    vf_purchase_expense_account: Optional[str] = None

    vf_purchase_expense_contra_account: Optional[str] = None

    vf_expenses_added_to_stock_account: Optional[str] = None

    vf_expenses_added_to_stock_contra_account: Optional[str] = None

    selling_cost_center_id: Optional[uuid.UUID] = None

    income_account_id: Optional[uuid.UUID] = None

    vf_selling_cost_center: Optional[str] = None

    vf_income_account: Optional[str] = None

    default_cogs_account_id: Optional[uuid.UUID] = None

    vf_default_cogs_account: Optional[str] = None

    deferred_expense_account_id: Optional[uuid.UUID] = None

    deferred_revenue_account_id: Optional[uuid.UUID] = None

    vf_deferred_expense_account: Optional[str] = None

    vf_deferred_revenue_account: Optional[str] = None





ItemDefaultListResponse = Page[ItemDefaultRead]
