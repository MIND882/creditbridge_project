"""

Tax Rule -- converted from ``erpnext/accounts/doctype/tax_rule``.



Picks a tax template from the shape of a transaction: which party, which item,

where it is billed and shipped. ``autoname`` is ``ACC-TAX-RULE-.YYYY.-.#####``.



Upstream's ``validate_tax_template`` blanks out the half of the rule that does

not apply -- a Sales rule must not carry a supplier -- and that clearing is part

of the ported behaviour, not just a UI convenience.

"""



from __future__ import annotations



import uuid

from datetime import date

from typing import Optional



from sqlalchemy import Boolean, Date, ForeignKey, Integer, String, UniqueConstraint

from sqlalchemy import Enum as SAEnum

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.tax_enums import TaxRuleType

from app.core.base_model import TenantModel, tenant_index



__all__ = ["TaxRule", "NAMING_SERIES"]



NAMING_SERIES = "ACC-TAX-RULE-.YYYY.-"





class TaxRule(TenantModel):

    __tablename__ = "tax_rules"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_tax_rule_business_name"),

        # The conflict check matches on tax_type and every filter column.

        tenant_index("ix_tax_rule_tax_type", "tax_type"),

    )



    name: Mapped[str] = mapped_column(String(255), nullable=False)



    tax_type: Mapped[Optional[TaxRuleType]] = mapped_column(

        SAEnum(TaxRuleType, name="tax_rule_type"), default=TaxRuleType.SALES, nullable=True

    )

    use_for_shopping_cart: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=True

    )



    sales_tax_template_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("sales_taxes_and_charges_templates.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    sales_tax_template = relationship(

        "SalesTaxesAndChargesTemplate", foreign_keys=[sales_tax_template_id]

    )



    purchase_tax_template_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("purchase_taxes_and_charges_templates.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    purchase_tax_template = relationship(

        "PurchaseTaxesAndChargesTemplate", foreign_keys=[purchase_tax_template_id]

    )



    tax_category_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("tax_categories.id", ondelete="RESTRICT"), nullable=True, index=True

    )

    tax_category = relationship("TaxCategory", foreign_keys=[tax_category_id])



    # Customer / Supplier / Item / Country / the two group doctypes are not

    # converted, so these Links stay as plain strings.

    customer: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    supplier: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    customer_group: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    supplier_group: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    item_group: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    billing_city: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    billing_county: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    billing_state: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    billing_zipcode: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    billing_country: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    shipping_city: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    shipping_county: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    shipping_state: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    shipping_zipcode: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    shipping_country: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    from_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    to_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)



    #: Ties are a conflict: two rules matching at the same priority are

    #: ambiguous, which is what ``validate_filters`` rejects.

    priority: Mapped[Optional[int]] = mapped_column(Integer, default=1, nullable=True)



    def __repr__(self) -> str:

        return f"<TaxRule id={self.id} name={self.name!r} type={self.tax_type!r}>"
