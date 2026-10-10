"""Business logic for Product Bundle -- port of

``erpnext/selling/doctype/product_bundle/product_bundle.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.selling.product_bundle_domain.models.product_bundle import ProductBundle

from app.selling.product_bundle_domain.repositories.product_bundle_repository import (

    ProductBundleRepository,

)

from app.selling.product_bundle_domain.schemas.product_bundle import (

    ProductBundleCreate,

    ProductBundleUpdate,

)

from app.selling.product_bundle_item_domain.models.product_bundle_item import ProductBundleItem

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ProductBundleService"]





class ProductBundleService:

    def __init__(self, repository: Optional[ProductBundleRepository] = None) -> None:

        self.repository = repository or ProductBundleRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProductBundle:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Product Bundle", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: ProductBundle

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProductBundle:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ProductBundle]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ProductBundle].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(ProductBundle).where(

                    ProductBundle.business_id == business_id

                )

            )

            or 0

        )

        return f"PRO-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: ProductBundleCreate

    ) -> ProductBundle:

        row = ProductBundle(

            business_id=business_id,

            name=self.next_name(db, business_id),

            new_item_code_id=payload.new_item_code_id,

            description=payload.description,

            is_active=payload.is_active,

            disabled=payload.disabled,

            amended_from_id=payload.amended_from_id,

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

        payload: ProductBundleUpdate,

    ) -> ProductBundle:

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

        self, business_id: uuid.UUID, row: ProductBundle, items: list[dict]

    ) -> None:

        row.items.clear()

        for idx, entry in enumerate(items, start=1):

            row.items.append(

                ProductBundleItem(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Product Bundle",

                    parentfield="items",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )
