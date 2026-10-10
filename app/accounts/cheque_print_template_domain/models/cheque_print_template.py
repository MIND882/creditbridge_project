"""

Cheque Print Template -- converted from ``erpnext/accounts/doctype/cheque_print_template``.





"""



from __future__ import annotations



import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["ChequePrintTemplate", "ChequePrintTemplateChequeSize"]







class ChequePrintTemplateChequeSize(str, enum.Enum):

    REGULAR = "Regular"

    A4 = "A4"









class ChequePrintTemplate(TenantModel):

    __tablename__ = "cheque_print_templates"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_cheque_print_templates_business_name"),

    )



    #: ``autoname`` = 'field:bank_name'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    has_print_format: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    bank_name: Mapped[str] = mapped_column(String(140), nullable=False)

    cheque_size: Mapped[Optional[ChequePrintTemplateChequeSize]] = mapped_column(

        SAEnum(ChequePrintTemplateChequeSize, native_enum=False, length=7, validate_strings=True),

        nullable=True,

    )

    starting_position_from_top_edge: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    cheque_width: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    cheque_height: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    scanned_cheque: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    is_account_payable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    acc_pay_dist_from_top_edge: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    acc_pay_dist_from_left_edge: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    message_to_show: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    date_dist_from_top_edge: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    date_dist_from_left_edge: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    payer_name_from_top_edge: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    payer_name_from_left_edge: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    amt_in_words_from_top_edge: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    amt_in_words_from_left_edge: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    amt_in_word_width: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    amt_in_words_line_spacing: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    amt_in_figures_from_top_edge: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    amt_in_figures_from_left_edge: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    acc_no_dist_from_top_edge: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    acc_no_dist_from_left_edge: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    signatory_from_top_edge: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    signatory_from_left_edge: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ChequePrintTemplate id={self.id}>"
