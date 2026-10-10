"""

Data access for Account Category.



Every statement filters on ``business_id`` without exception -- there is no

code path in this module that reads or writes another tenant's rows.

"""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.account_category_domain.models.account_category import AccountCategory

from app.core.pagination import normalise_paging



__all__ = ["AccountCategoryRepository"]





class AccountCategoryRepository:

    """Thin, tenancy-scoped query surface. No business rules live here."""



    model = AccountCategory



    # ── reads ────────────────────────────────────────────────────────────────

    def get_by_id(self, db: Session, business_id: uuid.UUID, category_id: uuid.UUID) -> Optional[AccountCategory]:

        return db.scalar(

            select(AccountCategory).where(

                AccountCategory.business_id == business_id,

                AccountCategory.id == category_id,

            )

        )



    def get_by_name(

        self, db: Session, business_id: uuid.UUID, account_category_name: str

    ) -> Optional[AccountCategory]:

        """Lookup by the human label -- the ERPNext ``frappe.get_doc`` equivalent."""

        return db.scalar(

            select(AccountCategory).where(

                AccountCategory.business_id == business_id,

                AccountCategory.account_category_name == account_category_name,

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

        root_type: Optional[str] = None,

    ) -> tuple[Sequence[AccountCategory], int]:

        """Page of rows plus the unfiltered-by-paging total, for the envelope."""

        offset, limit = normalise_paging(offset, limit)



        conditions = [AccountCategory.business_id == business_id]

        if search:

            conditions.append(AccountCategory.account_category_name.ilike(f"%{search}%"))

        if root_type:

            conditions.append(AccountCategory.root_type == root_type)



        total = int(

            db.scalar(

                select(func.count()).select_from(AccountCategory).where(*conditions)

            )

            or 0

        )

        rows = db.scalars(

            select(AccountCategory)

            .where(*conditions)

            .order_by(AccountCategory.account_category_name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



    def list_all_names(self, db: Session, business_id: uuid.UUID) -> list[str]:

        """Every label for the tenant -- used by the bulk-import guard."""

        return list(

            db.scalars(

                select(AccountCategory.account_category_name).where(

                    AccountCategory.business_id == business_id

                )

            )

        )



    # ── writes ───────────────────────────────────────────────────────────────

    def add(self, db: Session, category: AccountCategory) -> AccountCategory:

        db.add(category)

        db.flush()

        return category



    def delete(self, db: Session, category: AccountCategory) -> None:

        db.delete(category)

        db.flush()
