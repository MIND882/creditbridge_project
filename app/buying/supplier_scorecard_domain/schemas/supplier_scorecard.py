"""Pydantic v2 schemas for SupplierScorecard."""





from __future__ import annotations

from app.buying.supplier_scorecard_domain.models.supplier_scorecard import (

    SupplierScorecardPeriod,

)

from typing import Optional

import uuid



from app.buying.supplier_scorecard_scoring_standing_domain.schemas.supplier_scorecard_scoring_standing import (

    SupplierScorecardScoringStandingCreate,

    SupplierScorecardScoringStandingRead,

)

from app.buying.supplier_scorecard_scoring_criteria_domain.schemas.supplier_scorecard_scoring_criteria import (

    SupplierScorecardScoringCriteriaCreate,

    SupplierScorecardScoringCriteriaRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SupplierScorecardCreate",

    "SupplierScorecardUpdate",

    "SupplierScorecardRead",

    "SupplierScorecardListResponse",

]





class SupplierScorecardBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    supplier_id: Optional[uuid.UUID] = None

    supplier_score: Optional[str] = None

    indicator_color: Optional[str] = None

    status: Optional[str] = None

    period: SupplierScorecardPeriod

    weighting_function: str

    warn_rfqs: Optional[bool] = None

    warn_pos: Optional[bool] = None

    prevent_rfqs: Optional[bool] = None

    prevent_pos: Optional[bool] = None

    notify_supplier: Optional[bool] = None

    notify_employee: Optional[bool] = None

    employee: Optional[str] = None

    standings: list[SupplierScorecardScoringStandingCreate] = []

    criteria: list[SupplierScorecardScoringCriteriaCreate] = []





class SupplierScorecardCreate(SupplierScorecardBase):

    pass





class SupplierScorecardUpdate(InputSchema):

    """A partial update."""



    supplier_id: Optional[uuid.UUID] = None

    supplier_score: Optional[str] = None

    indicator_color: Optional[str] = None

    status: Optional[str] = None

    period: Optional[SupplierScorecardPeriod] = None

    weighting_function: Optional[str] = None

    warn_rfqs: Optional[bool] = None

    warn_pos: Optional[bool] = None

    prevent_rfqs: Optional[bool] = None

    prevent_pos: Optional[bool] = None

    notify_supplier: Optional[bool] = None

    notify_employee: Optional[bool] = None

    employee: Optional[str] = None

    standings: Optional[list[SupplierScorecardScoringStandingCreate]] = None

    criteria: Optional[list[SupplierScorecardScoringCriteriaCreate]] = None





class SupplierScorecardRead(ReadSchema):

    id: uuid.UUID

    name: str

    supplier_id: Optional[uuid.UUID] = None

    supplier_score: Optional[str] = None

    indicator_color: Optional[str] = None

    status: Optional[str] = None

    period: Optional[SupplierScorecardPeriod] = None

    weighting_function: str

    warn_rfqs: Optional[bool] = None

    warn_pos: Optional[bool] = None

    prevent_rfqs: Optional[bool] = None

    prevent_pos: Optional[bool] = None

    notify_supplier: Optional[bool] = None

    notify_employee: Optional[bool] = None

    employee: Optional[str] = None

    standings: list[SupplierScorecardScoringStandingRead] = []

    criteria: list[SupplierScorecardScoringCriteriaRead] = []





SupplierScorecardListResponse = Page[SupplierScorecardRead]
