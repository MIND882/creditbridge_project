"""

Supplier -- converted from ``erpnext/buying/doctype/supplier``.

"""



from __future__ import annotations



import datetime as dt

import enum

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, Enum as SAEnum, ForeignKey, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.buying.customer_number_at_supplier_domain.models.customer_number_at_supplier import CustomerNumberAtSupplier



from app.core.base_model import TenantModel



__all__ = ["Supplier", "SupplierNamingSeries", "SupplierSupplierType", "SupplierHoldType"]





class SupplierNamingSeries(str, enum.Enum):

    SUP_YYYY = "SUP-.YYYY.-"



class SupplierSupplierType(str, enum.Enum):

    COMPANY = "Company"

    INDIVIDUAL = "Individual"

    PARTNERSHIP = "Partnership"



class SupplierHoldType(str, enum.Enum):

    ALL = "All"

    INVOICES = "Invoices"

    PAYMENTS = "Payments"





class Supplier(TenantModel):

    __tablename__ = "suppliers"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_suppliers_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    naming_series: Mapped[Optional[str]] = mapped_column(SAEnum(SupplierNamingSeries, native_enum=False, length=15, validate_strings=True), nullable=True)

    supplier_name: Mapped[str] = mapped_column(String(140), nullable=False)

    country: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    default_bank_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("acc_bank_accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    default_bank_account = relationship("app.accounts.bank_account_domain.models.bank_account.BankAccount", foreign_keys=[default_bank_account_id])

    tax_id: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    tax_category_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("tax_categories.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    tax_category = relationship("app.accounts.tax_category_domain.models.tax_category.TaxCategory", foreign_keys=[tax_category_id])

    tax_withholding_category_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("tax_withholding_categories.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    tax_withholding_category = relationship("app.accounts.tax_withholding_category_domain.models.tax_withholding_category.TaxWithholdingCategory", foreign_keys=[tax_withholding_category_id])

    is_transporter: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    is_internal_supplier: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    represents_company: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    image: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    supplier_group: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    supplier_type: Mapped[str] = mapped_column(SAEnum(SupplierSupplierType, native_enum=False, length=15, validate_strings=True), nullable=False)

    language: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    warn_rfqs: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    warn_pos: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    prevent_rfqs: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    prevent_pos: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    default_currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    default_price_list_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("price_lists.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    default_price_list = relationship("app.stock.price_list_domain.models.price_list.PriceList", foreign_keys=[default_price_list_id])

    payment_terms_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("payment_terms_templates.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    payment_terms = relationship("app.accounts.payment_terms_template_domain.models.payment_terms_template.PaymentTermsTemplate", foreign_keys=[payment_terms_id])

    on_hold: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    hold_type: Mapped[Optional[str]] = mapped_column(SAEnum(SupplierHoldType, native_enum=False, length=12, validate_strings=True), nullable=True)

    release_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    website: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    supplier_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    is_frozen: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    allow_purchase_invoice_creation_without_purchase_order: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    allow_purchase_invoice_creation_without_purchase_receipt: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    supplier_primary_contact: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    mobile_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    email_id: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    primary_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    supplier_primary_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    restrict_to_companies: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    tax_withholding_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("tax_withholding_groups.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    tax_withholding_group = relationship("app.accounts.tax_withholding_group_domain.models.tax_withholding_group.TaxWithholdingGroup", foreign_keys=[tax_withholding_group_id])

    gender: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    alias: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    customer_numbers: Mapped[list["CustomerNumberAtSupplier"]] = relationship(  # noqa: F821

        "CustomerNumberAtSupplier",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[CustomerNumberAtSupplier.parent_id]",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<Supplier id={self.id}>"
