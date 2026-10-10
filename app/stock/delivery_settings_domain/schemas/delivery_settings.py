"""Pydantic v2 schemas for DeliverySettings."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "DeliverySettingsUpdate",

    "DeliverySettingsRead",

]





class DeliverySettingsUpdate(InputSchema):

    """A partial update of the tenant settings row."""



    dispatch_template: Optional[str] = None

    dispatch_attachment: Optional[str] = None

    send_with_attachment: Optional[bool] = None

    stop_delay: Optional[int] = None





class DeliverySettingsRead(ReadSchema):

    id: uuid.UUID

    dispatch_template: Optional[str] = None

    dispatch_attachment: Optional[str] = None

    send_with_attachment: Optional[bool] = None

    stop_delay: Optional[int] = None


