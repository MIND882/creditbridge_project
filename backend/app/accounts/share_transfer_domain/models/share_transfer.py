"""

Share Transfer -- converted from ``erpnext/accounts/doctype/share_transfer``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Date, Enum as SAEnum, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.account_domain.models.account import Account  # noqa: F401

from app.accounts.share_type_domain.models.share_type import ShareType  # noqa: F401

from app.accounts.shareholder_domain.models.shareholder import Shareholder  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["ShareTransfer", "ShareTransferTransferType"]







class ShareTransferTransferType(str, enum.Enum):

    ISSUE = "Issue"

    PURCHASE = "Purchase"

    TRANSFER = "Transfer"









class ShareTransfer(SubmittableModel, TenantModel):

    __tablename__ = "share_transfers"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_share_transfers_business_name"),

    )



    #: ``autoname`` = 'ACC-SHT-.YYYY.-.#####'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    transfer_type: Mapped[ShareTransferTransferType] = mapped_column(

        SAEnum(ShareTransferTransferType, native_enum=False, length=8, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=False,

    )

    date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    from_shareholder_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("shareholders.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    from_shareholder = relationship("Shareholder", foreign_keys=[from_shareholder_id])

    from_folio_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    equity_or_liability_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    equity_or_liability_account = relationship("Account", foreign_keys=[equity_or_liability_account_id])

    asset_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    asset_account = relationship("Account", foreign_keys=[asset_account_id])

    to_shareholder_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("shareholders.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    to_shareholder = relationship("Shareholder", foreign_keys=[to_shareholder_id])

    to_folio_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    share_type_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("share_types.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    share_type = relationship("ShareType", foreign_keys=[share_type_id])

    from_no: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    rate: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    no_of_shares: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    to_no: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    remarks: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    amended_from: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ShareTransfer id={self.id}>"
