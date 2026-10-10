# HAND-WRITTEN

"""

Business logic for Financial Report Template -- port of

``erpnext/accounts/doctype/financial_report_template/financial_report_template.py``.







Upstream hooks:

    before_validate

    clear_hidden_fields

    validate

    on_update

    on_trash



Upstream declares no validation, so `_validate` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.financial_report_template_domain.models.financial_report_template import FinancialReportTemplate

from app.accounts.financial_report_row_domain.models.financial_report_row import FinancialReportRow

from app.accounts.financial_report_template_domain.repositories.financial_report_template_repository import (

    FinancialReportTemplateRepository,

)

from app.accounts.financial_report_template_domain.schemas.financial_report_template import (

    FinancialReportTemplateCreate,

    FinancialReportTemplateUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["FinancialReportTemplateService"]





class FinancialReportTemplateService:

    def __init__(self, repository: Optional[FinancialReportTemplateRepository] = None) -> None:

        self.repository = repository or FinancialReportTemplateRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> FinancialReportTemplate:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Financial Report Template", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: FinancialReportTemplate

    ) -> None:

        """

        Upstream's controller defines no ``frappe.throw``, so there is

        no rule to port. Empty by design, not by omission.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> FinancialReportTemplate:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[FinancialReportTemplate]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[FinancialReportTemplate].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_rows(

        self, business_id: uuid.UUID, row: FinancialReportTemplate, items: list[dict]

    ) -> None:

        row.rows.clear()

        for idx, item in enumerate(items, start=1):

            row.rows.append(

                FinancialReportRow(

                    business_id=business_id,

                    idx=idx,

                    reference_code=item.get('reference_code'),

                    display_name=item.get('display_name'),

                    indentation_level=item.get('indentation_level'),

                    data_source=item.get('data_source'),

                    balance_type=item.get('balance_type'),

                    bold_text=item.get('bold_text'),

                    italic_text=item.get('italic_text'),

                    hidden_calculation=item.get('hidden_calculation'),

                    hide_when_empty=item.get('hide_when_empty'),

                    reverse_sign=item.get('reverse_sign'),

                    calculation_formula=item.get('calculation_formula'),

                    include_in_charts=item.get('include_in_charts'),

                    color=item.get('color'),

                    fieldtype=item.get('fieldtype'),

                    advanced_filtering=item.get('advanced_filtering'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(FinancialReportTemplate).where(

                    FinancialReportTemplate.business_id == business_id

                )

            )

            or 0

        )

        return f"FIN-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: FinancialReportTemplateCreate

    ) -> FinancialReportTemplate:

        row = FinancialReportTemplate(

            business_id=business_id,

            name=self.next_name(db, business_id),

            template_name=payload.template_name,

            report_type=payload.report_type,

            module=payload.module,

            disabled=payload.disabled,

        )

        self._replace_rows(business_id, row, [x.model_dump() for x in payload.rows])



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

        payload: FinancialReportTemplateUpdate,

    ) -> FinancialReportTemplate:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "rows":

                    self._replace_rows(business_id, row, value or [])

                else:

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
