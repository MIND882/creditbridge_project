"""

ItemTaxTemplateDetail -- converted from

``erpnext/accounts/doctype/item_tax_template_detail``.



One row of ``ItemTaxTemplate.taxes``: a tax account and the rate to apply when

an item uses this template.



``not_applicable`` marks a tax that the item is exempt from; upstream forces its

rate to zero rather than deleting the row, so the exemption stays visible.



Rows only ever exist inside a template, so the API is read-only.

"""



from __future__ import annotations



import uuid

from decimal import Decimal

from typing import Optional



from sqlalchemy import Boolean, ForeignKey, Numeric

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["ItemTaxTemplateDetail"]





class ItemTaxTemplateDetail(ChildTableModel, TenantModel):

    """One row of ``ItemTaxTemplate.taxes``."""



    __tablename__ = "item_tax_template_details"



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("item_tax_templates.id", ondelete="CASCADE"), nullable=True, index=True

    )

    parent = relationship("ItemTaxTemplate", back_populates="taxes", foreign_keys=[parent_id])



    #: Must be an account of type Tax / Chargeable / Income / Expense.

    tax_type_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"), nullable=False, index=True

    )

    tax_type = relationship("Account", foreign_keys=[tax_type_id])



    tax_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    #: Forced to a zero rate on write; see ``set_zero_rate_for_not_applicable_tax``.

    not_applicable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ItemTaxTemplateDetail id={self.id} idx={self.idx}>"
