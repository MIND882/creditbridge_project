"""

Bisect Accounting Statements -- converted from ``erpnext/accounts/doctype/bisect_accounting_statements``.





"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import DateTime, Enum as SAEnum, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["BisectAccountingStatements", "BisectAccountingStatementsAlgorithm"]







class BisectAccountingStatementsAlgorithm(str, enum.Enum):

    BFS = "BFS"

    DFS = "DFS"









class BisectAccountingStatements(TenantModel):

    __tablename__ = "bisect_accounting_statements"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_bisect_accounting_statements_business_name"),

    )



    #: Upstream declares no ``autoname``; Frappe mints a hash.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    from_date: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)

    to_date: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)

    algorithm: Mapped[Optional[BisectAccountingStatementsAlgorithm]] = mapped_column(

        SAEnum(BisectAccountingStatementsAlgorithm, native_enum=False, length=3, validate_strings=True),

        nullable=True,

    )

    current_node: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    current_from_date: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)

    current_to_date: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)

    p_l_summary: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    b_s_summary: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    difference: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<BisectAccountingStatements id={self.id}>"
