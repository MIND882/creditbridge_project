# HAND-WRITTEN

"""

Business logic for Cheque Print Template -- port of

``erpnext/accounts/doctype/cheque_print_template/cheque_print_template.py``.







Upstream hooks:

    (none -- upstream's controller defines no hooks)



Upstream declares no validation, so `_validate` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.cheque_print_template_domain.models.cheque_print_template import ChequePrintTemplate

from app.accounts.cheque_print_template_domain.repositories.cheque_print_template_repository import (

    ChequePrintTemplateRepository,

)

from app.accounts.cheque_print_template_domain.schemas.cheque_print_template import (

    ChequePrintTemplateCreate,

    ChequePrintTemplateUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ChequePrintTemplateService"]





class ChequePrintTemplateService:

    def __init__(self, repository: Optional[ChequePrintTemplateRepository] = None) -> None:

        self.repository = repository or ChequePrintTemplateRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ChequePrintTemplate:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Cheque Print Template", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: ChequePrintTemplate

    ) -> None:

        """

        Upstream's controller defines no ``frappe.throw``, so there is

        no rule to port. Empty by design, not by omission.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ChequePrintTemplate:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ChequePrintTemplate]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ChequePrintTemplate].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(ChequePrintTemplate).where(

                    ChequePrintTemplate.business_id == business_id

                )

            )

            or 0

        )

        return f"CHE-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: ChequePrintTemplateCreate

    ) -> ChequePrintTemplate:

        row = ChequePrintTemplate(

            business_id=business_id,

            name=self.next_name(db, business_id),

            has_print_format=payload.has_print_format,

            bank_name=payload.bank_name,

            cheque_size=payload.cheque_size,

            starting_position_from_top_edge=payload.starting_position_from_top_edge,

            cheque_width=payload.cheque_width,

            cheque_height=payload.cheque_height,

            scanned_cheque=payload.scanned_cheque,

            is_account_payable=payload.is_account_payable,

            acc_pay_dist_from_top_edge=payload.acc_pay_dist_from_top_edge,

            acc_pay_dist_from_left_edge=payload.acc_pay_dist_from_left_edge,

            message_to_show=payload.message_to_show,

            date_dist_from_top_edge=payload.date_dist_from_top_edge,

            date_dist_from_left_edge=payload.date_dist_from_left_edge,

            payer_name_from_top_edge=payload.payer_name_from_top_edge,

            payer_name_from_left_edge=payload.payer_name_from_left_edge,

            amt_in_words_from_top_edge=payload.amt_in_words_from_top_edge,

            amt_in_words_from_left_edge=payload.amt_in_words_from_left_edge,

            amt_in_word_width=payload.amt_in_word_width,

            amt_in_words_line_spacing=payload.amt_in_words_line_spacing,

            amt_in_figures_from_top_edge=payload.amt_in_figures_from_top_edge,

            amt_in_figures_from_left_edge=payload.amt_in_figures_from_left_edge,

            acc_no_dist_from_top_edge=payload.acc_no_dist_from_top_edge,

            acc_no_dist_from_left_edge=payload.acc_no_dist_from_left_edge,

            signatory_from_top_edge=payload.signatory_from_top_edge,

            signatory_from_left_edge=payload.signatory_from_left_edge,

        )



        try:

            db.flush()  # children need ids before validation reads them

            self._validate(db, business_id, row)

            self.repository.add(db, row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def update(

        self,

        db: Session,

        business_id: uuid.UUID,

        row_id: uuid.UUID,

        payload: ChequePrintTemplateUpdate,

    ) -> ChequePrintTemplate:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                setattr(row, field_name, value)

            db.flush()

            self._validate(db, business_id, row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def delete(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> None:

        row = self._get_or_404(db, business_id, row_id)

        self.repository.delete(db, row)

        db.commit()
