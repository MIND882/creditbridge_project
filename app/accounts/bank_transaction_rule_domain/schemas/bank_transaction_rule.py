"""Pydantic v2 schemas for Bank Transaction Rule."""



from __future__ import annotations



import uuid

from datetime import datetime

from decimal import Decimal

from typing import Annotated, Optional



from pydantic import Field, field_validator



from app.accounts.bank_transaction_rule_accounts_domain.schemas.bank_transaction_rule_accounts import (

    BankTransactionRuleAccountCreate,

    BankTransactionRuleAccountRead,

)

from app.accounts.bank_transaction_rule_description_conditions_domain.schemas.bank_transaction_rule_description_conditions import (

    BankTransactionRuleDescriptionConditionCreate,

    BankTransactionRuleDescriptionConditionRead,

)

from app.accounts.bank_transaction_rule_domain.models.bank_transaction_rule import (

    RuleBankEntryType,

    RuleClassifyAs,

    RuleTransactionType,

)

from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import Page



__all__ = [

    "BankTransactionRuleCreate",

    "BankTransactionRuleUpdate",

    "BankTransactionRuleRead",

    "BankTransactionRuleListResponse",

]



_STR = Annotated[str, Field(max_length=140)]





class BankTransactionRuleCreate(InputSchema):

    rule_name: Annotated[str, Field(min_length=1, max_length=140)]

    transaction_type: RuleTransactionType = RuleTransactionType.ANY

    min_amount: Optional[Decimal] = Field(default=None, ge=0)

    max_amount: Optional[Decimal] = Field(default=None, ge=0)

    rule_description: Optional[str] = None



    classify_as: RuleClassifyAs

    bank_entry_type: Optional[RuleBankEntryType] = None

    account_id: Optional[uuid.UUID] = None

    party_type: Optional[_STR] = None

    party: Optional[_STR] = None



    #: Optional on input: upstream assigns ``max(priority) + 1`` when unset.

    priority: Optional[int] = Field(default=None, ge=1)



    description_rules: list[BankTransactionRuleDescriptionConditionCreate] = Field(

        default_factory=list,

        description="reqd=1 upstream; a rule with no description condition never matches",

    )

    accounts: list[BankTransactionRuleAccountCreate] = Field(default_factory=list)



    @field_validator("party_type", "party", mode="before")

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class BankTransactionRuleUpdate(InputSchema):

    """

    ``priority`` is absent: it is managed by :meth:`create` (auto-assign) and

    by the renumbering that follows a delete, so accepting it here would let a

    caller create gaps or duplicates behind the service's back.

    """



    rule_name: Optional[Annotated[str, Field(min_length=1, max_length=140)]] = None

    transaction_type: Optional[RuleTransactionType] = None

    min_amount: Optional[Decimal] = Field(default=None, ge=0)

    max_amount: Optional[Decimal] = Field(default=None, ge=0)

    rule_description: Optional[str] = None



    classify_as: Optional[RuleClassifyAs] = None

    bank_entry_type: Optional[RuleBankEntryType] = None

    account_id: Optional[uuid.UUID] = None

    party_type: Optional[_STR] = None

    party: Optional[_STR] = None



    description_rules: Optional[list[BankTransactionRuleDescriptionConditionCreate]] = None

    accounts: Optional[list[BankTransactionRuleAccountCreate]] = None



    @field_validator("party_type", "party", mode="before")

    @classmethod

    def _empty_is_unset(cls, v: object) -> object:

        return blank_to_none(v)





class BankTransactionRuleRead(ReadSchema):

    id: uuid.UUID

    business_id: uuid.UUID

    name: str

    rule_name: str

    transaction_type: RuleTransactionType

    min_amount: Optional[Decimal] = None

    max_amount: Optional[Decimal] = None

    rule_description: Optional[str] = None

    classify_as: RuleClassifyAs

    bank_entry_type: Optional[RuleBankEntryType] = None

    account_id: Optional[uuid.UUID] = None

    party_type: Optional[str] = None

    party: Optional[str] = None

    priority: int

    description_rules: list[BankTransactionRuleDescriptionConditionRead] = Field(

        default_factory=list

    )

    accounts: list[BankTransactionRuleAccountRead] = Field(default_factory=list)

    created_at: datetime

    updated_at: datetime





BankTransactionRuleListResponse = Page[BankTransactionRuleRead]
