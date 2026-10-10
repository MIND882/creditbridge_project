"""Pydantic v2 schemas for Supplier."""





from __future__ import annotations

from app.buying.supplier_domain.models.supplier import (

    SupplierNamingSeries,

    SupplierSupplierType,

    SupplierHoldType,

)

from typing import Optional

import datetime as dt

import uuid



from app.buying.customer_number_at_supplier_domain.schemas.customer_number_at_supplier import (

    CustomerNumberAtSupplierCreate,

    CustomerNumberAtSupplierRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SupplierCreate",

    "SupplierUpdate",

    "SupplierRead",

    "SupplierListResponse",

]





class SupplierBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    naming_series: Optional[SupplierNamingSeries] = None

    supplier_name: str

    country: Optional[str] = None

    default_bank_account_id: Optional[uuid.UUID] = None

    tax_id: Optional[str] = None

    tax_category_id: Optional[uuid.UUID] = None

    tax_withholding_category_id: Optional[uuid.UUID] = None

    is_transporter: Optional[bool] = None

    is_internal_supplier: Optional[bool] = None

    represents_company: Optional[str] = None

    image: Optional[str] = None

    supplier_group: Optional[str] = None

    supplier_type: SupplierSupplierType

    language: Optional[str] = None

    disabled: Optional[bool] = None

    warn_rfqs: Optional[bool] = None

    warn_pos: Optional[bool] = None

    prevent_rfqs: Optional[bool] = None

    prevent_pos: Optional[bool] = None

    default_currency: Optional[str] = None

    default_price_list_id: Optional[uuid.UUID] = None

    payment_terms_id: Optional[uuid.UUID] = None

    on_hold: Optional[bool] = None

    hold_type: Optional[SupplierHoldType] = None

    release_date: Optional[dt.date] = None

    website: Optional[str] = None

    supplier_details: Optional[str] = None

    is_frozen: Optional[bool] = None

    allow_purchase_invoice_creation_without_purchase_order: Optional[bool] = None

    allow_purchase_invoice_creation_without_purchase_receipt: Optional[bool] = None

    supplier_primary_contact: Optional[str] = None

    mobile_no: Optional[str] = None

    email_id: Optional[str] = None

    primary_address: Optional[str] = None

    supplier_primary_address: Optional[str] = None

    restrict_to_companies: Optional[bool] = None

    tax_withholding_group_id: Optional[uuid.UUID] = None

    gender: Optional[str] = None

    alias: Optional[str] = None

    customer_numbers: list[CustomerNumberAtSupplierCreate] = []





class SupplierCreate(SupplierBase):

    pass





class SupplierUpdate(InputSchema):

    """A partial update."""



    naming_series: Optional[SupplierNamingSeries] = None

    supplier_name: Optional[str] = None

    country: Optional[str] = None

    default_bank_account_id: Optional[uuid.UUID] = None

    tax_id: Optional[str] = None

    tax_category_id: Optional[uuid.UUID] = None

    tax_withholding_category_id: Optional[uuid.UUID] = None

    is_transporter: Optional[bool] = None

    is_internal_supplier: Optional[bool] = None

    represents_company: Optional[str] = None

    image: Optional[str] = None

    supplier_group: Optional[str] = None

    supplier_type: Optional[SupplierSupplierType] = None

    language: Optional[str] = None

    disabled: Optional[bool] = None

    warn_rfqs: Optional[bool] = None

    warn_pos: Optional[bool] = None

    prevent_rfqs: Optional[bool] = None

    prevent_pos: Optional[bool] = None

    default_currency: Optional[str] = None

    default_price_list_id: Optional[uuid.UUID] = None

    payment_terms_id: Optional[uuid.UUID] = None

    on_hold: Optional[bool] = None

    hold_type: Optional[SupplierHoldType] = None

    release_date: Optional[dt.date] = None

    website: Optional[str] = None

    supplier_details: Optional[str] = None

    is_frozen: Optional[bool] = None

    allow_purchase_invoice_creation_without_purchase_order: Optional[bool] = None

    allow_purchase_invoice_creation_without_purchase_receipt: Optional[bool] = None

    supplier_primary_contact: Optional[str] = None

    mobile_no: Optional[str] = None

    email_id: Optional[str] = None

    primary_address: Optional[str] = None

    supplier_primary_address: Optional[str] = None

    restrict_to_companies: Optional[bool] = None

    tax_withholding_group_id: Optional[uuid.UUID] = None

    gender: Optional[str] = None

    alias: Optional[str] = None

    customer_numbers: Optional[list[CustomerNumberAtSupplierCreate]] = None





class SupplierRead(ReadSchema):

    id: uuid.UUID

    name: str

    naming_series: Optional[SupplierNamingSeries] = None

    supplier_name: str

    country: Optional[str] = None

    default_bank_account_id: Optional[uuid.UUID] = None

    tax_id: Optional[str] = None

    tax_category_id: Optional[uuid.UUID] = None

    tax_withholding_category_id: Optional[uuid.UUID] = None

    is_transporter: Optional[bool] = None

    is_internal_supplier: Optional[bool] = None

    represents_company: Optional[str] = None

    image: Optional[str] = None

    supplier_group: Optional[str] = None

    supplier_type: Optional[SupplierSupplierType] = None

    language: Optional[str] = None

    disabled: Optional[bool] = None

    warn_rfqs: Optional[bool] = None

    warn_pos: Optional[bool] = None

    prevent_rfqs: Optional[bool] = None

    prevent_pos: Optional[bool] = None

    default_currency: Optional[str] = None

    default_price_list_id: Optional[uuid.UUID] = None

    payment_terms_id: Optional[uuid.UUID] = None

    on_hold: Optional[bool] = None

    hold_type: Optional[SupplierHoldType] = None

    release_date: Optional[dt.date] = None

    website: Optional[str] = None

    supplier_details: Optional[str] = None

    is_frozen: Optional[bool] = None

    allow_purchase_invoice_creation_without_purchase_order: Optional[bool] = None

    allow_purchase_invoice_creation_without_purchase_receipt: Optional[bool] = None

    supplier_primary_contact: Optional[str] = None

    mobile_no: Optional[str] = None

    email_id: Optional[str] = None

    primary_address: Optional[str] = None

    supplier_primary_address: Optional[str] = None

    restrict_to_companies: Optional[bool] = None

    tax_withholding_group_id: Optional[uuid.UUID] = None

    gender: Optional[str] = None

    alias: Optional[str] = None

    customer_numbers: list[CustomerNumberAtSupplierRead] = []





SupplierListResponse = Page[SupplierRead]
