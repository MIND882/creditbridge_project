"""Pydantic v2 schemas for Customer."""





from __future__ import annotations

from app.selling.customer_domain.models.customer import (

    CustomerNamingSeries,

    CustomerCustomerType,

)

from decimal import Decimal

from typing import Optional

import uuid



from app.selling.customer_credit_limit_domain.schemas.customer_credit_limit import (

    CustomerCreditLimitCreate,

    CustomerCreditLimitRead,

)

from app.selling.sales_team_domain.schemas.sales_team import (

    SalesTeamCreate,

    SalesTeamRead,

)

from app.selling.supplier_number_at_customer_domain.schemas.supplier_number_at_customer import (

    SupplierNumberAtCustomerCreate,

    SupplierNumberAtCustomerRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "CustomerCreate",

    "CustomerUpdate",

    "CustomerRead",

    "CustomerListResponse",

]





class CustomerBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    naming_series: Optional[CustomerNamingSeries] = None

    customer_name: str

    alias: Optional[str] = None

    customer_type: CustomerCustomerType

    gender: Optional[str] = None

    customer_group: Optional[str] = None

    territory: Optional[str] = None

    image: Optional[str] = None

    default_currency: Optional[str] = None

    default_bank_account_id: Optional[uuid.UUID] = None

    default_price_list_id: Optional[uuid.UUID] = None

    payment_terms_id: Optional[uuid.UUID] = None

    loyalty_program_id: Optional[uuid.UUID] = None

    loyalty_program_tier: Optional[str] = None

    customer_primary_address: Optional[str] = None

    primary_address: Optional[str] = None

    customer_primary_contact: Optional[str] = None

    mobile_no: Optional[str] = None

    email_id: Optional[str] = None

    first_name: Optional[str] = None

    last_name: Optional[str] = None

    is_internal_customer: Optional[bool] = None

    represents_company: Optional[str] = None

    tax_id: Optional[str] = None

    tax_category_id: Optional[uuid.UUID] = None

    tax_withholding_group_id: Optional[uuid.UUID] = None

    tax_withholding_category_id: Optional[uuid.UUID] = None

    restrict_to_companies: Optional[bool] = None

    so_required: Optional[bool] = None

    dn_required: Optional[bool] = None

    disabled: Optional[bool] = None

    is_frozen: Optional[bool] = None

    account_manager: Optional[str] = None

    default_sales_partner: Optional[str] = None

    default_commission_rate: Optional[Decimal] = None

    lead_name: Optional[str] = None

    opportunity_name: Optional[str] = None

    prospect_name: Optional[str] = None

    market_segment: Optional[str] = None

    industry_id: Optional[uuid.UUID] = None

    website: Optional[str] = None

    language: Optional[str] = None

    customer_pos_id: Optional[str] = None

    customer_details: Optional[str] = None

    credit_limits: list[CustomerCreditLimitCreate] = []

    sales_team: list[SalesTeamCreate] = []

    supplier_numbers: list[SupplierNumberAtCustomerCreate] = []





class CustomerCreate(CustomerBase):

    pass





class CustomerUpdate(InputSchema):

    """A partial update."""



    naming_series: Optional[CustomerNamingSeries] = None

    customer_name: Optional[str] = None

    alias: Optional[str] = None

    customer_type: Optional[CustomerCustomerType] = None

    gender: Optional[str] = None

    customer_group: Optional[str] = None

    territory: Optional[str] = None

    image: Optional[str] = None

    default_currency: Optional[str] = None

    default_bank_account_id: Optional[uuid.UUID] = None

    default_price_list_id: Optional[uuid.UUID] = None

    payment_terms_id: Optional[uuid.UUID] = None

    loyalty_program_id: Optional[uuid.UUID] = None

    loyalty_program_tier: Optional[str] = None

    customer_primary_address: Optional[str] = None

    primary_address: Optional[str] = None

    customer_primary_contact: Optional[str] = None

    mobile_no: Optional[str] = None

    email_id: Optional[str] = None

    first_name: Optional[str] = None

    last_name: Optional[str] = None

    is_internal_customer: Optional[bool] = None

    represents_company: Optional[str] = None

    tax_id: Optional[str] = None

    tax_category_id: Optional[uuid.UUID] = None

    tax_withholding_group_id: Optional[uuid.UUID] = None

    tax_withholding_category_id: Optional[uuid.UUID] = None

    restrict_to_companies: Optional[bool] = None

    so_required: Optional[bool] = None

    dn_required: Optional[bool] = None

    disabled: Optional[bool] = None

    is_frozen: Optional[bool] = None

    account_manager: Optional[str] = None

    default_sales_partner: Optional[str] = None

    default_commission_rate: Optional[Decimal] = None

    lead_name: Optional[str] = None

    opportunity_name: Optional[str] = None

    prospect_name: Optional[str] = None

    market_segment: Optional[str] = None

    industry_id: Optional[uuid.UUID] = None

    website: Optional[str] = None

    language: Optional[str] = None

    customer_pos_id: Optional[str] = None

    customer_details: Optional[str] = None

    credit_limits: Optional[list[CustomerCreditLimitCreate]] = None

    sales_team: Optional[list[SalesTeamCreate]] = None

    supplier_numbers: Optional[list[SupplierNumberAtCustomerCreate]] = None





class CustomerRead(ReadSchema):

    id: uuid.UUID

    name: str

    naming_series: Optional[CustomerNamingSeries] = None

    customer_name: str

    alias: Optional[str] = None

    customer_type: Optional[CustomerCustomerType] = None

    gender: Optional[str] = None

    customer_group: Optional[str] = None

    territory: Optional[str] = None

    image: Optional[str] = None

    default_currency: Optional[str] = None

    default_bank_account_id: Optional[uuid.UUID] = None

    default_price_list_id: Optional[uuid.UUID] = None

    payment_terms_id: Optional[uuid.UUID] = None

    loyalty_program_id: Optional[uuid.UUID] = None

    loyalty_program_tier: Optional[str] = None

    customer_primary_address: Optional[str] = None

    primary_address: Optional[str] = None

    customer_primary_contact: Optional[str] = None

    mobile_no: Optional[str] = None

    email_id: Optional[str] = None

    first_name: Optional[str] = None

    last_name: Optional[str] = None

    is_internal_customer: Optional[bool] = None

    represents_company: Optional[str] = None

    tax_id: Optional[str] = None

    tax_category_id: Optional[uuid.UUID] = None

    tax_withholding_group_id: Optional[uuid.UUID] = None

    tax_withholding_category_id: Optional[uuid.UUID] = None

    restrict_to_companies: Optional[bool] = None

    so_required: Optional[bool] = None

    dn_required: Optional[bool] = None

    disabled: Optional[bool] = None

    is_frozen: Optional[bool] = None

    account_manager: Optional[str] = None

    default_sales_partner: Optional[str] = None

    default_commission_rate: Optional[Decimal] = None

    lead_name: Optional[str] = None

    opportunity_name: Optional[str] = None

    prospect_name: Optional[str] = None

    market_segment: Optional[str] = None

    industry_id: Optional[uuid.UUID] = None

    website: Optional[str] = None

    language: Optional[str] = None

    customer_pos_id: Optional[str] = None

    customer_details: Optional[str] = None

    credit_limits: list[CustomerCreditLimitRead] = []

    sales_team: list[SalesTeamRead] = []

    supplier_numbers: list[SupplierNumberAtCustomerRead] = []





CustomerListResponse = Page[CustomerRead]
