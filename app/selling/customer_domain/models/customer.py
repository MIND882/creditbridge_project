"""

Customer -- converted from ``erpnext/selling/doctype/customer``.

"""



from __future__ import annotations



import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, ForeignKey, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.selling.customer_credit_limit_domain.models.customer_credit_limit import CustomerCreditLimit

from app.selling.sales_team_domain.models.sales_team import SalesTeam

from app.selling.supplier_number_at_customer_domain.models.supplier_number_at_customer import SupplierNumberAtCustomer



from app.core.base_model import TenantModel



__all__ = ["Customer", "CustomerNamingSeries", "CustomerCustomerType"]





class CustomerNamingSeries(str, enum.Enum):

    CUST_YYYY = "CUST-.YYYY.-"



class CustomerCustomerType(str, enum.Enum):

    COMPANY = "Company"

    INDIVIDUAL = "Individual"

    PARTNERSHIP = "Partnership"





class Customer(TenantModel):

    __tablename__ = "selling_customers"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_selling_customers_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    naming_series: Mapped[Optional[str]] = mapped_column(SAEnum(CustomerNamingSeries, native_enum=False, length=16, validate_strings=True), nullable=True)

    customer_name: Mapped[str] = mapped_column(String(140), nullable=False)

    alias: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    customer_type: Mapped[str] = mapped_column(SAEnum(CustomerCustomerType, values_callable=lambda x: [e.value for e in x], native_enum=False, length=15, validate_strings=True), nullable=False)

    gender: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    customer_group: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    territory: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    image: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    default_currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    default_bank_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("acc_bank_accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    default_bank_account = relationship("app.accounts.bank_account_domain.models.bank_account.BankAccount", foreign_keys=[default_bank_account_id])

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

    loyalty_program_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("loyalty_programs.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    loyalty_program = relationship("app.accounts.loyalty_program_domain.models.loyalty_program.LoyaltyProgram", foreign_keys=[loyalty_program_id])

    loyalty_program_tier: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    customer_primary_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    primary_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    customer_primary_contact: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    mobile_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    email_id: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    first_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    last_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_internal_customer: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    represents_company: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    tax_id: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    tax_category_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("tax_categories.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    tax_category = relationship("app.accounts.tax_category_domain.models.tax_category.TaxCategory", foreign_keys=[tax_category_id])

    tax_withholding_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("tax_withholding_groups.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    tax_withholding_group = relationship("app.accounts.tax_withholding_group_domain.models.tax_withholding_group.TaxWithholdingGroup", foreign_keys=[tax_withholding_group_id])

    tax_withholding_category_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("tax_withholding_categories.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    tax_withholding_category = relationship("app.accounts.tax_withholding_category_domain.models.tax_withholding_category.TaxWithholdingCategory", foreign_keys=[tax_withholding_category_id])

    restrict_to_companies: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    so_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    dn_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    is_frozen: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    account_manager: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    default_sales_partner: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    default_commission_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    lead_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    opportunity_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    prospect_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    market_segment: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    industry_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("industry_types.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    industry = relationship("app.selling.industry_type_domain.models.industry_type.IndustryType", foreign_keys=[industry_id])

    website: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    language: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    customer_pos_id: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    customer_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)



    credit_limits: Mapped[list["CustomerCreditLimit"]] = relationship(  # noqa: F821

        "app.selling.customer_credit_limit_domain.models.customer_credit_limit.CustomerCreditLimit",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys=[CustomerCreditLimit.parent_id],

    )



    sales_team: Mapped[list["SalesTeam"]] = relationship(  # noqa: F821

        "app.selling.sales_team_domain.models.sales_team.SalesTeam",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys=[SalesTeam.parent_id],

    )



    supplier_numbers: Mapped[list["SupplierNumberAtCustomer"]] = relationship(  # noqa: F821

        "app.selling.supplier_number_at_customer_domain.models.supplier_number_at_customer.SupplierNumberAtCustomer",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys=[SupplierNumberAtCustomer.parent_id],

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<Customer id={self.id}>"
