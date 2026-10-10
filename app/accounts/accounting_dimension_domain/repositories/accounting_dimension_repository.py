"""Data access for Accounting Dimension. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.accounting_dimension_domain.models.accounting_dimension import (

    AccountingDimension,

)

from app.core.pagination import normalise_paging



__all__ = ["AccountingDimensionRepository"]





class AccountingDimensionRepository:

    model = AccountingDimension



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, dimension_id: uuid.UUID

    ) -> Optional[AccountingDimension]:

        return db.scalar(

            select(AccountingDimension)

            .options(selectinload(AccountingDimension.dimension_defaults))

            .where(

                AccountingDimension.business_id == business_id,

                AccountingDimension.id == dimension_id,

            )

        )



    def get_by_name(

        self, db: Session, business_id: uuid.UUID, label: str

    ) -> Optional[AccountingDimension]:

        return db.scalar(

            select(AccountingDimension)

            .options(selectinload(AccountingDimension.dimension_defaults))

            .where(

                AccountingDimension.business_id == business_id,

                AccountingDimension.label == label,

            )

        )



    def get_by_fieldname(

        self,

        db: Session,

        business_id: uuid.UUID,

        fieldname: str,

        *,

        exclude_id: Optional[uuid.UUID] = None,

    ) -> Optional[AccountingDimension]:

        """

        Fieldname collisions matter more than label collisions: the fieldname is

        what becomes a column/attribute on transaction doctypes, so two

        dimensions sharing one would write to the same place.

        """

        conditions = [

            AccountingDimension.business_id == business_id,

            AccountingDimension.fieldname == fieldname,

        ]

        if exclude_id is not None:

            conditions.append(AccountingDimension.id != exclude_id)

        return db.scalar(select(AccountingDimension).where(*conditions))



    def list_enabled(self, db: Session, business_id: uuid.UUID) -> list[AccountingDimension]:

        """The active dimensions -- what a transaction form would render."""

        return list(

            db.scalars(

                select(AccountingDimension)

                .options(selectinload(AccountingDimension.dimension_defaults))

                .where(

                    AccountingDimension.business_id == business_id,

                    AccountingDimension.disabled.is_(False),

                )

                .order_by(AccountingDimension.label.asc())

            )

        )



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        search: Optional[str] = None,

        include_disabled: bool = True,

    ) -> tuple[Sequence[AccountingDimension], int]:

        offset, limit = normalise_paging(offset, limit)



        conditions = [AccountingDimension.business_id == business_id]

        if search:

            pattern = f"%{search}%"

            conditions.append(

                AccountingDimension.label.ilike(pattern)

                | AccountingDimension.fieldname.ilike(pattern)

            )

        if not include_disabled:

            conditions.append(AccountingDimension.disabled.is_(False))



        total = int(

            db.scalar(

                select(func.count()).select_from(AccountingDimension).where(*conditions)

            )

            or 0

        )

        rows = db.scalars(

            select(AccountingDimension)

            .options(selectinload(AccountingDimension.dimension_defaults))

            .where(*conditions)

            .order_by(AccountingDimension.label.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



    def add(self, db: Session, dimension: AccountingDimension) -> AccountingDimension:

        db.add(dimension)

        db.flush()

        return dimension



    def delete(self, db: Session, dimension: AccountingDimension) -> None:

        db.delete(dimension)

        db.flush()
