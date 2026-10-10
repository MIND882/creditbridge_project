"""Data access for Item Tax Template. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.item_tax_template_domain.models.item_tax_template import ItemTaxTemplate

from app.core.pagination import normalise_paging



__all__ = ["ItemTaxTemplateRepository"]





class ItemTaxTemplateRepository:

    model = ItemTaxTemplate



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks conftest

        # collection with "failed to locate a name".

        return [selectinload(ItemTaxTemplate.taxes)]



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, template_id: uuid.UUID

    ) -> Optional[ItemTaxTemplate]:

        return db.scalar(

            select(ItemTaxTemplate)

            .where(

                ItemTaxTemplate.business_id == business_id,

                ItemTaxTemplate.id == template_id,

            )

            .options(*self._options())

        )



    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ItemTaxTemplate]:

        return db.scalar(

            select(ItemTaxTemplate)

            .where(

                ItemTaxTemplate.business_id == business_id,

                ItemTaxTemplate.name == name,

            )

            .options(*self._options())

        )



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        include_disabled: bool = True,

        search: Optional[str] = None,

    ) -> tuple[Sequence[ItemTaxTemplate], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ItemTaxTemplate.business_id == business_id]

        if not include_disabled:

            conditions.append(ItemTaxTemplate.disabled.is_(False))

        if search:

            like = f"%{search.strip()}%"

            conditions.append(

                ItemTaxTemplate.name.ilike(like) | ItemTaxTemplate.title.ilike(like)

            )



        total = int(

            db.scalar(select(func.count()).select_from(ItemTaxTemplate).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ItemTaxTemplate)

            .where(*conditions)

            .order_by(ItemTaxTemplate.name.asc())

            .offset(offset)

            .limit(limit)

            .options(*self._options())

        ).all()

        return rows, total



    def add(self, db: Session, row: ItemTaxTemplate) -> ItemTaxTemplate:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: ItemTaxTemplate) -> None:

        db.delete(row)

        db.flush()
