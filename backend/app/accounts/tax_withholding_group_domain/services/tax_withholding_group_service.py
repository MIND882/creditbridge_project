# HAND-WRITTEN

"""

Business logic for Tax Withholding Group -- port of

``erpnext/accounts/doctype/tax_withholding_group/tax_withholding_group.py``.







Upstream hooks:

    (none -- upstream's controller defines no hooks)



Upstream declares no validation, so `_validate` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.tax_withholding_group_domain.models.tax_withholding_group import TaxWithholdingGroup

from app.accounts.tax_withholding_group_domain.repositories.tax_withholding_group_repository import (

    TaxWithholdingGroupRepository,

)

from app.accounts.tax_withholding_group_domain.schemas.tax_withholding_group import (

    TaxWithholdingGroupCreate,

    TaxWithholdingGroupUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["TaxWithholdingGroupService"]





class TaxWithholdingGroupService:

    def __init__(self, repository: Optional[TaxWithholdingGroupRepository] = None) -> None:

        self.repository = repository or TaxWithholdingGroupRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> TaxWithholdingGroup:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Tax Withholding Group", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: TaxWithholdingGroup

    ) -> None:

        """

        Upstream's controller defines no ``frappe.throw``, so there is

        no rule to port. Empty by design, not by omission.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> TaxWithholdingGroup:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[TaxWithholdingGroup]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[TaxWithholdingGroup].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(TaxWithholdingGroup).where(

                    TaxWithholdingGroup.business_id == business_id

                )

            )

            or 0

        )

        return f"TAX-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: TaxWithholdingGroupCreate

    ) -> TaxWithholdingGroup:

        row = TaxWithholdingGroup(

            business_id=business_id,

            name=self.next_name(db, business_id),

            group_name=payload.group_name,

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

        payload: TaxWithholdingGroupUpdate,

    ) -> TaxWithholdingGroup:

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
