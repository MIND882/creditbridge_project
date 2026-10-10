"""Business logic for Sales Forecast -- port of

``erpnext/manufacturing/doctype/sales_forecast/sales_forecast.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.sales_forecast_domain.models.sales_forecast import SalesForecast

from app.manufacturing.sales_forecast_domain.repositories.sales_forecast_repository import (

    SalesForecastRepository,

)

from app.manufacturing.sales_forecast_domain.schemas.sales_forecast import (

    SalesForecastCreate,

    SalesForecastUpdate,

)

from app.manufacturing.sales_forecast_item_domain.models.sales_forecast_item import SalesForecastItem

from app.manufacturing.sales_forecast_item_domain.models.sales_forecast_item import SalesForecastItem

from app.core.errors import NotFoundError

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.pagination import ResultPage



__all__ = ["SalesForecastService"]





class SalesForecastService:

    def __init__(self, repository: Optional[SalesForecastRepository] = None) -> None:

        self.repository = repository or SalesForecastRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SalesForecast:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Sales Forecast", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: SalesForecast

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SalesForecast:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[SalesForecast]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SalesForecast].build(

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

                select(func.count()).select_from(SalesForecast).where(

                    SalesForecast.business_id == business_id

                )

            )

            or 0

        )

        return f"{prefix}{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: SalesForecastCreate

    ) -> SalesForecast:

        row = SalesForecast(

            business_id=business_id,

            name=self.next_name(db, business_id, payload.naming_series),

            naming_series=payload.naming_series,

            company=payload.company,

            posting_date=payload.posting_date,

            from_date=payload.from_date,

            frequency=payload.frequency,

            demand_number=payload.demand_number,

            parent_warehouse_id=payload.parent_warehouse_id,

            amended_from_id=payload.amended_from_id,

            status=payload.status,

        )

        self._replace_selected_items(business_id, row, [x.model_dump() for x in payload.selected_items])

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

        payload: SalesForecastUpdate,

    ) -> SalesForecast:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "selected_items":

                    self._replace_selected_items(business_id, row, value or [])

                    continue

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



    def submit(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SalesForecast:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Sales Forecast")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SalesForecast:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Sales Forecast")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row



    def _replace_selected_items(

        self, business_id: uuid.UUID, row: SalesForecast, selected_items: list[dict]

    ) -> None:

        row.selected_items.clear()

        for idx, entry in enumerate(selected_items, start=1):

            row.selected_items.append(

                SalesForecastItem(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Sales Forecast",

                    parentfield="selected_items",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_items(

        self, business_id: uuid.UUID, row: SalesForecast, items: list[dict]

    ) -> None:

        row.items.clear()

        for idx, entry in enumerate(items, start=1):

            row.items.append(

                SalesForecastItem(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Sales Forecast",

                    parentfield="items",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )
