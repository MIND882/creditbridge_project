"""Data access for Dunning Type. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select, update

from sqlalchemy.orm import Session, selectinload



from app.accounts.dunning_type_domain.models.dunning_type import DunningType

from app.core.pagination import normalise_paging



__all__ = ["DunningTypeRepository"]





class DunningTypeRepository:

    model = DunningType



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks conftest

        # collection with "failed to locate a name".

        return [selectinload(DunningType.dunning_letter_text)]



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, dunning_type_id: uuid.UUID

    ) -> Optional[DunningType]:

        return db.scalar(

            select(DunningType)

            .where(

                DunningType.business_id == business_id,

                DunningType.id == dunning_type_id,

            )

            .options(*self._options())

        )



    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[DunningType]:

        return db.scalar(

            select(DunningType)

            .where(DunningType.business_id == business_id, DunningType.name == name)

            .options(*self._options())

        )



    def get_default(self, db: Session, business_id: uuid.UUID) -> Optional[DunningType]:

        return db.scalar(

            select(DunningType)

            .where(

                DunningType.business_id == business_id,

                DunningType.is_default.is_(True),

            )

            .options(*self._options())

        )



    def clear_default(

        self, db: Session, business_id: uuid.UUID, except_id: Optional[uuid.UUID]

    ) -> None:

        """

        Port of the ``frappe.db.set_value`` half of ``set_default_dunning_type``.



        Upstream clears ``is_default`` on every other row for the company; one

        tenant has exactly one default.

        """

        conditions = [

            DunningType.business_id == business_id,

            DunningType.is_default.is_(True),

        ]

        if except_id is not None:

            conditions.append(DunningType.id != except_id)

        db.execute(update(DunningType).where(*conditions).values(is_default=False))

        db.flush()



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        search: Optional[str] = None,

    ) -> tuple[Sequence[DunningType], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [DunningType.business_id == business_id]

        if search:

            like = f"%{search.strip()}%"

            conditions.append(

                DunningType.name.ilike(like) | DunningType.dunning_type.ilike(like)

            )



        total = int(

            db.scalar(select(func.count()).select_from(DunningType).where(*conditions)) or 0

        )

        rows = db.scalars(

            select(DunningType)

            .where(*conditions)

            .order_by(DunningType.name.asc())

            .offset(offset)

            .limit(limit)

            .options(*self._options())

        ).all()

        return rows, total



    def add(self, db: Session, row: DunningType) -> DunningType:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: DunningType) -> None:

        db.delete(row)

        db.flush()
