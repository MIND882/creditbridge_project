"""

Pydantic v2 schemas for Account.



Three fields are deliberately absent from :class:`AccountUpdate`:



``root_type`` / ``report_type``

    Derived, not chosen. ``set_root_and_report_type`` copies both from the

    parent when one exists, and infers ``report_type`` from ``root_type``

    otherwise. Letting PATCH set them would let a child disagree with its

    parent, which upstream actively repairs by cascading the parent's value

    down the subtree. Change them by moving the node.



``is_group``

    Guarded state transition, not an edit. ``validate_group_or_ledger`` blocks

    the change when GL entries or child nodes exist, and

    ``convert_group_to_ledger`` / ``convert_ledger_to_group`` are separate

    ``@frappe.whitelist()`` entry points upstream. They are exposed as

    ``POST /{id}/convert_to_ledger`` and ``POST /{id}/convert_to_group``.



``parent_account_id`` IS patchable: moving a node is a legitimate edit, and the

service runs the cycle guard on it.

"""



from __future__ import annotations



import uuid

from datetime import datetime

from decimal import Decimal

from typing import Annotated, Optional



from pydantic import Field, field_validator



from app.accounts.enums import AccountType, BalanceMustBe, FreezeAccount, ReportType, RootType

from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import Page



__all__ = [

    "AccountBase",

    "AccountCreate",

    "AccountUpdate",

    "AccountRead",

    "AccountListResponse",

    "AccountTreeNode",

    "AccountTreeResponse",

    "ConvertResult",

]





class AccountBase(InputSchema):

    """Client-controlled Account fields shared by Create and Update."""



    account_name: Annotated[str, Field(min_length=1, max_length=140)]

    account_number: Optional[Annotated[str, Field(max_length=140)]] = None

    account_type: Optional[AccountType] = None

    account_currency: Optional[Annotated[str, Field(max_length=140)]] = None

    tax_rate: Optional[Decimal] = Field(

        default=None,

        ge=0,

        description="Percent, stored as Numeric(21,9) to match the Float->Numeric rule",

    )

    balance_must_be: Optional[BalanceMustBe] = None

    freeze_account: Optional[FreezeAccount] = None

    include_in_gross: bool = False

    disabled: bool = False

    account_category: Optional[Annotated[str, Field(max_length=140)]] = None



    # ERPNext stores unselected Select/Link fields as "", so a client posting a

    # raw ERPNext export must not be rejected for it.

    @field_validator(

        "account_number",

        "account_type",

        "account_currency",

        "balance_must_be",

        "freeze_account",

        "account_category",

        mode="before",

    )

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class AccountCreate(AccountBase):

    """

    POST payload.



    ``root_type`` is accepted on create because a root node has no parent to

    inherit from -- upstream's ``validate_mandatory`` requires it to end up set

    one way or the other. On a child it is overridden by the parent's value,

    exactly as ``set_root_and_report_type`` does.



    ``is_group`` is accepted on create only: there is nothing to guard against

    yet (no GL entries, no children), so the conversion endpoints are not

    needed for the initial choice.

    """



    parent_account_id: Optional[uuid.UUID] = Field(

        default=None, description="Omit or null to create a root node"

    )

    root_type: Optional[RootType] = None

    is_group: bool = False



    @field_validator("root_type", mode="before")

    @classmethod

    def _empty_root_type(cls, v: object) -> object:

        return blank_to_none(v)





class AccountUpdate(InputSchema):

    """PATCH payload -- all optional; see the module docstring for exclusions."""



    account_name: Optional[Annotated[str, Field(min_length=1, max_length=140)]] = None

    account_number: Optional[Annotated[str, Field(max_length=140)]] = None

    parent_account_id: Optional[uuid.UUID] = None

    account_type: Optional[AccountType] = None

    account_currency: Optional[Annotated[str, Field(max_length=140)]] = None

    tax_rate: Optional[Decimal] = Field(default=None, ge=0)

    balance_must_be: Optional[BalanceMustBe] = None

    freeze_account: Optional[FreezeAccount] = None

    include_in_gross: Optional[bool] = None

    disabled: Optional[bool] = None

    account_category: Optional[Annotated[str, Field(max_length=140)]] = None



    @field_validator(

        "account_number",

        "account_type",

        "account_currency",

        "balance_must_be",

        "freeze_account",

        "account_category",

        mode="before",

    )

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class AccountRead(ReadSchema):

    """Full Account representation, including the derived fields."""



    id: uuid.UUID

    business_id: uuid.UUID

    name: str

    account_name: str

    account_number: Optional[str] = None

    parent_account_id: Optional[uuid.UUID] = None

    is_group: bool

    root_type: Optional[RootType] = None

    report_type: Optional[ReportType] = None

    account_type: Optional[AccountType] = None

    account_currency: Optional[str] = None

    tax_rate: Optional[Decimal] = None

    balance_must_be: Optional[BalanceMustBe] = None

    freeze_account: Optional[FreezeAccount] = None

    include_in_gross: bool

    disabled: bool

    account_category: Optional[str] = None

    created_at: datetime

    updated_at: datetime





AccountListResponse = Page[AccountRead]





class AccountTreeNode(ReadSchema):

    """

    One node of ``GET /tree``.



    Recursive: ``children`` nests the subtree. ``depth`` is included so a client

    can render indentation without recomputing it, and because the adjacency

    list no longer carries ``lft``/``rgt`` to infer ordering from.

    """



    id: uuid.UUID

    name: str

    account_name: str

    account_number: Optional[str] = None

    parent_account_id: Optional[uuid.UUID] = None

    is_group: bool

    root_type: Optional[RootType] = None

    report_type: Optional[ReportType] = None

    account_type: Optional[AccountType] = None

    account_currency: Optional[str] = None

    disabled: bool

    depth: int = 0

    children: list["AccountTreeNode"] = Field(default_factory=list)





AccountTreeNode.model_rebuild()





class AccountTreeResponse(ReadSchema):

    """Envelope for ``GET /tree`` -- a forest, since a tenant may have >1 root."""



    roots: list[AccountTreeNode]

    total_nodes: int





class ConvertResult(ReadSchema):

    """Returned by the group/ledger conversion endpoints."""



    id: uuid.UUID

    is_group: bool

    converted: bool = True
