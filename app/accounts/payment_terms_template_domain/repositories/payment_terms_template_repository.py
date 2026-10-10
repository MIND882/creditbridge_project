"""Data access for Payment Terms Template. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.payment_terms_template_domain.models.payment_terms_template import (

    PaymentTermsTemplate,

)

from app.core.pagination import normalise_paging



__all__ = ["PaymentTermsTemplateRepository"]





class PaymentTermsTemplateRepository:

    model = PaymentTermsTemplate



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks conftest

        # collection with "failed to locate a name".

        return [selectinload(PaymentTermsTemplate.terms)]



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, template_id: uuid.UUID

    ) -> Optional[PaymentTermsTemplate]:

        return db.scalar(

            select(PaymentTermsTemplate)

            .where(

                PaymentTermsTemplate.business_id == business_id,

                PaymentTermsTemplate.id == template_id,

            )

            .options(*self._options())

        )



    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[PaymentTermsTemplate]:

        return db.scalar(

            select(PaymentTermsTemplate)

            .where(

                PaymentTermsTemplate.business_id == business_id,

                PaymentTermsTemplate.name == name,

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

        search: Optional[str] = None,

    ) -> tuple[Sequence[PaymentTermsTemplate], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PaymentTermsTemplate.business_id == business_id]

        if search:

            like = f"%{search.strip()}%"

            conditions.append(

                PaymentTermsTemplate.name.ilike(like)

                | PaymentTermsTemplate.template_name.ilike(like)

            )



        total = int(

            db.scalar(

                select(func.count()).select_from(PaymentTermsTemplate).where(*conditions)

            )

            or 0

        )

        rows = db.scalars(

            select(PaymentTermsTemplate)

            .where(*conditions)

            .order_by(PaymentTermsTemplate.name.asc())

            .offset(offset)

            .limit(limit)

            .options(*self._options())

        ).all()

        return rows, total



    def add(self, db: Session, row: PaymentTermsTemplate) -> PaymentTermsTemplate:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: PaymentTermsTemplate) -> None:

        db.delete(row)

        db.flush()
