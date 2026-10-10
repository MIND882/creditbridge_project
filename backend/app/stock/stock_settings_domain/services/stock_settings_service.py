"""Business logic for Stock Settings -- port of

``erpnext/stock/doctype/stock_settings/stock_settings.py``.



Upstream has 6 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.stock.stock_settings_domain.models.stock_settings import StockSettings

from app.stock.stock_settings_domain.repositories.stock_settings_repository import (

    StockSettingsRepository,

)

from app.stock.stock_settings_domain.schemas.stock_settings import (

    StockSettingsUpdate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["StockSettingsService"]





class StockSettingsService:

    def __init__(self, repository: Optional[StockSettingsRepository] = None) -> None:

        self.repository = repository or StockSettingsRepository()





    def get_or_create(

        self, db: Session, business_id: uuid.UUID

    ) -> StockSettings:

        """The tenant's settings row, created with upstream defaults on first read."""

        row = self.repository.get_for_business(db, business_id)

        if row is None:

            row = StockSettings(business_id=business_id)

            try:

                self.repository.add(db, row)

                db.commit()

            except Exception:

                db.rollback()

                raise

            db.refresh(row)

        return row



    def update(

        self, db: Session, business_id: uuid.UUID, payload: StockSettingsUpdate

    ) -> StockSettings:

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
