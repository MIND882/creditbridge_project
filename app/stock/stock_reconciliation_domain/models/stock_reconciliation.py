"""

Stock Reconciliation -- converted from ``erpnext/stock/doctype/stock_reconciliation``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, Enum as SAEnum, ForeignKey, Numeric, String, Time, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.stock.stock_reconciliation_item_domain.models.stock_reconciliation_item import StockReconciliationItem



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["StockReconciliation", "StockReconciliationNamingSeries", "StockReconciliationPurpose"]





class StockReconciliationNamingSeries(str, enum.Enum):

    MAT_RECO_YYYY = "MAT-RECO-.YYYY.-"



class StockReconciliationPurpose(str, enum.Enum):

    OPENING_STOCK = "Opening Stock"

    STOCK_RECONCILIATION = "Stock Reconciliation"





class StockReconciliation(SubmittableModel, TenantModel):

    __tablename__ = "stock_reconciliations"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_stock_reconciliations_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    naming_series: Mapped[str] = mapped_column(SAEnum(StockReconciliationNamingSeries, native_enum=False, length=20, validate_strings=True), nullable=False)

    company: Mapped[str] = mapped_column(String(140), nullable=False)

    purpose: Mapped[str] = mapped_column(SAEnum(StockReconciliationPurpose, native_enum=False, length=24, validate_strings=True), nullable=False)

    posting_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    posting_time: Mapped[dt.time] = mapped_column(Time, nullable=False)

    set_posting_time: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    expense_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    expense_account = relationship("Account", foreign_keys=[expense_account_id])

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])

    difference_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("stock_reconciliations.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("StockReconciliation", foreign_keys=[amended_from_id])

    scan_barcode: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    scan_mode: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    set_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    set_warehouse = relationship("Warehouse", foreign_keys=[set_warehouse_id])

    last_scanned_warehouse: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    items: Mapped[list["StockReconciliationItem"]] = relationship(  # noqa: F821

        "StockReconciliationItem",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[StockReconciliationItem.parent_id]",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<StockReconciliation id={self.id}>"
