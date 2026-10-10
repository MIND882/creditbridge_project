"""

Party Specific Item -- converted from ``erpnext/selling/doctype/party_specific_item``.

"""



from __future__ import annotations



import enum

from typing import Optional

import uuid



from sqlalchemy import Enum as SAEnum, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["PartySpecificItem", "PartySpecificItemPartyType", "PartySpecificItemRestrictBasedOn"]





class PartySpecificItemPartyType(str, enum.Enum):

    CUSTOMER = "Customer"

    CUSTOMER_GROUP = "Customer Group"

    SUPPLIER = "Supplier"

    SUPPLIER_GROUP = "Supplier Group"



class PartySpecificItemRestrictBasedOn(str, enum.Enum):

    ITEM = "Item"

    ITEM_GROUP = "Item Group"

    BRAND = "Brand"





class PartySpecificItem(TenantModel):

    __tablename__ = "party_specific_items"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_party_specific_items_business_name"),

    )



    #: Upstream declares no ``autoname``; Frappe mints a hash.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    party_type: Mapped[str] = mapped_column(SAEnum(PartySpecificItemPartyType, values_callable=lambda x: [e.value for e in x], native_enum=False, length=18, validate_strings=True), nullable=False)

    party: Mapped[str] = mapped_column(String(140), nullable=False)

    restrict_based_on: Mapped[str] = mapped_column(SAEnum(PartySpecificItemRestrictBasedOn, values_callable=lambda x: [e.value for e in x], native_enum=False, length=14, validate_strings=True), nullable=False)

    based_on_value: Mapped[str] = mapped_column(String(140), nullable=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PartySpecificItem id={self.id}>"
