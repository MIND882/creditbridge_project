"""Business logic for Price List -- port of

``erpnext/stock/doctype/price_list/price_list.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.price_list_domain.models.price_list import PriceList

from app.stock.price_list_domain.repositories.price_list_repository import (

    PriceListRepository,

)

from app.stock.price_list_domain.schemas.price_list import (

    PriceListCreate,

    PriceListUpdate,

)

from app.stock.price_list_country_domain.models.price_list_country import PriceListCountry

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PriceListService"]





class PriceListService:

    def __init__(self, repository: Optional[PriceListRepository] = None) -> None:

        self.repository = repository or PriceListRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PriceList:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Price List", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: PriceList

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PriceList:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PriceList]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PriceList].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    # ``autoname = 'field:price_list_name'``: the name is the value of

    # that field, derived at create time (Frappe derives it on every save;

    # the creation-time value is what migrated documents carry).



    def create(

        self, db: Session, business_id: uuid.UUID, payload: PriceListCreate

    ) -> PriceList:

        row = PriceList(

            business_id=business_id,

            name=payload.price_list_name,

            enabled=payload.enabled,

            price_list_name=payload.price_list_name,

            currency=payload.currency,

            buying=payload.buying,

            selling=payload.selling,

            price_not_uom_dependent=payload.price_not_uom_dependent,

        )

        self._replace_countries(business_id, row, [x.model_dump() for x in payload.countries])



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

        payload: PriceListUpdate,

    ) -> PriceList:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "countries":

                    self._replace_countries(business_id, row, value or [])

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



    def _replace_countries(

        self, business_id: uuid.UUID, row: PriceList, countries: list[dict]

    ) -> None:

        row.countries.clear()

        for idx, entry in enumerate(countries, start=1):

            row.countries.append(

                PriceListCountry(

                    business_id=business_id,

                    idx=idx,

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )
