"""Business logic for BOM Update Tool -- port of

``erpnext/manufacturing/doctype/bom_update_tool/bom_update_tool.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.manufacturing.bom_update_tool_domain.models.bom_update_tool import BomUpdateTool

from app.manufacturing.bom_update_tool_domain.repositories.bom_update_tool_repository import (

    BomUpdateToolRepository,

)

from app.manufacturing.bom_update_tool_domain.schemas.bom_update_tool import (

    BomUpdateToolUpdate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BomUpdateToolService"]





class BomUpdateToolService:

    def __init__(self, repository: Optional[BomUpdateToolRepository] = None) -> None:

        self.repository = repository or BomUpdateToolRepository()





    def get_or_create(

        self, db: Session, business_id: uuid.UUID

    ) -> BomUpdateTool:

        """The tenant's settings row, created with upstream defaults on first read."""

        row = self.repository.get_for_business(db, business_id)

        if row is None:

            row = BomUpdateTool(business_id=business_id)

            try:

                self.repository.add(db, row)

                db.commit()

            except Exception:

                db.rollback()

                raise

            db.refresh(row)

        return row



    def update(

        self, db: Session, business_id: uuid.UUID, payload: BomUpdateToolUpdate

    ) -> BomUpdateTool:

        row = self.get_or_create(db, business_id)

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
