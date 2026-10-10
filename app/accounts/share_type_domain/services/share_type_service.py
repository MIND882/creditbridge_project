"""

Business logic for Share Type -- port of

``erpnext/accounts/doctype/share_type/share_type.py``.



Upstream's controller is empty, so there is no ``validate``/``before_save`` to

port. What remains is ``autoname`` (``field:title``) and the uniqueness that

follows from it, which is enforced per tenant here.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.share_type_domain.models.share_type import ShareType

from app.accounts.share_type_domain.repositories.share_type_repository import (

    ShareTypeRepository,

)

from app.accounts.share_type_domain.schemas.share_type import (

    ShareTypeCreate,

    ShareTypeUpdate,

)

from app.core.errors import ConflictError, DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ShareTypeService"]





class ShareTypeService:

    def __init__(self, repository: Optional[ShareTypeRepository] = None) -> None:

        self.repository = repository or ShareTypeRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ShareType:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Share Type", row_id)

        return row



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ShareType:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ShareType]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ShareType].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def create(

        self, db: Session, business_id: uuid.UUID, payload: ShareTypeCreate

    ) -> ShareType:

        name = payload.title.strip()

        if not name:

            raise DomainValidationError(

                "Title is mandatory", code="share_type_title_mandatory"

            )

        if self.repository.get_by_name(db, business_id, name) is not None:

            raise ConflictError(

                f"Share Type \'{name}\' already exists", code="share_type_duplicate"

            )



        row = ShareType(

            business_id=business_id,

            name=name,

            title=name,

            description=payload.description,

        )

        try:

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

        payload: ShareTypeUpdate,

    ) -> ShareType:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                setattr(row, field_name, value)

            db.flush()

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
