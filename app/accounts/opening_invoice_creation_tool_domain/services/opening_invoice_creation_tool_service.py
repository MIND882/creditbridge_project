# HAND-WRITTEN

"""

Business logic for Opening Invoice Creation Tool -- port of

``erpnext/accounts/doctype/opening_invoice_creation_tool/opening_invoice_creation_tool.py``.







Upstream hooks:

    onload

    get_opening_invoice_summary

    validate_company

    set_missing_values

    validate_mandatory_invoice_fields

    validate_temporary_opening_account

    get_invoices

    add_party

    get_invoice_dict

    make_invoices



**Upstream has 10 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.opening_invoice_creation_tool_domain.models.opening_invoice_creation_tool import OpeningInvoiceCreationTool

from app.accounts.discounted_invoice_domain.models.discounted_invoice import DiscountedInvoice

from app.accounts.opening_invoice_creation_tool_domain.repositories.opening_invoice_creation_tool_repository import (

    OpeningInvoiceCreationToolRepository,

)

from app.accounts.opening_invoice_creation_tool_domain.schemas.opening_invoice_creation_tool import (

    OpeningInvoiceCreationToolCreate,

    OpeningInvoiceCreationToolUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["OpeningInvoiceCreationToolService"]





class OpeningInvoiceCreationToolService:

    def __init__(self, repository: Optional[OpeningInvoiceCreationToolRepository] = None) -> None:

        self.repository = repository or OpeningInvoiceCreationToolRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> OpeningInvoiceCreationTool:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Opening Invoice Creation Tool", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: OpeningInvoiceCreationTool

    ) -> None:

        """

        TODO(PORT-VALIDATION): upstream validation is NOT ported.



        This controller has **10 ``frappe.throw`` site(s)** upstream.

        None are enforced here, so writes upstream would reject

        currently succeed. It fails open deliberately rather than

        blocking the CRUD surface, but must not be read as complete.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> OpeningInvoiceCreationTool:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[OpeningInvoiceCreationTool]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[OpeningInvoiceCreationTool].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_invoices(

        self, business_id: uuid.UUID, row: OpeningInvoiceCreationTool, items: list[dict]

    ) -> None:

        row.invoices.clear()

        for idx, item in enumerate(items, start=1):

            row.invoices.append(

                OpeningInvoiceCreationToolItem(

                    business_id=business_id,

                    idx=idx,

                    party_type=item.get('party_type'),

                    party=item.get('party'),

                    temporary_opening_account_id=item.get('temporary_opening_account_id'),

                    posting_date=item.get('posting_date'),

                    due_date=item.get('due_date'),

                    item_name=item.get('item_name'),

                    outstanding_amount=item.get('outstanding_amount'),

                    qty=item.get('qty'),

                    cost_center_id=item.get('cost_center_id'),

                    invoice_number=item.get('invoice_number'),

                    supplier_invoice_date=item.get('supplier_invoice_date'),

                    party_name=item.get('party_name'),

                    project=item.get('project'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(OpeningInvoiceCreationTool).where(

                    OpeningInvoiceCreationTool.business_id == business_id

                )

            )

            or 0

        )

        return f"OPE-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: OpeningInvoiceCreationToolCreate

    ) -> OpeningInvoiceCreationTool:

        row = OpeningInvoiceCreationTool(

            business_id=business_id,

            name=self.next_name(db, business_id),

            create_missing_party=payload.create_missing_party,

            invoice_type=payload.invoice_type,

            cost_center_id=payload.cost_center_id,

            project=payload.project,

        )

        self._replace_invoices(business_id, row, [x.model_dump() for x in payload.invoices])



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

        payload: OpeningInvoiceCreationToolUpdate,

    ) -> OpeningInvoiceCreationTool:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "invoices":

                    self._replace_invoices(business_id, row, value or [])

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
