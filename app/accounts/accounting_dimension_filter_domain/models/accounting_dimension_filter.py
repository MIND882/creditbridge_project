"""

Accounting Dimension Filter -- converted from

``erpnext/accounts/doctype/accounting_dimension_filter``.



Restricts which dimension values may be used against which accounts, either as

an allow-list or a deny-list (``allow_or_restrict``).



JSON field                  Type here            Notes

--------------------------  -------------------  -------------------------

accounting_dimension        String(140) reqd     the dimension being filtered

allow_or_restrict           Enum        reqd     Allow / Restrict

accounts                    Table       reqd     -> ApplicableOnAccount

dimensions                  Table                -> AllowedDimension

apply_restriction_on_values Boolean

disabled                    Boolean

company                     *collapsed*          -> business_id

fieldname                   String(140)



``autoname`` is ``format:{accounting_dimension}-{#####}`` -- a per-dimension

counter, scoped per tenant.



The ``dimension_filter_help`` HTML field is a UI-only explainer and is not

carried over.

"""



from __future__ import annotations



import enum

import uuid

from typing import Optional



from sqlalchemy import Boolean, String, UniqueConstraint

from sqlalchemy import Enum as SAEnum

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel, tenant_index



__all__ = ["AccountingDimensionFilter", "AllowOrRestrict"]





class AllowOrRestrict(str, enum.Enum):

    """``allow_or_restrict`` Select -- the polarity of the filter."""



    ALLOW = "Allow"

    RESTRICT = "Restrict"





class AccountingDimensionFilter(TenantModel):

    """An allow/deny rule binding dimension values to accounts."""



    __tablename__ = "accounting_dimension_filters"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_adf_business_id_name"),

        tenant_index("ix_adf_business_dimension", "accounting_dimension"),

    )



    #: ``{accounting_dimension}-{#####}``, counter scoped per tenant.

    name: Mapped[str] = mapped_column(String(200), nullable=False)



    #: Label of the AccountingDimension this filter applies to.

    accounting_dimension: Mapped[str] = mapped_column(String(140), nullable=False)

    fieldname: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    allow_or_restrict: Mapped[AllowOrRestrict] = mapped_column(

        SAEnum(AllowOrRestrict, native_enum=False, length=10, validate_strings=True),

        nullable=False,

    )



    apply_restriction_on_values: Mapped[bool] = mapped_column(

        Boolean, nullable=False, default=False

    )

    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    accounts: Mapped[list["ApplicableOnAccount"]] = relationship(  # noqa: F821

        "ApplicableOnAccount",

        back_populates="parent",

        cascade="all, delete-orphan",

        passive_deletes=True,

        order_by="ApplicableOnAccount.idx",

    )

    dimensions: Mapped[list["AllowedDimension"]] = relationship(  # noqa: F821

        "AllowedDimension",

        back_populates="parent",

        cascade="all, delete-orphan",

        passive_deletes=True,

        order_by="AllowedDimension.idx",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<AccountingDimensionFilter id={self.id} name={self.name!r}>"
