"""

Installation Note -- converted from ``erpnext/selling/doctype/installation_note``.

"""



from __future__ import annotations



import datetime as dt

import enum

from typing import Optional

import uuid



from sqlalchemy import Date, Enum as SAEnum, ForeignKey, String, Text, Time, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.selling.installation_note_item_domain.models.installation_note_item import InstallationNoteItem



from app.core.base_model import TenantModel



__all__ = ["InstallationNote", "InstallationNoteNamingSeries", "InstallationNoteStatus"]





class InstallationNoteNamingSeries(str, enum.Enum):

    MAT_INS_YYYY = "MAT-INS-.YYYY.-"



class InstallationNoteStatus(str, enum.Enum):

    DRAFT = "Draft"

    SUBMITTED = "Submitted"

    CANCELLED = "Cancelled"





class InstallationNote(TenantModel):

    __tablename__ = "installation_notes"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_installation_notes_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    naming_series: Mapped[str] = mapped_column(SAEnum(InstallationNoteNamingSeries,values_callable=lambda x: [e.value for e in x],  native_enum=False, length=19, validate_strings=True), nullable=False)

    customer_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("selling_customers.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    customer = relationship("app.selling.customer_domain.models.customer.Customer", foreign_keys=[customer_id])

    customer_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    contact_person: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    customer_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    address_display: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    contact_display: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    contact_mobile: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    contact_email: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    territory: Mapped[str] = mapped_column(String(140), nullable=False)

    customer_group: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    inst_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    inst_time: Mapped[Optional[dt.time]] = mapped_column(Time, nullable=True)

    status: Mapped[str] = mapped_column(SAEnum(InstallationNoteStatus, native_enum=False, length=13, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=False)

    company: Mapped[str] = mapped_column(String(140), nullable=False)

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("installation_notes.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("app.selling.installation_note_domain.models.installation_note.InstallationNote", foreign_keys=[amended_from_id])

    remarks: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    items: Mapped[list["InstallationNoteItem"]] = relationship(  # noqa: F821

        "app.selling.installation_note_item_domain.models.installation_note_item.InstallationNoteItem",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys=[InstallationNoteItem.parent_id],

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<InstallationNote id={self.id}>"
