"""Pydantic v2 schemas for ShareType."""



from __future__ import annotations



import uuid

from typing import Optional



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ShareTypeCreate",

    "ShareTypeUpdate",

    "ShareTypeRead",

    "ShareTypeListResponse",

]





class ShareTypeBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    description: Optional[str] = None





class ShareTypeCreate(ShareTypeBase):

    #: ``autoname = field:title``, so this is also the ``name``.

    title: str





class ShareTypeUpdate(ShareTypeBase):

    """

    A partial update.



    ``title`` is not patchable: upstream it *is* the ``name``, and renaming it

    would break every ``Share Balance`` row referring to it.

    """





class ShareTypeRead(ReadSchema):

    id: uuid.UUID

    name: str

    title: str

    description: Optional[str] = None





ShareTypeListResponse = Page[ShareTypeRead]
