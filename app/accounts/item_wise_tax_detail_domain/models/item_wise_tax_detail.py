"""

ItemWiseTaxDetail -- converted from

``erpnext/accounts/doctype/item_wise_tax_detail``.



The tax breakdown behind a posted transaction: for each (item row, tax row)

pair, the rate applied and the amount charged. Written by the invoice when it

submits, and read by the tax reports.



**Orphan child table.** Upstream's parents are Sales Invoice and Purchase

Invoice, neither of which is converted, so there is no ``parent_id`` here.

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional



from sqlalchemy import Numeric, String

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel, tenant_index



__all__ = ["ItemWiseTaxDetail"]





class ItemWiseTaxDetail(TenantModel):

    __tablename__ = "item_wise_tax_details"

    __table_args__ = (tenant_index("ix_item_wise_tax_detail_item_row", "item_row"),)



    #: Row ids of the source document, kept as strings because the parents are

    #: not converted and so cannot be real FKs yet.

    item_row: Mapped[str] = mapped_column(String(140), nullable=False)

    tax_row: Mapped[str] = mapped_column(String(140), nullable=False)



    rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    taxable_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    def __repr__(self) -> str:

        return (

            f"<ItemWiseTaxDetail id={self.id} item={self.item_row!r} "

            f"tax={self.tax_row!r} amount={self.amount}>"

        )
