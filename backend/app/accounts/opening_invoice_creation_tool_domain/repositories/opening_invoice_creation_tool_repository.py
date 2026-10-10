"""Data access for OpeningInvoiceCreationTool. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.opening_invoice_creation_tool_domain.models.opening_invoice_creation_tool import OpeningInvoiceCreationTool

from app.core.pagination import normalise_paging



__all__ = ["OpeningInvoiceCreationToolRepository"]





class OpeningInvoiceCreationToolRepository:

    model = OpeningInvoiceCreationTool



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(OpeningInvoiceCreationTool.invoices)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[OpeningInvoiceCreationTool]:

        return db.scalar(

            select(OpeningInvoiceCreationTool).where(

                OpeningInvoiceCreationTool.business_id == business_id, OpeningInvoiceCreationTool.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[OpeningInvoiceCreationTool]:

        return db.scalar(

            select(OpeningInvoiceCreationTool).where(

                OpeningInvoiceCreationTool.business_id == business_id, OpeningInvoiceCreationTool.name == name

            ).options(*self._options())

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        search: Optional[str] = None,

    ) -> tuple[Sequence[OpeningInvoiceCreationTool], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [OpeningInvoiceCreationTool.business_id == business_id]

        if search:

            conditions.append(OpeningInvoiceCreationTool.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(OpeningInvoiceCreationTool).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(OpeningInvoiceCreationTool)

            .where(*conditions)

            .order_by(OpeningInvoiceCreationTool.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: OpeningInvoiceCreationTool) -> OpeningInvoiceCreationTool:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: OpeningInvoiceCreationTool) -> None:

        db.delete(row)

        db.flush()
