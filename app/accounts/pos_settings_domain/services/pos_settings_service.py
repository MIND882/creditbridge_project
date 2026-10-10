# HAND-WRITTEN

"""

Business logic for POS Settings -- port of

``erpnext/accounts/doctype/pos_settings/pos_settings.py``.







Upstream hooks:

    validate

    validate_invoice_fields

    validate_invoice_type



**Upstream has 2 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.pos_settings_domain.models.pos_settings import POSSettings

from app.accounts.pos_field_domain.models.pos_field import POSField

from app.accounts.pos_search_fields_domain.models.pos_search_fields import POSSearchFields

from app.accounts.pos_settings_domain.repositories.pos_settings_repository import (

    POSSettingsRepository,

)

from app.accounts.pos_settings_domain.schemas.pos_settings import (

    POSSettingsCreate,

    POSSettingsUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["POSSettingsService"]





class POSSettingsService:

    def __init__(self, repository: Optional[POSSettingsRepository] = None) -> None:

        self.repository = repository or POSSettingsRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> POSSettings:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("POS Settings", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: POSSettings

    ) -> None:

        """

        TODO(PORT-VALIDATION): upstream validation is NOT ported.



        This controller has **2 ``frappe.throw`` site(s)** upstream.

        None are enforced here, so writes upstream would reject

        currently succeed. It fails open deliberately rather than

        blocking the CRUD surface, but must not be read as complete.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> POSSettings:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[POSSettings]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[POSSettings].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_invoice_fields(

        self, business_id: uuid.UUID, row: POSSettings, items: list[dict]

    ) -> None:

        row.invoice_fields.clear()

        for idx, item in enumerate(items, start=1):

            row.invoice_fields.append(

                POSField(

                    business_id=business_id,

                    idx=idx,

                    fieldname=item.get('fieldname'),

                    fieldtype=item.get('fieldtype'),

                    label=item.get('label'),

                    options=item.get('options'),

                    reqd=item.get('reqd'),

                    read_only=item.get('read_only'),

                    default_value=item.get('default_value'),

                )

            )



    def _replace_pos_search_fields(

        self, business_id: uuid.UUID, row: POSSettings, items: list[dict]

    ) -> None:

        row.pos_search_fields.clear()

        for idx, item in enumerate(items, start=1):

            row.pos_search_fields.append(

                POSSearchFields(

                    business_id=business_id,

                    idx=idx,

                    fieldname=item.get('fieldname'),

                    field=item.get('field'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(POSSettings).where(

                    POSSettings.business_id == business_id

                )

            )

            or 0

        )

        return f"POS-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: POSSettingsCreate

    ) -> POSSettings:

        row = POSSettings(

            business_id=business_id,

            name=self.next_name(db, business_id),

            invoice_type=payload.invoice_type,

            post_change_gl_entries=payload.post_change_gl_entries,

        )

        self._replace_invoice_fields(business_id, row, [x.model_dump() for x in payload.invoice_fields])

        self._replace_pos_search_fields(business_id, row, [x.model_dump() for x in payload.pos_search_fields])



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

        payload: POSSettingsUpdate,

    ) -> POSSettings:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "invoice_fields":

                    self._replace_invoice_fields(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "pos_search_fields":

                    self._replace_pos_search_fields(business_id, row, value or [])

                else:

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
