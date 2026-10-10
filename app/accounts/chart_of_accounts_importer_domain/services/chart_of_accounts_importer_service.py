# HAND-WRITTEN

"""

Business logic for Chart Of Accounts Importer -- port of

``erpnext/accounts/doctype/chart_of_accounts_importer/chart_of_accounts_importer.py``.







Upstream hooks:

    validate



**Upstream has 9 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.chart_of_accounts_importer_domain.models.chart_of_accounts_importer import ChartOfAccountsImporter

from app.accounts.chart_of_accounts_importer_domain.repositories.chart_of_accounts_importer_repository import (

    ChartOfAccountsImporterRepository,

)

from app.accounts.chart_of_accounts_importer_domain.schemas.chart_of_accounts_importer import (

    ChartOfAccountsImporterCreate,

    ChartOfAccountsImporterUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ChartOfAccountsImporterService"]





class ChartOfAccountsImporterService:

    def __init__(self, repository: Optional[ChartOfAccountsImporterRepository] = None) -> None:

        self.repository = repository or ChartOfAccountsImporterRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ChartOfAccountsImporter:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Chart Of Accounts Importer", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: ChartOfAccountsImporter

    ) -> None:

        """

        TODO(PORT-VALIDATION): upstream validation is NOT ported.



        This controller has **9 ``frappe.throw`` site(s)** upstream.

        None are enforced here, so writes upstream would reject

        currently succeed. It fails open deliberately rather than

        blocking the CRUD surface, but must not be read as complete.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ChartOfAccountsImporter:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ChartOfAccountsImporter]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ChartOfAccountsImporter].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(ChartOfAccountsImporter).where(

                    ChartOfAccountsImporter.business_id == business_id

                )

            )

            or 0

        )

        return f"CHA-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: ChartOfAccountsImporterCreate

    ) -> ChartOfAccountsImporter:

        row = ChartOfAccountsImporter(

            business_id=business_id,

            name=self.next_name(db, business_id),

            import_file=payload.import_file,

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

        payload: ChartOfAccountsImporterUpdate,

    ) -> ChartOfAccountsImporter:

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
