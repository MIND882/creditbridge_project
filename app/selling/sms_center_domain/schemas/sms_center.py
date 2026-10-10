"""Pydantic v2 schemas for SmsCenter."""





from __future__ import annotations

from app.selling.sms_center_domain.models.sms_center import (

    SmsCenterSendTo,

)

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SmsCenterUpdate",

    "SmsCenterRead",

]





class SmsCenterUpdate(InputSchema):

    """A partial update of the tenant settings row."""



    send_to: Optional[SmsCenterSendTo] = None

    customer_id: Optional[uuid.UUID] = None

    supplier_id: Optional[uuid.UUID] = None

    sales_partner: Optional[str] = None

    department: Optional[str] = None

    branch: Optional[str] = None

    receiver_list: Optional[str] = None

    message: Optional[str] = None

    total_characters: Optional[int] = None

    total_messages: Optional[int] = None





class SmsCenterRead(ReadSchema):

    id: uuid.UUID

    send_to: Optional[SmsCenterSendTo] = None

    customer_id: Optional[uuid.UUID] = None

    supplier_id: Optional[uuid.UUID] = None

    sales_partner: Optional[str] = None

    department: Optional[str] = None

    branch: Optional[str] = None

    receiver_list: Optional[str] = None

    message: Optional[str] = None

    total_characters: Optional[int] = None

    total_messages: Optional[int] = None


