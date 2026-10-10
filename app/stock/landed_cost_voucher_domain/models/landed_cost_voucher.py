"""

Landed Cost Voucher -- converted from ``erpnext/stock/doctype/landed_cost_voucher``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Date, Enum as SAEnum, ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.stock.landed_cost_purchase_receipt_domain.models.landed_cost_purchase_receipt import LandedCostPurchaseReceipt

from app.stock.landed_cost_item_domain.models.landed_cost_item import LandedCostItem

from app.stock.landed_cost_taxes_and_charges_domain.models.landed_cost_taxes_and_charges import LandedCostTaxesAndCharges

from app.stock.landed_cost_vendor_invoice_domain.models.landed_cost_vendor_invoice import LandedCostVendorInvoice



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["LandedCostVoucher", "LandedCostVoucherNamingSeries", "LandedCostVoucherDistributeChargesBasedOn"]





class LandedCostVoucherNamingSeries(str, enum.Enum):

    MAT_LCV_YYYY = "MAT-LCV-.YYYY.-"



class LandedCostVoucherDistributeChargesBasedOn(str, enum.Enum):

    QTY = "Qty"

    AMOUNT = "Amount"

    DISTRIBUTE_MANUALLY = "Distribute Manually"





class LandedCostVoucher(SubmittableModel, TenantModel):

    __tablename__ = "landed_cost_vouchers"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_landed_cost_vouchers_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    naming_series: Mapped[str] = mapped_column(SAEnum(LandedCostVoucherNamingSeries, native_enum=False, length=19, validate_strings=True), nullable=False)

    company: Mapped[str] = mapped_column(String(140), nullable=False)

    total_taxes_and_charges: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    distribute_charges_based_on: Mapped[str] = mapped_column(SAEnum(LandedCostVoucherDistributeChargesBasedOn, native_enum=False, length=23, validate_strings=True), nullable=False)

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("landed_cost_vouchers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("LandedCostVoucher", foreign_keys=[amended_from_id])

    posting_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    total_vendor_invoices_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    purchase_receipts: Mapped[list["LandedCostPurchaseReceipt"]] = relationship(  # noqa: F821

        "LandedCostPurchaseReceipt",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[LandedCostPurchaseReceipt.parent_id]",

    )



    items: Mapped[list["LandedCostItem"]] = relationship(  # noqa: F821

        "LandedCostItem",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[LandedCostItem.parent_id]",

    )



    taxes: Mapped[list["LandedCostTaxesAndCharges"]] = relationship(  # noqa: F821

        "LandedCostTaxesAndCharges",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[LandedCostTaxesAndCharges.parent_id]",

    )



    vendor_invoices: Mapped[list["LandedCostVendorInvoice"]] = relationship(  # noqa: F821

        "LandedCostVendorInvoice",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[LandedCostVendorInvoice.parent_id]",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<LandedCostVoucher id={self.id}>"
