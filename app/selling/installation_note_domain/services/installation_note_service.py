"""Business logic for Installation Note -- port of

``erpnext/selling/doctype/installation_note/installation_note.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.selling.installation_note_domain.models.installation_note import InstallationNote

from app.selling.installation_note_domain.repositories.installation_note_repository import (

    InstallationNoteRepository,

)

from app.selling.installation_note_domain.schemas.installation_note import (

    InstallationNoteCreate,

    InstallationNoteUpdate,

)

from app.selling.installation_note_item_domain.models.installation_note_item import InstallationNoteItem

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["InstallationNoteService"]





class InstallationNoteService:

    def __init__(self, repository: Optional[InstallationNoteRepository] = None) -> None:

        self.repository = repository or InstallationNoteRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> InstallationNote:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Installation Note", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: InstallationNote

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> InstallationNote:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[InstallationNote]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[InstallationNote].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID, series: Optional[str] = None) -> str:

        """A per-tenant sequential name; upstream mints one from ``naming_series``."""

        # ``naming_series`` is optional on input (Frappe fills it from a

        # default), so fall back to the doctype prefix when it is absent.

        series = series or ""

        prefix = series.split(".")[0].split("#")[0]

        if prefix and not prefix.endswith("-"):

            prefix += "-"

        count = int(

            db.scalar(

                select(func.count()).select_from(InstallationNote).where(

                    InstallationNote.business_id == business_id

                )

            )

            or 0

        )

        return f"{prefix}{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: InstallationNoteCreate

    ) -> InstallationNote:

        row = InstallationNote(

            business_id=business_id,

            name=self.next_name(db, business_id, payload.naming_series),

            naming_series=payload.naming_series,

            customer_id=payload.customer_id,

            customer_address=payload.customer_address,

            contact_person=payload.contact_person,

            customer_name=payload.customer_name,

            address_display=payload.address_display,

            contact_display=payload.contact_display,

            contact_mobile=payload.contact_mobile,

            contact_email=payload.contact_email,

            territory=payload.territory,

            customer_group=payload.customer_group,

            inst_date=payload.inst_date,

            inst_time=payload.inst_time,

            status=payload.status,

            company=payload.company,

            amended_from_id=payload.amended_from_id,

            remarks=payload.remarks,

            project=payload.project,

        )

        self._replace_items(business_id, row, [x.model_dump() for x in payload.items])



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

        payload: InstallationNoteUpdate,

    ) -> InstallationNote:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "items":

                    self._replace_items(business_id, row, value or [])

                    continue

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



    def _replace_items(

        self, business_id: uuid.UUID, row: InstallationNote, items: list[dict]

    ) -> None:

        row.items.clear()

        for idx, entry in enumerate(items, start=1):

            row.items.append(

                InstallationNoteItem(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Installation Note",

                    parentfield="items",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )
