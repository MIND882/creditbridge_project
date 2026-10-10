"""

Pydantic v2 schemas for Account Category.



``business_id`` is absent from every input schema: the tenant is taken from the

token (see ``app.core.tenancy``) and injected by the service.

"""



from __future__ import annotations



import uuid

from datetime import datetime

from typing import Annotated, Optional



from pydantic import Field, field_validator



from app.accounts.enums import RootType

from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import Page



__all__ = [

    "AccountCategoryBase",

    "AccountCategoryCreate",

    "AccountCategoryUpdate",

    "AccountCategoryRead",

    "AccountCategoryListResponse",

]





class AccountCategoryBase(InputSchema):

    """Fields the client controls, shared by Create and Update."""



    account_category_name: Annotated[

        str,

        Field(min_length=1, max_length=140, description="Human label; unique per business"),

    ]

    description: Optional[str] = Field(default=None, max_length=2000)

    root_type: Optional[RootType] = Field(

        default=None,

        description="Pre-sets the root type of Accounts created under this category",

    )



    # ERPNext exports unselected Selects as "", so accept it as "unset" rather

    # than failing enum validation.

    @field_validator("description", "root_type", mode="before")

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class AccountCategoryCreate(AccountCategoryBase):

    """POST payload. All ERPNext-required fields are required here too."""





class AccountCategoryUpdate(InputSchema):

    """

    PATCH payload -- every field optional.



    ``root_type`` IS updatable here (unlike on Account, where the tree

    inheritance rules make it read-only), because a category is a flat lookup

    with nothing derived from it at rest.

    """



    account_category_name: Optional[Annotated[str, Field(min_length=1, max_length=140)]] = None

    description: Optional[str] = Field(default=None, max_length=2000)

    root_type: Optional[RootType] = None



    @field_validator("description", "root_type", mode="before")

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class AccountCategoryRead(ReadSchema):

    id: uuid.UUID

    business_id: uuid.UUID

    account_category_name: str

    description: Optional[str] = None

    root_type: Optional[RootType] = None

    created_at: datetime

    updated_at: datetime





#: The shared list envelope, specialised so OpenAPI renders a concrete model

#: instead of an unbound generic.

AccountCategoryListResponse = Page[AccountCategoryRead]
