"""Pydantic v2 schemas for ChequePrintTemplate."""





from __future__ import annotations

from app.accounts.cheque_print_template_domain.models.cheque_print_template import (

    ChequePrintTemplateChequeSize,

)

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ChequePrintTemplateCreate",

    "ChequePrintTemplateUpdate",

    "ChequePrintTemplateRead",

    "ChequePrintTemplateListResponse",

]





class ChequePrintTemplateBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    has_print_format: Optional[bool] = None

    bank_name: str

    cheque_size: Optional[ChequePrintTemplateChequeSize] = None

    starting_position_from_top_edge: Optional[Decimal] = None

    cheque_width: Optional[Decimal] = None

    cheque_height: Optional[Decimal] = None

    scanned_cheque: Optional[str] = None

    is_account_payable: Optional[bool] = None

    acc_pay_dist_from_top_edge: Optional[Decimal] = None

    acc_pay_dist_from_left_edge: Optional[Decimal] = None

    message_to_show: Optional[str] = None

    date_dist_from_top_edge: Optional[Decimal] = None

    date_dist_from_left_edge: Optional[Decimal] = None

    payer_name_from_top_edge: Optional[Decimal] = None

    payer_name_from_left_edge: Optional[Decimal] = None

    amt_in_words_from_top_edge: Optional[Decimal] = None

    amt_in_words_from_left_edge: Optional[Decimal] = None

    amt_in_word_width: Optional[Decimal] = None

    amt_in_words_line_spacing: Optional[Decimal] = None

    amt_in_figures_from_top_edge: Optional[Decimal] = None

    amt_in_figures_from_left_edge: Optional[Decimal] = None

    acc_no_dist_from_top_edge: Optional[Decimal] = None

    acc_no_dist_from_left_edge: Optional[Decimal] = None

    signatory_from_top_edge: Optional[Decimal] = None

    signatory_from_left_edge: Optional[Decimal] = None





class ChequePrintTemplateCreate(ChequePrintTemplateBase):

    pass





class ChequePrintTemplateUpdate(InputSchema):

    """A partial update."""



    has_print_format: Optional[bool] = None

    bank_name: Optional[str] = None

    cheque_size: Optional[ChequePrintTemplateChequeSize] = None

    starting_position_from_top_edge: Optional[Decimal] = None

    cheque_width: Optional[Decimal] = None

    cheque_height: Optional[Decimal] = None

    scanned_cheque: Optional[str] = None

    is_account_payable: Optional[bool] = None

    acc_pay_dist_from_top_edge: Optional[Decimal] = None

    acc_pay_dist_from_left_edge: Optional[Decimal] = None

    message_to_show: Optional[str] = None

    date_dist_from_top_edge: Optional[Decimal] = None

    date_dist_from_left_edge: Optional[Decimal] = None

    payer_name_from_top_edge: Optional[Decimal] = None

    payer_name_from_left_edge: Optional[Decimal] = None

    amt_in_words_from_top_edge: Optional[Decimal] = None

    amt_in_words_from_left_edge: Optional[Decimal] = None

    amt_in_word_width: Optional[Decimal] = None

    amt_in_words_line_spacing: Optional[Decimal] = None

    amt_in_figures_from_top_edge: Optional[Decimal] = None

    amt_in_figures_from_left_edge: Optional[Decimal] = None

    acc_no_dist_from_top_edge: Optional[Decimal] = None

    acc_no_dist_from_left_edge: Optional[Decimal] = None

    signatory_from_top_edge: Optional[Decimal] = None

    signatory_from_left_edge: Optional[Decimal] = None





class ChequePrintTemplateRead(ReadSchema):

    id: uuid.UUID

    name: str

    has_print_format: bool

    bank_name: str

    cheque_size: Optional[ChequePrintTemplateChequeSize] = None

    starting_position_from_top_edge: Optional[Decimal] = None

    cheque_width: Optional[Decimal] = None

    cheque_height: Optional[Decimal] = None

    scanned_cheque: Optional[str] = None

    is_account_payable: bool

    acc_pay_dist_from_top_edge: Optional[Decimal] = None

    acc_pay_dist_from_left_edge: Optional[Decimal] = None

    message_to_show: Optional[str] = None

    date_dist_from_top_edge: Optional[Decimal] = None

    date_dist_from_left_edge: Optional[Decimal] = None

    payer_name_from_top_edge: Optional[Decimal] = None

    payer_name_from_left_edge: Optional[Decimal] = None

    amt_in_words_from_top_edge: Optional[Decimal] = None

    amt_in_words_from_left_edge: Optional[Decimal] = None

    amt_in_word_width: Optional[Decimal] = None

    amt_in_words_line_spacing: Optional[Decimal] = None

    amt_in_figures_from_top_edge: Optional[Decimal] = None

    amt_in_figures_from_left_edge: Optional[Decimal] = None

    acc_no_dist_from_top_edge: Optional[Decimal] = None

    acc_no_dist_from_left_edge: Optional[Decimal] = None

    signatory_from_top_edge: Optional[Decimal] = None

    signatory_from_left_edge: Optional[Decimal] = None





ChequePrintTemplateListResponse = Page[ChequePrintTemplateRead]
