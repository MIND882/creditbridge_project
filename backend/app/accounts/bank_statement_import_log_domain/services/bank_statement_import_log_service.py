# HAND-WRITTEN

"""

Business logic for Bank Statement Import Log -- port of

``erpnext/accounts/doctype/bank_statement_import_log/bank_statement_import_log.py``.







Upstream hooks:

    before_validate

    set_currency

    validate

    before_insert

    after_insert

    set_file_properties

    recompute_properties

    set_total_debits_and_credits

    get_file_doc

    get_file_extension

    is_pdf

    get_statement_password

    get_data

    set_header_row_index

    set_column_mapping

    set_column_mapping_from_columns

    apply_column_mapping

    apply_header_index

    get_transaction_rows

    set_closing_balance

    get_final_transactions

    get_pdf_tables

    prepare_pdf_tables

    attach_pdf_page_images

    save_page_image

    get_pdf_final_transactions

    set_pdf_summary

    apply_pdf_tables

    insert_transactions



**Upstream has 16 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.bank_statement_import_log_domain.models.bank_statement_import_log import BankStatementImportLog

from app.accounts.bank_statement_import_log_column_map_domain.models.bank_statement_import_log_column_map import BankStatementImportLogColumnMap

from app.accounts.bank_statement_import_log_domain.repositories.bank_statement_import_log_repository import (

    BankStatementImportLogRepository,

)

from app.accounts.bank_statement_import_log_domain.schemas.bank_statement_import_log import (

    BankStatementImportLogCreate,

    BankStatementImportLogUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BankStatementImportLogService"]





class BankStatementImportLogService:

    def __init__(self, repository: Optional[BankStatementImportLogRepository] = None) -> None:

        self.repository = repository or BankStatementImportLogRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> BankStatementImportLog:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Bank Statement Import Log", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: BankStatementImportLog

    ) -> None:

        """

        TODO(PORT-VALIDATION): upstream validation is NOT ported.



        This controller has **16 ``frappe.throw`` site(s)** upstream.

        None are enforced here, so writes upstream would reject

        currently succeed. It fails open deliberately rather than

        blocking the CRUD surface, but must not be read as complete.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> BankStatementImportLog:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[BankStatementImportLog]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[BankStatementImportLog].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_column_mapping(

        self, business_id: uuid.UUID, row: BankStatementImportLog, items: list[dict]

    ) -> None:

        row.column_mapping.clear()

        for idx, item in enumerate(items, start=1):

            row.column_mapping.append(

                BankStatementImportLogColumnMap(

                    business_id=business_id,

                    idx=idx,

                    header_text=item.get('header_text'),

                    maps_to=item.get('maps_to'),

                    index=item.get('index'),

                    variable=item.get('variable'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(BankStatementImportLog).where(

                    BankStatementImportLog.business_id == business_id

                )

            )

            or 0

        )

        return f"BAN-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: BankStatementImportLogCreate

    ) -> BankStatementImportLog:

        row = BankStatementImportLog(

            business_id=business_id,

            name=self.next_name(db, business_id),

            bank_account_id=payload.bank_account_id,

            number_of_transactions=payload.number_of_transactions,

            closing_balance=payload.closing_balance,

            start_date=payload.start_date,

            end_date=payload.end_date,

            file=payload.file,

            detected_date_format=payload.detected_date_format,

            detected_amount_format=payload.detected_amount_format,

            detected_header_index=payload.detected_header_index,

            detected_transaction_starting_index=payload.detected_transaction_starting_index,

            detected_transaction_ending_index=payload.detected_transaction_ending_index,

            pdf_tables=payload.pdf_tables,

            status=payload.status,

            currency=payload.currency,

            total_debits=payload.total_debits,

            total_credits=payload.total_credits,

            total_debit_transactions=payload.total_debit_transactions,

            total_credit_transactions=payload.total_credit_transactions,

        )

        self._replace_column_mapping(business_id, row, [x.model_dump() for x in payload.column_mapping])



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

        payload: BankStatementImportLogUpdate,

    ) -> BankStatementImportLog:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "column_mapping":

                    self._replace_column_mapping(business_id, row, value or [])

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
