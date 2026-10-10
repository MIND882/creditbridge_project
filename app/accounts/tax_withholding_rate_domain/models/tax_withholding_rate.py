"""

TaxWithholdingRate -- converted from

``erpnext/accounts/doctype/tax_withholding_rate``.



One row of ``TaxWithholdingCategory.rates``: the rate that applies over a date

window, plus the two thresholds that decide whether it bites at all.



Rows only ever exist inside a category, so the API is read-only.

"""



from __future__ import annotations



import uuid

from datetime import date

from decimal import Decimal

from typing import Optional



from sqlalchemy import Date, ForeignKey, Numeric, String

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["TaxWithholdingRate"]





class TaxWithholdingRate(ChildTableModel, TenantModel):

    """One row of ``TaxWithholdingCategory.rates``."""



    __tablename__ = "tax_withholding_rates"



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("tax_withholding_categories.id", ondelete="CASCADE"), nullable=True, index=True

    )



    tax_withholding_rate: Mapped[Optional[Decimal]] = mapped_column(

        Numeric(21, 9), nullable=False

    )



    #: Below this, a single transaction is not withheld.

    single_threshold: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    #: Below this, the running total is not withheld.

    cumulative_threshold: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    #: Both required upstream, and both drive ``get_applicable_tax_row``.

    from_date: Mapped[date] = mapped_column(Date, nullable=False)

    to_date: Mapped[date] = mapped_column(Date, nullable=False)



    #: Tax Withholding Group is its own doctype and is not converted.

    tax_withholding_group: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<TaxWithholdingRate id={self.id} idx={self.idx} rate={self.tax_withholding_rate}>"
