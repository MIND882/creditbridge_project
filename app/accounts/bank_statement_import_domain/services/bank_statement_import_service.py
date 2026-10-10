# HAND-WRITTEN

"""

Business logic for Bank Statement Import -- port of

``erpnext/accounts/doctype/bank_statement_import/bank_statement_import.py``.







Upstream hooks:

    validate

    start_import



**Upstream has 6 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.bank_statement_import_domain.models.bank_statement_import import BankStatementImport

from app.accounts.bank_statement_import_domain.repositories.bank_statement_import_repository import (

    BankStatementImportRepository,

)

from app.accounts.bank_statement_import_domain.schemas.bank_statement_import import (

    BankStatementImportCreate,

    BankStatementImportUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BankStatementImportService"]





class BankStatementImportService:

    def __init__(self, repository: Optional[BankStatementImportRepository] = None) -> None:

        self.repository = repository or BankStatementImportRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> BankStatementImport:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Bank Statement Import", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: BankStatementImport

    ) -> None:

        """

        TODO(PORT-VALIDATION): upstream validation is NOT ported.



        This controller has **6 ``frappe.throw`` site(s)** upstream.

        None are enforced here, so writes upstream would reject

        currently succeed. It fails open deliberately rather than

        blocking the CRUD surface, but must not be read as complete.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> BankStatementImport:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[BankStatementImport]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[BankStatementImport].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(BankStatementImport).where(

                    BankStatementImport.business_id == business_id

                )

            )

            or 0

        )

        return f"BAN-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: BankStatementImportCreate

    ) -> BankStatementImport:

        row = BankStatementImport(

            business_id=business_id,

            name=self.next_name(db, business_id),

            bank_account_id=payload.bank_account_id,

            bank_id=payload.bank_id,

            import_file=payload.import_file,

            template_options=payload.template_options,

            status=payload.status,

            template_warnings=payload.template_warnings,

            show_failed_logs=payload.show_failed_logs,

            google_sheets_url=payload.google_sheets_url,

            reference_doctype=payload.reference_doctype,

            import_type=payload.import_type,

            submit_after_import=payload.submit_after_import,

            mute_emails=payload.mute_emails,

            custom_delimiters=payload.custom_delimiters,

            delimiter_options=payload.delimiter_options,

            use_csv_sniffer=payload.use_csv_sniffer,

            import_mt940_fromat=payload.import_mt940_fromat,

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

        payload: BankStatementImportUpdate,

    ) -> BankStatementImport:

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
