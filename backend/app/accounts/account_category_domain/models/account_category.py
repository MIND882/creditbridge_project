"""

Account Category -- converted from ``erpnext/accounts/doctype/account_category``.



ERPNext models this as a tiny single-table lookup whose ``name`` *is* the

category label. Here the label becomes an explicit ``account_category_name``

column and ``id`` is a UUID, because the whole converted schema keys on UUIDs

and a human label as a primary key cannot survive a rename.



Source fields (account_category.json):



    account_category_name  Data        required

    description            Small Text

    root_type              Select      Asset/Liability/Income/Expense/Equity



The upstream controller's only behaviour is ``after_rename``, which rewrites

``Financial Report Row`` formulas containing the old label. That doctype is not

part of this conversion yet, so the hook is recorded as a TODO on the service

rather than silently dropped.

"""



from __future__ import annotations



from sqlalchemy import String, Text, UniqueConstraint

from sqlalchemy import Enum as SAEnum

from sqlalchemy.orm import Mapped, mapped_column



from app.accounts.enums import RootType

from app.core.base_model import TenantModel

from app.core.base_model import tenant_index



__all__ = ["AccountCategory"]





class AccountCategory(TenantModel):

    """A user-defined grouping label that can pre-set an Account's root type."""



    __tablename__ = "account_categories"

    __table_args__ = (

        # ERPNext enforces this implicitly: the doctype's `name` is the label,

        # and `name` is unique per site. Per-tenant here.

        UniqueConstraint(

            "business_id",

            "account_category_name",

            name="uq_account_categories_business_id_name",

        ),

        tenant_index("ix_account_categories_business_root_type", "root_type"),

    )



    account_category_name: Mapped[str] = mapped_column(String(140), nullable=False)



    #: `Small Text` in ERPNext -- a short free-form note, so Text not String(n).

    description: Mapped[str | None] = mapped_column(Text, nullable=True)



    #: `native_enum=False` renders VARCHAR + a CHECK constraint instead of a

    #: Postgres enum type, which keeps Alembic autogenerate from emitting a

    #: CREATE TYPE (and the awkward migration) every time an option is added.

    root_type: Mapped[RootType | None] = mapped_column(

        SAEnum(RootType, native_enum=False, length=20, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<AccountCategory id={self.id} name={self.account_category_name!r}>"
