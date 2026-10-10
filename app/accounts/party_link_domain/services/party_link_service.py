# HAND-WRITTEN

"""

Business logic for Party Link -- port of

``erpnext/accounts/doctype/party_link/party_link.py``.







Upstream hooks:

    validate



**Upstream has 4 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.party_link_domain.models.party_link import PartyLink

from app.accounts.party_link_domain.repositories.party_link_repository import (

    PartyLinkRepository,

)

from app.accounts.party_link_domain.schemas.party_link import (

    PartyLinkCreate,

    PartyLinkUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PartyLinkService"]





class PartyLinkService:

    def __init__(self, repository: Optional[PartyLinkRepository] = None) -> None:

        self.repository = repository or PartyLinkRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PartyLink:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Party Link", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: PartyLink

    ) -> None:

        """

        TODO(PORT-VALIDATION): upstream validation is NOT ported.



        This controller has **4 ``frappe.throw`` site(s)** upstream.

        None are enforced here, so writes upstream would reject

        currently succeed. It fails open deliberately rather than

        blocking the CRUD surface, but must not be read as complete.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PartyLink:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PartyLink]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PartyLink].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(PartyLink).where(

                    PartyLink.business_id == business_id

                )

            )

            or 0

        )

        return f"PAR-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: PartyLinkCreate

    ) -> PartyLink:

        row = PartyLink(

            business_id=business_id,

            name=self.next_name(db, business_id),

            primary_role=payload.primary_role,

            secondary_role=payload.secondary_role,

            primary_party=payload.primary_party,

            secondary_party=payload.secondary_party,

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

        payload: PartyLinkUpdate,

    ) -> PartyLink:

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
