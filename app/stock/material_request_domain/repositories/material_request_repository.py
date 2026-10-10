"""Data access for MaterialRequest. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.material_request_domain.models.material_request import MaterialRequest

from app.core.pagination import normalise_paging



__all__ = ["MaterialRequestRepository"]





class MaterialRequestRepository:

    model = MaterialRequest





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[MaterialRequest]:

        return db.scalar(

            select(MaterialRequest).where(

                MaterialRequest.business_id == business_id, MaterialRequest.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[MaterialRequest]:

        return db.scalar(

            select(MaterialRequest).where(

                MaterialRequest.business_id == business_id, MaterialRequest.name == name

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

        include_cancelled: bool = False,

    ) -> tuple[Sequence[MaterialRequest], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [MaterialRequest.business_id == business_id]

        if not include_cancelled:

            conditions.append(MaterialRequest.docstatus != 2)

        if search:

            conditions.append(MaterialRequest.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(MaterialRequest).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(MaterialRequest)

            .where(*conditions)

            .order_by(MaterialRequest.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: MaterialRequest) -> MaterialRequest:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: MaterialRequest) -> None:

        db.delete(row)

        db.flush()
