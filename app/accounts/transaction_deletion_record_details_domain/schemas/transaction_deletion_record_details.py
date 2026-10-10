"""Pydantic v2 schemas for TransactionDeletionRecordDetails."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "TransactionDeletionRecordDetailsCreate",

    "TransactionDeletionRecordDetailsRead",

    "TransactionDeletionRecordDetailsListResponse",

]





class TransactionDeletionRecordDetailsBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    doctype_name: str

    docfield_name: Optional[str] = None

    no_of_docs: Optional[int] = None

    done: Optional[bool] = None





class TransactionDeletionRecordDetailsCreate(TransactionDeletionRecordDetailsBase):

    """Accepted only nested inside the parent payload."""

    pass





class TransactionDeletionRecordDetailsRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    doctype_name: str

    docfield_name: Optional[str] = None

    no_of_docs: Optional[int] = None

    done: bool





TransactionDeletionRecordDetailsListResponse = Page[TransactionDeletionRecordDetailsRead]
