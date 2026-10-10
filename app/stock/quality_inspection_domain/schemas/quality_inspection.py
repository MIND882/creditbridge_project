"""Pydantic v2 schemas for QualityInspection."""





from __future__ import annotations

from app.stock.quality_inspection_domain.models.quality_inspection import (

    QualityInspectionNamingSeries,

    QualityInspectionInspectionType,

    QualityInspectionReferenceType,

    QualityInspectionStatus,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.stock.quality_inspection_reading_domain.schemas.quality_inspection_reading import (

    QualityInspectionReadingCreate,

    QualityInspectionReadingRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "QualityInspectionCreate",

    "QualityInspectionUpdate",

    "QualityInspectionRead",

    "QualityInspectionListResponse",

]





class QualityInspectionBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    naming_series: QualityInspectionNamingSeries

    report_date: dt.date

    inspection_type: QualityInspectionInspectionType

    reference_type: QualityInspectionReferenceType

    reference_name: str

    item_code_id: uuid.UUID

    item_serial_no_id: Optional[uuid.UUID] = None

    batch_no_id: Optional[uuid.UUID] = None

    sample_size: Decimal

    item_name: Optional[str] = None

    description: Optional[str] = None

    inspected_by: str

    verified_by: Optional[str] = None

    bom_no: Optional[str] = None

    remarks: Optional[str] = None

    amended_from_id: Optional[uuid.UUID] = None

    quality_inspection_template_id: Optional[uuid.UUID] = None

    status: QualityInspectionStatus

    manual_inspection: Optional[bool] = None

    child_row_reference: Optional[str] = None

    company: Optional[str] = None

    letter_head: Optional[str] = None

    readings: list[QualityInspectionReadingCreate] = []





class QualityInspectionCreate(QualityInspectionBase):

    pass





class QualityInspectionUpdate(InputSchema):

    """A partial update."""



    naming_series: Optional[QualityInspectionNamingSeries] = None

    report_date: Optional[dt.date] = None

    inspection_type: Optional[QualityInspectionInspectionType] = None

    reference_type: Optional[QualityInspectionReferenceType] = None

    reference_name: Optional[str] = None

    item_code_id: Optional[uuid.UUID] = None

    item_serial_no_id: Optional[uuid.UUID] = None

    batch_no_id: Optional[uuid.UUID] = None

    sample_size: Optional[Decimal] = None

    item_name: Optional[str] = None

    description: Optional[str] = None

    inspected_by: Optional[str] = None

    verified_by: Optional[str] = None

    bom_no: Optional[str] = None

    remarks: Optional[str] = None

    amended_from_id: Optional[uuid.UUID] = None

    quality_inspection_template_id: Optional[uuid.UUID] = None

    status: Optional[QualityInspectionStatus] = None

    manual_inspection: Optional[bool] = None

    child_row_reference: Optional[str] = None

    company: Optional[str] = None

    letter_head: Optional[str] = None

    readings: Optional[list[QualityInspectionReadingCreate]] = None





class QualityInspectionRead(ReadSchema):

    id: uuid.UUID

    name: str

    naming_series: Optional[QualityInspectionNamingSeries] = None

    report_date: Optional[dt.date] = None

    inspection_type: Optional[QualityInspectionInspectionType] = None

    reference_type: Optional[QualityInspectionReferenceType] = None

    reference_name: str

    item_code_id: Optional[uuid.UUID] = None

    item_serial_no_id: Optional[uuid.UUID] = None

    batch_no_id: Optional[uuid.UUID] = None

    sample_size: Optional[Decimal] = None

    item_name: Optional[str] = None

    description: Optional[str] = None

    inspected_by: str

    verified_by: Optional[str] = None

    bom_no: Optional[str] = None

    remarks: Optional[str] = None

    amended_from_id: Optional[uuid.UUID] = None

    quality_inspection_template_id: Optional[uuid.UUID] = None

    status: Optional[QualityInspectionStatus] = None

    manual_inspection: Optional[bool] = None

    child_row_reference: Optional[str] = None

    company: Optional[str] = None

    letter_head: Optional[str] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0

    readings: list[QualityInspectionReadingRead] = []





QualityInspectionListResponse = Page[QualityInspectionRead]
