"""

Packing Slip -- converted from ``erpnext/stock/doctype/packing_slip``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Enum as SAEnum, ForeignKey, Integer, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.stock.packing_slip_item_domain.models.packing_slip_item import PackingSlipItem



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["PackingSlip", "PackingSlipNamingSeries"]





class PackingSlipNamingSeries(str, enum.Enum):

    MAT_PAC_YYYY = "MAT-PAC-.YYYY.-"





class PackingSlip(SubmittableModel, TenantModel):

    __tablename__ = "packing_slips"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_packing_slips_business_name"),

    )



    #: ``autoname`` = 'MAT-PAC-.YYYY.-.#####'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    delivery_note_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("delivery_notes.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    delivery_note = relationship("DeliveryNote", foreign_keys=[delivery_note_id])

    naming_series: Mapped[str] = mapped_column(SAEnum(PackingSlipNamingSeries, native_enum=False, length=19, validate_strings=True), nullable=False)

    from_case_no: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    to_case_no: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    net_weight_pkg: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    net_weight_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    net_weight_uom = relationship("Uom", foreign_keys=[net_weight_uom_id])

    gross_weight_pkg: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    gross_weight_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    gross_weight_uom = relationship("Uom", foreign_keys=[gross_weight_uom_id])

    letter_head: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("packing_slips.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("PackingSlip", foreign_keys=[amended_from_id])



    items: Mapped[list["PackingSlipItem"]] = relationship(  # noqa: F821

        "PackingSlipItem",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[PackingSlipItem.parent_id]",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PackingSlip id={self.id}>"
