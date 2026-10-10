# HAND-WRITTEN

"""

Business logic for Currency Exchange Settings -- port of

``erpnext/accounts/doctype/currency_exchange_settings/currency_exchange_settings.py``.







Upstream hooks:

    validate

    set_parameters_and_result

    validate_parameters

    validate_result



**Upstream has 4 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.currency_exchange_settings_domain.models.currency_exchange_settings import CurrencyExchangeSettings

from app.accounts.currency_exchange_settings_details_domain.models.currency_exchange_settings_details import CurrencyExchangeSettingsDetails

from app.accounts.currency_exchange_settings_result_domain.models.currency_exchange_settings_result import CurrencyExchangeSettingsResult

from app.accounts.currency_exchange_settings_domain.repositories.currency_exchange_settings_repository import (

    CurrencyExchangeSettingsRepository,

)

from app.accounts.currency_exchange_settings_domain.schemas.currency_exchange_settings import (

    CurrencyExchangeSettingsCreate,

    CurrencyExchangeSettingsUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["CurrencyExchangeSettingsService"]





class CurrencyExchangeSettingsService:

    def __init__(self, repository: Optional[CurrencyExchangeSettingsRepository] = None) -> None:

        self.repository = repository or CurrencyExchangeSettingsRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> CurrencyExchangeSettings:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Currency Exchange Settings", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: CurrencyExchangeSettings

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

    ) -> CurrencyExchangeSettings:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[CurrencyExchangeSettings]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[CurrencyExchangeSettings].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_req_params(

        self, business_id: uuid.UUID, row: CurrencyExchangeSettings, items: list[dict]

    ) -> None:

        row.req_params.clear()

        for idx, item in enumerate(items, start=1):

            row.req_params.append(

                CurrencyExchangeSettingsDetails(

                    business_id=business_id,

                    idx=idx,

                    key=item.get('key'),

                    value=item.get('value'),

                )

            )



    def _replace_result_key(

        self, business_id: uuid.UUID, row: CurrencyExchangeSettings, items: list[dict]

    ) -> None:

        row.result_key.clear()

        for idx, item in enumerate(items, start=1):

            row.result_key.append(

                CurrencyExchangeSettingsResult(

                    business_id=business_id,

                    idx=idx,

                    key=item.get('key'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(CurrencyExchangeSettings).where(

                    CurrencyExchangeSettings.business_id == business_id

                )

            )

            or 0

        )

        return f"CUR-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: CurrencyExchangeSettingsCreate

    ) -> CurrencyExchangeSettings:

        row = CurrencyExchangeSettings(

            business_id=business_id,

            name=self.next_name(db, business_id),

            api_endpoint=payload.api_endpoint,

            url=payload.url,

            service_provider=payload.service_provider,

            disabled=payload.disabled,

            access_key=payload.access_key,

            use_http=payload.use_http,

        )

        self._replace_req_params(business_id, row, [x.model_dump() for x in payload.req_params])

        self._replace_result_key(business_id, row, [x.model_dump() for x in payload.result_key])



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

        payload: CurrencyExchangeSettingsUpdate,

    ) -> CurrencyExchangeSettings:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "req_params":

                    self._replace_req_params(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "result_key":

                    self._replace_result_key(business_id, row, value or [])

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
