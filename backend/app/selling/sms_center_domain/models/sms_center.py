"""

SMS Center -- converted from ``erpnext/selling/doctype/sms_center``.



A Frappe Single (``issingle: 1``): one row per ``business_id``, enforced by a unique constraint on ``business_id`` alone.

"""



from __future__ import annotations



import enum

from typing import Optional

import uuid



from sqlalchemy import Enum as SAEnum, ForeignKey, Integer, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel



__all__ = ["SmsCenter", "SmsCenterSendTo"]





class SmsCenterSendTo(str, enum.Enum):

    ALL_CONTACT = "All Contact"

    ALL_CUSTOMER_CONTACT = "All Customer Contact"

    ALL_SUPPLIER_CONTACT = "All Supplier Contact"

    ALL_SALES_PARTNER_CONTACT = "All Sales Partner Contact"

    ALL_LEAD_OPEN = "All Lead (Open)"

    ALL_EMPLOYEE_ACTIVE = "All Employee (Active)"

    ALL_SALES_PERSON = "All Sales Person"





class SmsCenter(TenantModel):

    __tablename__ = "sms_centers"

    __table_args__ = (

        UniqueConstraint("business_id", name="uq_sms_centers_business"),

    )



    send_to: Mapped[Optional[str]] = mapped_column(SAEnum(SmsCenterSendTo, values_callable=lambda x: [e.value for e in x], native_enum=False, length=29, validate_strings=True), nullable=True)

    customer_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("selling_customers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    customer = relationship("app.selling.customer_domain.models.customer.Customer", foreign_keys=[customer_id])

    supplier_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("suppliers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    supplier = relationship("app.buying.supplier_domain.models.supplier.Supplier", foreign_keys=[supplier_id])

    sales_partner: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    department: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    branch: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    receiver_list: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    total_characters: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    total_messages: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SmsCenter id={self.id}>"
