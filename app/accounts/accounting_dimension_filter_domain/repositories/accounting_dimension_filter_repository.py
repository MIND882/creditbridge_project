"""Data access for Accounting Dimension Filter. Scoped by ``business_id``."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.accounting_dimension_filter_domain.models.accounting_dimension_filter import (

    AccountingDimensionFilter,

)

from app.core.pagination import normalise_paging



__all__ = ["AccountingDimensionFilterRepository"]





class AccountingDimensionFilterRepository:

    model = AccountingDimensionFilter



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, filter_id: uuid.UUID

    ) -> Optional[AccountingDimensionFilter]:

        return db.scalar(

            select(AccountingDimensionFilter)

            .options(

                selectinload(AccountingDimensionFilter.accounts),

                selectinload(AccountingDimensionFilter.dimensions),

            )

            .where(

                AccountingDimensionFilter.business_id == business_id,

                AccountingDimensionFilter.id == filter_id,

            )

        )



    def next_name(self, db: Session, business_id: uuid.UUID, dimension: str) -> str:

        """

        ``format:{accounting_dimension}-{#####}``, counter scoped per tenant.



        Counted across *all* the tenant's filters rather than per dimension, so

        the number stays unique within the table even if two filters target the

        same dimension.

        """

        count = int(

            db.scalar(

                select(func.count())

                .select_from(AccountingDimensionFilter)

                .where(AccountingDimensionFilter.business_id == business_id)

            )

            or 0

        )

        return f"{dimension}-{count + 1:05d}"



    def list_for_account(

        self, db: Session, business_id: uuid.UUID, account_id: uuid.UUID

    ) -> list[AccountingDimensionFilter]:

        """

        Every enabled filter governing one account.



        This is the query a transaction save would run to decide whether a

        chosen dimension value is permitted.

        """

        from app.accounts.applicable_on_account_domain.models.applicable_on_account import (

            ApplicableOnAccount,

        )



        rows = db.scalars(

            select(AccountingDimensionFilter)

            .options(

                selectinload(AccountingDimensionFilter.accounts),

                selectinload(AccountingDimensionFilter.dimensions),

            )

            .join(ApplicableOnAccount, ApplicableOnAccount.parent_id == AccountingDimensionFilter.id)

            .where(

                AccountingDimensionFilter.business_id == business_id,

                AccountingDimensionFilter.disabled.is_(False),

                ApplicableOnAccount.account_id == account_id,

            )

        ).all()

        # A filter can match the join more than once if an account appears twice.

        return list({row.id: row for row in rows}.values())



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        accounting_dimension: Optional[str] = None,

        include_disabled: bool = True,

    ) -> tuple[Sequence[AccountingDimensionFilter], int]:

        offset, limit = normalise_paging(offset, limit)



        conditions = [AccountingDimensionFilter.business_id == business_id]

        if accounting_dimension:

            conditions.append(

                AccountingDimensionFilter.accounting_dimension == accounting_dimension

            )

        if not include_disabled:

            conditions.append(AccountingDimensionFilter.disabled.is_(False))



        total = int(

            db.scalar(

                select(func.count())

                .select_from(AccountingDimensionFilter)

                .where(*conditions)

            )

            or 0

        )

        rows = db.scalars(

            select(AccountingDimensionFilter)

            .options(

                selectinload(AccountingDimensionFilter.accounts),

                selectinload(AccountingDimensionFilter.dimensions),

            )

            .where(*conditions)

            .order_by(AccountingDimensionFilter.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



    def add(

        self, db: Session, dimension_filter: AccountingDimensionFilter

    ) -> AccountingDimensionFilter:

        db.add(dimension_filter)

        db.flush()

        return dimension_filter



    def delete(self, db: Session, dimension_filter: AccountingDimensionFilter) -> None:

        db.delete(dimension_filter)

        db.flush()
