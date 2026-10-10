"""Data access for InstallationNote. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.selling.installation_note_domain.models.installation_note import InstallationNote

from app.core.pagination import normalise_paging



__all__ = ["InstallationNoteRepository"]





class InstallationNoteRepository:

    model = InstallationNote





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[InstallationNote]:

        return db.scalar(

            select(InstallationNote).where(

                InstallationNote.business_id == business_id, InstallationNote.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[InstallationNote]:

        return db.scalar(

            select(InstallationNote).where(

                InstallationNote.business_id == business_id, InstallationNote.name == name

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

    ) -> tuple[Sequence[InstallationNote], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [InstallationNote.business_id == business_id]

        if search:

            conditions.append(InstallationNote.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(InstallationNote).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(InstallationNote)

            .where(*conditions)

            .order_by(InstallationNote.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: InstallationNote) -> InstallationNote:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: InstallationNote) -> None:

        db.delete(row)

        db.flush()
