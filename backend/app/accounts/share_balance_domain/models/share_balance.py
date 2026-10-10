"""

Share Balance -- converted from ``erpnext/accounts/doctype/share_balance``.



A Frappe child table (``istable: 1``): one holding of a shareholder -- a run of

certificate numbers, how many shares, at what rate, and the resulting amount.



Upstream the controller is empty. The only logic touching these rows is

``Shareholder.before_save``, which recomputes ``amount`` as

``no_of_shares * rate``; that is ported on the parent.



``current_state`` is upstream a Select whose options are the empty string,

``Issued`` and ``Purchased``. The empty option is modelled as ``None`` here

rather than as a member of the enum, so "not yet set" and "issued" stay

distinguishable.

"""



from __future__ import annotations



import enum

import uuid

from decimal import Decimal

from typing import Optional



from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String

from sqlalchemy import Enum as SAEnum

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["ShareBalance", "ShareCurrentState"]





class ShareCurrentState(str, enum.Enum):

    ISSUED = "Issued"

    PURCHASED = "Purchased"





class ShareBalance(ChildTableModel, TenantModel):

    """One row of ``Shareholder.share_balance``."""



    __tablename__ = "share_balances"



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("shareholders.id", ondelete="CASCADE"), nullable=True, index=True

    )

    parent = relationship(

        "Shareholder", back_populates="share_balance", foreign_keys=[parent_id]

    )



    share_type_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("share_types.id", ondelete="RESTRICT"), nullable=False, index=True

    )

    share_type = relationship("ShareType", foreign_keys=[share_type_id])



    #: Certificate number range, inclusive at both ends.

    from_no: Mapped[int] = mapped_column(Integer, nullable=False)

    to_no: Mapped[int] = mapped_column(Integer, nullable=False)



    rate: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False)

    no_of_shares: Mapped[int] = mapped_column(Integer, nullable=False)



    #: Recomputed as ``no_of_shares * rate`` by ``ShareholderService``.

    amount: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False)



    is_company: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    current_state: Mapped[Optional[ShareCurrentState]] = mapped_column(

        SAEnum(ShareCurrentState, native_enum=False, length=10, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ShareBalance id={self.id} idx={self.idx} shares={self.no_of_shares}>"
