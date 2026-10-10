"""Pydantic v2 contracts for Tax Rule."""



from __future__ import annotations



import datetime as dt

import uuid

from typing import Optional



from pydantic import BaseModel, ConfigDict, Field, field_validator



from app.accounts.tax_enums import TaxRuleType

from app.core.base_schema import InputSchema, ReadSchema, blank_to_none

from app.core.pagination import ResultPage



__all__ = ["TaxRuleCreate", "TaxRuleUpdate", "TaxRuleRead", "TaxRuleListResponse"]



_BLANK_FIELDS = (

    "customer", "supplier", "item", "customer_group", "supplier_group", "item_group",

    "billing_city", "billing_county", "billing_state", "billing_zipcode", "billing_country",

    "shipping_city", "shipping_county", "shipping_state", "shipping_zipcode",

    "shipping_country",

)





def _str140() -> Field:

    return Field(default=None, max_length=140)





class TaxRuleBase(BaseModel):

    """

    Client-supplied fields. Never accepts ``business_id``.



    ``tax_type`` is deliberately *not* here. It decides which half of the rule is

    meaningful -- upstream clears the other side on save -- so it belongs on

    create only. Keeping it out of the base keeps it out of ``TaxRuleUpdate``,

    which is what makes ``extra="forbid"`` reject an attempt to patch it rather

    than silently ignoring the field.

    """



    use_for_shopping_cart: Optional[bool] = True



    sales_tax_template_id: Optional[uuid.UUID] = Field(default=None)

    purchase_tax_template_id: Optional[uuid.UUID] = Field(default=None)

    tax_category_id: Optional[uuid.UUID] = Field(default=None)



    customer: Optional[str] = _str140()

    supplier: Optional[str] = _str140()

    item: Optional[str] = _str140()

    customer_group: Optional[str] = _str140()

    supplier_group: Optional[str] = _str140()

    item_group: Optional[str] = _str140()



    billing_city: Optional[str] = _str140()

    billing_county: Optional[str] = _str140()

    billing_state: Optional[str] = _str140()

    billing_zipcode: Optional[str] = _str140()

    billing_country: Optional[str] = _str140()



    shipping_city: Optional[str] = _str140()

    shipping_county: Optional[str] = _str140()

    shipping_state: Optional[str] = _str140()

    shipping_zipcode: Optional[str] = _str140()

    shipping_country: Optional[str] = _str140()



    from_date: Optional[dt.date] = Field(default=None)

    to_date: Optional[dt.date] = Field(default=None)

    priority: Optional[int] = Field(default=1)





class TaxRuleCreate(TaxRuleBase, InputSchema):

    tax_type: Optional[TaxRuleType] = TaxRuleType.SALES



    @field_validator(*_BLANK_FIELDS, mode="before")

    @classmethod

    def _empty_is_none(cls, value: object) -> object:

        return blank_to_none(value)





class TaxRuleUpdate(TaxRuleBase, InputSchema):

    """

    A partial update.



    ``tax_type`` is not declared here at all. It decides which half of the rule

    is meaningful -- upstream clears the other side on save -- so switching it in

    place would leave a rule half-populated. Omitting it means ``extra="forbid"``

    rejects a PATCH that tries, instead of accepting the field and quietly

    dropping it. Change the type by creating a new rule.

    """



    @field_validator(*_BLANK_FIELDS, mode="before")

    @classmethod

    def _empty_is_none(cls, value: object) -> object:

        return blank_to_none(value)





class TaxRuleRead(TaxRuleBase, ReadSchema):

    id: uuid.UUID

    name: str

    tax_type: Optional[TaxRuleType] = None



    model_config = ConfigDict(from_attributes=True)





class TaxRuleListResponse(BaseModel):

    items: list[TaxRuleRead]

    total: int

    offset: int

    limit: int



    @classmethod

    def from_result(

        cls, result: ResultPage[object], items: list[TaxRuleRead]

    ) -> "TaxRuleListResponse":

        return cls(items=items, total=result.total, offset=result.offset, limit=result.limit)
