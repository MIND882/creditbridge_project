"""Pydantic v2 schemas for SupplierScorecardStanding."""





from __future__ import annotations

from app.buying.supplier_scorecard_standing_domain.models.supplier_scorecard_standing import (

    SupplierScorecardStandingStandingColor,

)

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SupplierScorecardStandingCreate",

    "SupplierScorecardStandingUpdate",

    "SupplierScorecardStandingRead",

    "SupplierScorecardStandingListResponse",

]





class SupplierScorecardStandingBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    standing_name: Optional[str] = None

    standing_color: Optional[SupplierScorecardStandingStandingColor] = None

    min_grade: Optional[Decimal] = None

    max_grade: Optional[Decimal] = None

    warn_rfqs: Optional[bool] = None

    warn_pos: Optional[bool] = None

    prevent_rfqs: Optional[bool] = None

    prevent_pos: Optional[bool] = None

    notify_supplier: Optional[bool] = None

    notify_employee: Optional[bool] = None

    employee_link: Optional[str] = None





class SupplierScorecardStandingCreate(SupplierScorecardStandingBase):

    pass





class SupplierScorecardStandingUpdate(InputSchema):

    """A partial update."""



    standing_name: Optional[str] = None

    standing_color: Optional[SupplierScorecardStandingStandingColor] = None

    min_grade: Optional[Decimal] = None

    max_grade: Optional[Decimal] = None

    warn_rfqs: Optional[bool] = None

    warn_pos: Optional[bool] = None

    prevent_rfqs: Optional[bool] = None

    prevent_pos: Optional[bool] = None

    notify_supplier: Optional[bool] = None

    notify_employee: Optional[bool] = None

    employee_link: Optional[str] = None





class SupplierScorecardStandingRead(ReadSchema):

    id: uuid.UUID

    name: str

    standing_name: Optional[str] = None

    standing_color: Optional[SupplierScorecardStandingStandingColor] = None

    min_grade: Optional[Decimal] = None

    max_grade: Optional[Decimal] = None

    warn_rfqs: Optional[bool] = None

    warn_pos: Optional[bool] = None

    prevent_rfqs: Optional[bool] = None

    prevent_pos: Optional[bool] = None

    notify_supplier: Optional[bool] = None

    notify_employee: Optional[bool] = None

    employee_link: Optional[str] = None





SupplierScorecardStandingListResponse = Page[SupplierScorecardStandingRead]
