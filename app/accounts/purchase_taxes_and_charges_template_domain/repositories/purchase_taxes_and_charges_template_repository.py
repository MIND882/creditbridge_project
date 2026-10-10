"""Data access for Purchase Taxes and Charges Template. Scoped by ``business_id``."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select, update

from sqlalchemy.orm import Session, selectinload



from app.accounts.purchase_taxes_and_charges_template_domain.models.purchase_taxes_and_charges_template import (  # noqa: E501

    PurchaseTaxesAndChargesTemplate,

)

from app.core.pagination import normalise_paging



__all__ = ["PurchaseTaxesAndChargesTemplateRepository"]





class PurchaseTaxesAndChargesTemplateRepository:

    model = PurchaseTaxesAndChargesTemplate



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks conftest

        # collection with "failed to locate a name".

        return [selectinload(PurchaseTaxesAndChargesTemplate.taxes)]



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, template_id: uuid.UUID

    ) -> Optional[PurchaseTaxesAndChargesTemplate]:

        return db.scalar(

            select(PurchaseTaxesAndChargesTemplate)

            .where(

                PurchaseTaxesAndChargesTemplate.business_id == business_id,

                PurchaseTaxesAndChargesTemplate.id == template_id,

            )

            .options(*self._options())

        )



    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[PurchaseTaxesAndChargesTemplate]:

        return db.scalar(

            select(PurchaseTaxesAndChargesTemplate)

            .where(

                PurchaseTaxesAndChargesTemplate.business_id == business_id,

                PurchaseTaxesAndChargesTemplate.name == name,

            )

            .options(*self._options())

        )



    def exists_enabled_for_tax_category(

        self,

        db: Session,

        business_id: uuid.UUID,

        tax_category_id: uuid.UUID,

        except_id: Optional[uuid.UUID],

    ) -> bool:

        """

        Only one *enabled* template per tax category. Mirrors the sales

        repository: the two templates share the rule, not the implementation.

        """

        conditions = [

            PurchaseTaxesAndChargesTemplate.business_id == business_id,

            PurchaseTaxesAndChargesTemplate.tax_category_id == tax_category_id,

            PurchaseTaxesAndChargesTemplate.disabled.is_(False),

        ]

        if except_id is not None:

            conditions.append(PurchaseTaxesAndChargesTemplate.id != except_id)

        return (

            db.scalar(select(PurchaseTaxesAndChargesTemplate.id).where(*conditions))

            is not None

        )



    def clear_default(

        self, db: Session, business_id: uuid.UUID, except_id: Optional[uuid.UUID]

    ) -> None:

        conditions = [

            PurchaseTaxesAndChargesTemplate.business_id == business_id,

            PurchaseTaxesAndChargesTemplate.is_default.is_(True),

        ]

        if except_id is not None:

            conditions.append(PurchaseTaxesAndChargesTemplate.id != except_id)

        db.execute(

            update(PurchaseTaxesAndChargesTemplate)

            .where(*conditions)

            .values(is_default=False)

        )

        db.flush()



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        include_disabled: bool = True,

        tax_category_id: Optional[uuid.UUID] = None,

        search: Optional[str] = None,

    ) -> tuple[Sequence[PurchaseTaxesAndChargesTemplate], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PurchaseTaxesAndChargesTemplate.business_id == business_id]

        if not include_disabled:

            conditions.append(PurchaseTaxesAndChargesTemplate.disabled.is_(False))

        if tax_category_id is not None:

            conditions.append(

                PurchaseTaxesAndChargesTemplate.tax_category_id == tax_category_id

            )

        if search:

            like = f"%{search.strip()}%"

            conditions.append(

                PurchaseTaxesAndChargesTemplate.name.ilike(like)

                | PurchaseTaxesAndChargesTemplate.title.ilike(like)

            )



        total = int(

            db.scalar(

                select(func.count())

                .select_from(PurchaseTaxesAndChargesTemplate)

                .where(*conditions)

            )

            or 0

        )

        rows = db.scalars(

            select(PurchaseTaxesAndChargesTemplate)

            .where(*conditions)

            .order_by(PurchaseTaxesAndChargesTemplate.name.asc())

            .offset(offset)

            .limit(limit)

            .options(*self._options())

        ).all()

        return rows, total



    def add(

        self, db: Session, row: PurchaseTaxesAndChargesTemplate

    ) -> PurchaseTaxesAndChargesTemplate:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: PurchaseTaxesAndChargesTemplate) -> None:

        db.delete(row)

        db.flush()
