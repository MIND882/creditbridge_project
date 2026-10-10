"""

Accounting Dimension -- converted from

``erpnext/accounts/doctype/accounting_dimension``.



An accounting dimension is an *extra* analysis axis on transactions (Branch,

Department, Territory...) beyond the chart of accounts. Upstream it is unusual:

``document_type`` is a Link to a **DocType**, and creating one causes Frappe to

add a real custom field to the transaction doctypes at runtime.



That runtime-schema behaviour has no equivalent here and is deliberately not

faked. What is preserved:



* the dimension registry itself (label, fieldname, source doctype, defaults);

* the ``fieldname`` derivation from ``label``;

* the mandatory-name rule that ``autoname: field:label`` implies.



TODO(accounts-conversion): upstream's ``create_custom_fields`` /

``delete_custom_fields`` mutate the target doctype's schema. Port this when the

transaction doctypes (Sales Invoice, Journal Entry...) are converted -- the hook

point is :meth:`AccountingDimensionService.sync_custom_fields`.

"""



from __future__ import annotations



import re

import uuid

from typing import Optional



from sqlalchemy import Boolean, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel



__all__ = ["AccountingDimension", "make_fieldname"]





def make_fieldname(label: str) -> str:

    """

    Port of the fieldname derivation in ``accounting_dimension.py``.



    Lowercases, replaces runs of non-alphanumerics with a single underscore,

    and strips leading/trailing underscores -- the same normalisation Frappe

    applies when generating a custom field from a label.

    """

    slug = re.sub(r"[^a-z0-9]+", "_", (label or "").strip().lower()).strip("_")

    return slug or "dimension"





class AccountingDimension(TenantModel):

    """A registered extra analysis axis for transactions."""



    __tablename__ = "accounting_dimensions"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_accounting_dimensions_business_id_name"),

        UniqueConstraint(

            "business_id", "fieldname", name="uq_accounting_dimensions_business_fieldname"

        ),

    )



    #: ``autoname: field:label``.

    name: Mapped[str] = mapped_column(String(140), nullable=False)

    label: Mapped[str] = mapped_column(String(140), nullable=False)



    #: Derived from ``label`` unless explicitly overridden.

    fieldname: Mapped[str] = mapped_column(String(140), nullable=False)



    #: The doctype whose records provide this dimension's values. Stored as a

    #: label; no DocType registry exists in this conversion.

    document_type: Mapped[str] = mapped_column(String(140), nullable=False)



    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    dimension_defaults: Mapped[list["AccountingDimensionDetail"]] = relationship(  # noqa: F821

        "AccountingDimensionDetail",

        back_populates="parent",

        cascade="all, delete-orphan",

        passive_deletes=True,

        order_by="AccountingDimensionDetail.idx",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<AccountingDimension id={self.id} name={self.name!r}>"
