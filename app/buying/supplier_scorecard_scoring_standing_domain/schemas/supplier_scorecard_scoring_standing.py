"""Pydantic v2 schemas for SupplierScorecardScoringStanding."""





from __future__ import annotations

from app.buying.supplier_scorecard_scoring_standing_domain.models.supplier_scorecard_scoring_standing import (

    SupplierScorecardScoringStandingStandingColor,

)

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SupplierScorecardScoringStandingCreate",

    "SupplierScorecardScoringStandingRead",

    "SupplierScorecardScoringStandingListResponse",

]





class SupplierScorecardScoringStandingBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    standing_name_id: Optional[uuid.UUID] = None

    standing_color: Optional[SupplierScorecardScoringStandingStandingColor] = None

    min_grade: Optional[Decimal] = None

    max_grade: Optional[Decimal] = None

    warn_rfqs: Optional[bool] = None

    warn_pos: Optional[bool] = None

    prevent_rfqs: Optional[bool] = None

    prevent_pos: Optional[bool] = None

    notify_supplier: Optional[bool] = None

    notify_employee: Optional[bool] = None

    employee_link: Optional[str] = None





class SupplierScorecardScoringStandingCreate(SupplierScorecardScoringStandingBase):

    pass





class SupplierScorecardScoringStandingUpdate(InputSchema):

    """A partial update."""



    standing_name_id: Optional[uuid.UUID] = None

    standing_color: Optional[SupplierScorecardScoringStandingStandingColor] = None

    min_grade: Optional[Decimal] = None

    max_grade: Optional[Decimal] = None

    warn_rfqs: Optional[bool] = None

    warn_pos: Optional[bool] = None

    prevent_rfqs: Optional[bool] = None

    prevent_pos: Optional[bool] = None

    notify_supplier: Optional[bool] = None

    notify_employee: Optional[bool] = None

    employee_link: Optional[str] = None





class SupplierScorecardScoringStandingRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    standing_name_id: Optional[uuid.UUID] = None

    standing_color: Optional[SupplierScorecardScoringStandingStandingColor] = None

    min_grade: Optional[Decimal] = None

    max_grade: Optional[Decimal] = None

    warn_rfqs: Optional[bool] = None

    warn_pos: Optional[bool] = None

    prevent_rfqs: Optional[bool] = None

    prevent_pos: Optional[bool] = None

    notify_supplier: Optional[bool] = None

    notify_employee: Optional[bool] = None

    employee_link: Optional[str] = None





SupplierScorecardScoringStandingListResponse = Page[SupplierScorecardScoringStandingRead]
