"""Data access for ChequePrintTemplate. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.cheque_print_template_domain.models.cheque_print_template import ChequePrintTemplate

from app.core.pagination import normalise_paging



__all__ = ["ChequePrintTemplateRepository"]





class ChequePrintTemplateRepository:

    model = ChequePrintTemplate





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ChequePrintTemplate]:

        return db.scalar(

            select(ChequePrintTemplate).where(

                ChequePrintTemplate.business_id == business_id, ChequePrintTemplate.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ChequePrintTemplate]:

        return db.scalar(

            select(ChequePrintTemplate).where(

                ChequePrintTemplate.business_id == business_id, ChequePrintTemplate.name == name

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

    ) -> tuple[Sequence[ChequePrintTemplate], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ChequePrintTemplate.business_id == business_id]

        if search:

            conditions.append(ChequePrintTemplate.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(ChequePrintTemplate).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ChequePrintTemplate)

            .where(*conditions)

            .order_by(ChequePrintTemplate.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: ChequePrintTemplate) -> ChequePrintTemplate:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: ChequePrintTemplate) -> None:

        db.delete(row)

        db.flush()
