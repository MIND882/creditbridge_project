"""Data access for Sales Taxes and Charges Template. Scoped by ``business_id``."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select, update

from sqlalchemy.orm import Session, selectinload



from app.accounts.sales_taxes_and_charges_template_domain.models.sales_taxes_and_charges_template import (  # noqa: E501

    SalesTaxesAndChargesTemplate,

)

from app.core.pagination import normalise_paging



__all__ = ["SalesTaxesAndChargesTemplateRepository"]





class SalesTaxesAndChargesTemplateRepository:

    model = SalesTaxesAndChargesTemplate



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks conftest

        # collection with "failed to locate a name".

        return [selectinload(SalesTaxesAndChargesTemplate.taxes)]



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, template_id: uuid.UUID

    ) -> Optional[SalesTaxesAndChargesTemplate]:

        return db.scalar(

            select(SalesTaxesAndChargesTemplate)

            .where(

                SalesTaxesAndChargesTemplate.business_id == business_id,

                SalesTaxesAndChargesTemplate.id == template_id,

            )

            .options(*self._options())

        )



    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[SalesTaxesAndChargesTemplate]:

        return db.scalar(

            select(SalesTaxesAndChargesTemplate)

            .where(

                SalesTaxesAndChargesTemplate.business_id == business_id,

                SalesTaxesAndChargesTemplate.name == name,

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

        Port of ``validate_for_tax_category``'s existence check.



        Upstream allows only one *enabled* template per tax category; a disabled

        one does not block, which is what makes the rule survivable.

        """

        conditions = [

            SalesTaxesAndChargesTemplate.business_id == business_id,

            SalesTaxesAndChargesTemplate.tax_category_id == tax_category_id,

            SalesTaxesAndChargesTemplate.disabled.is_(False),

        ]

        if except_id is not None:

            conditions.append(SalesTaxesAndChargesTemplate.id != except_id)

        return (

            db.scalar(

                select(SalesTaxesAndChargesTemplate.id).where(*conditions)

            )

            is not None

        )



    def clear_default(

        self, db: Session, business_id: uuid.UUID, except_id: Optional[uuid.UUID]

    ) -> None:

        """Port of the ``frappe.qb.update`` half of the template validator."""

        conditions = [

            SalesTaxesAndChargesTemplate.business_id == business_id,

            SalesTaxesAndChargesTemplate.is_default.is_(True),

        ]

        if except_id is not None:

            conditions.append(SalesTaxesAndChargesTemplate.id != except_id)

        db.execute(

            update(SalesTaxesAndChargesTemplate).where(*conditions).values(is_default=False)

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

    ) -> tuple[Sequence[SalesTaxesAndChargesTemplate], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SalesTaxesAndChargesTemplate.business_id == business_id]

        if not include_disabled:

            conditions.append(SalesTaxesAndChargesTemplate.disabled.is_(False))

        if tax_category_id is not None:

            conditions.append(

                SalesTaxesAndChargesTemplate.tax_category_id == tax_category_id

            )

        if search:

            like = f"%{search.strip()}%"

            conditions.append(

                SalesTaxesAndChargesTemplate.name.ilike(like)

                | SalesTaxesAndChargesTemplate.title.ilike(like)

            )



        total = int(

            db.scalar(

                select(func.count())

                .select_from(SalesTaxesAndChargesTemplate)

                .where(*conditions)

            )

            or 0

        )

        rows = db.scalars(

            select(SalesTaxesAndChargesTemplate)

            .where(*conditions)

            .order_by(SalesTaxesAndChargesTemplate.name.asc())

            .offset(offset)

            .limit(limit)

            .options(*self._options())

        ).all()

        return rows, total



    def add(

        self, db: Session, row: SalesTaxesAndChargesTemplate

    ) -> SalesTaxesAndChargesTemplate:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: SalesTaxesAndChargesTemplate) -> None:

        db.delete(row)

        db.flush()
