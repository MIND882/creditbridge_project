"""Pydantic v2 schemas for LandedCostVoucher."""





from __future__ import annotations

from app.stock.landed_cost_voucher_domain.models.landed_cost_voucher import (

    LandedCostVoucherNamingSeries,

    LandedCostVoucherDistributeChargesBasedOn,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.stock.landed_cost_purchase_receipt_domain.schemas.landed_cost_purchase_receipt import (

    LandedCostPurchaseReceiptCreate,

    LandedCostPurchaseReceiptRead,

)

from app.stock.landed_cost_item_domain.schemas.landed_cost_item import (

    LandedCostItemCreate,

    LandedCostItemRead,

)

from app.stock.landed_cost_taxes_and_charges_domain.schemas.landed_cost_taxes_and_charges import (

    LandedCostTaxesAndChargesCreate,

    LandedCostTaxesAndChargesRead,

)

from app.stock.landed_cost_vendor_invoice_domain.schemas.landed_cost_vendor_invoice import (

    LandedCostVendorInvoiceCreate,

    LandedCostVendorInvoiceRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "LandedCostVoucherCreate",

    "LandedCostVoucherUpdate",

    "LandedCostVoucherRead",

    "LandedCostVoucherListResponse",

]





class LandedCostVoucherBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    naming_series: LandedCostVoucherNamingSeries

    company: str

    total_taxes_and_charges: Decimal

    distribute_charges_based_on: LandedCostVoucherDistributeChargesBasedOn

    amended_from_id: Optional[uuid.UUID] = None

    posting_date: dt.date

    total_vendor_invoices_cost: Optional[Decimal] = None

    purchase_receipts: list[LandedCostPurchaseReceiptCreate] = []

    items: list[LandedCostItemCreate] = []

    taxes: list[LandedCostTaxesAndChargesCreate] = []

    vendor_invoices: list[LandedCostVendorInvoiceCreate] = []





class LandedCostVoucherCreate(LandedCostVoucherBase):

    pass





class LandedCostVoucherUpdate(InputSchema):

    """A partial update."""



    naming_series: Optional[LandedCostVoucherNamingSeries] = None

    company: Optional[str] = None

    total_taxes_and_charges: Optional[Decimal] = None

    distribute_charges_based_on: Optional[LandedCostVoucherDistributeChargesBasedOn] = None

    amended_from_id: Optional[uuid.UUID] = None

    posting_date: Optional[dt.date] = None

    total_vendor_invoices_cost: Optional[Decimal] = None

    purchase_receipts: Optional[list[LandedCostPurchaseReceiptCreate]] = None

    items: Optional[list[LandedCostItemCreate]] = None

    taxes: Optional[list[LandedCostTaxesAndChargesCreate]] = None

    vendor_invoices: Optional[list[LandedCostVendorInvoiceCreate]] = None





class LandedCostVoucherRead(ReadSchema):

    id: uuid.UUID

    name: str

    naming_series: Optional[LandedCostVoucherNamingSeries] = None

    company: str

    total_taxes_and_charges: Optional[Decimal] = None

    distribute_charges_based_on: Optional[LandedCostVoucherDistributeChargesBasedOn] = None

    amended_from_id: Optional[uuid.UUID] = None

    posting_date: Optional[dt.date] = None

    total_vendor_invoices_cost: Optional[Decimal] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0

    purchase_receipts: list[LandedCostPurchaseReceiptRead] = []

    items: list[LandedCostItemRead] = []

    taxes: list[LandedCostTaxesAndChargesRead] = []

    vendor_invoices: list[LandedCostVendorInvoiceRead] = []





LandedCostVoucherListResponse = Page[LandedCostVoucherRead]
