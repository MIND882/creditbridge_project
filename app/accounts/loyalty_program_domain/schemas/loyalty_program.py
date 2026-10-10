"""Pydantic v2 schemas for LoyaltyProgram."""





from __future__ import annotations

from app.accounts.loyalty_program_domain.models.loyalty_program import (

    LoyaltyProgramLoyaltyProgramType,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.loyalty_program_collection_domain.schemas.loyalty_program_collection import (

    LoyaltyProgramCollectionCreate,

    LoyaltyProgramCollectionRead,

)



__all__ = [

    "LoyaltyProgramCreate",

    "LoyaltyProgramUpdate",

    "LoyaltyProgramRead",

    "LoyaltyProgramListResponse",

]





class LoyaltyProgramBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    loyalty_program_name: str

    loyalty_program_type: Optional[LoyaltyProgramLoyaltyProgramType] = None

    from_date: dt.date

    to_date: Optional[dt.date] = None

    customer_group: Optional[str] = None

    customer_territory: Optional[str] = None

    auto_opt_in: Optional[bool] = None

    conversion_factor: Optional[Decimal] = None

    expiry_duration: Optional[int] = None

    expense_account_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    project: Optional[str] = None



    collection_rules: list[LoyaltyProgramCollectionCreate] = []





class LoyaltyProgramCreate(LoyaltyProgramBase):

    pass





class LoyaltyProgramUpdate(InputSchema):

    """A partial update."""



    loyalty_program_name: Optional[str] = None

    loyalty_program_type: Optional[LoyaltyProgramLoyaltyProgramType] = None

    from_date: Optional[dt.date] = None

    to_date: Optional[dt.date] = None

    customer_group: Optional[str] = None

    customer_territory: Optional[str] = None

    auto_opt_in: Optional[bool] = None

    conversion_factor: Optional[Decimal] = None

    expiry_duration: Optional[int] = None

    expense_account_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    collection_rules: Optional[list[LoyaltyProgramCollectionCreate]] = None





class LoyaltyProgramRead(ReadSchema):

    id: uuid.UUID

    name: str

    loyalty_program_name: str

    loyalty_program_type: Optional[LoyaltyProgramLoyaltyProgramType] = None

    from_date: dt.date

    to_date: Optional[dt.date] = None

    customer_group: Optional[str] = None

    customer_territory: Optional[str] = None

    auto_opt_in: bool

    conversion_factor: Optional[Decimal] = None

    expiry_duration: Optional[int] = None

    expense_account_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    collection_rules: list[LoyaltyProgramCollectionRead] = []





LoyaltyProgramListResponse = Page[LoyaltyProgramRead]
