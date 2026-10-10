"""Data access for ChartOfAccountsImporter. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.chart_of_accounts_importer_domain.models.chart_of_accounts_importer import ChartOfAccountsImporter

from app.core.pagination import normalise_paging



__all__ = ["ChartOfAccountsImporterRepository"]





class ChartOfAccountsImporterRepository:

    model = ChartOfAccountsImporter





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ChartOfAccountsImporter]:

        return db.scalar(

            select(ChartOfAccountsImporter).where(

                ChartOfAccountsImporter.business_id == business_id, ChartOfAccountsImporter.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ChartOfAccountsImporter]:

        return db.scalar(

            select(ChartOfAccountsImporter).where(

                ChartOfAccountsImporter.business_id == business_id, ChartOfAccountsImporter.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        search: Optional[str] = None,

    ) -> tuple[Sequence[ChartOfAccountsImporter], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ChartOfAccountsImporter.business_id == business_id]

        if search:

            conditions.append(ChartOfAccountsImporter.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(ChartOfAccountsImporter).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ChartOfAccountsImporter)

            .where(*conditions)

            .order_by(ChartOfAccountsImporter.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: ChartOfAccountsImporter) -> ChartOfAccountsImporter:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: ChartOfAccountsImporter) -> None:

        db.delete(row)

        db.flush()
