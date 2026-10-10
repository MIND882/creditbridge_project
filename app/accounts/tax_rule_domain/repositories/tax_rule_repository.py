"""Data access for Tax Rule. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from datetime import date

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.tax_enums import TaxRuleType

from app.accounts.tax_rule_domain.models.tax_rule import TaxRule

from app.core.pagination import normalise_paging



__all__ = ["TaxRuleRepository"]



#: Every column ``validate_filters`` matches on. Upstream builds this as a dict

#: of field -> value and compares each with ``IfNull(col, "") == cstr(value)``,

#: so a NULL and an empty string are the same thing. The tuple keeps the order

#: stable for the caller.

FILTER_COLUMNS = (

    "customer",

    "customer_group",

    "supplier",

    "supplier_group",

    "item",

    "item_group",

    "billing_city",

    "billing_county",

    "billing_state",

    "billing_zipcode",

    "billing_country",

    "shipping_city",

    "shipping_county",

    "shipping_state",

    "shipping_zipcode",

    "shipping_country",

    "tax_category_id",

)





class TaxRuleRepository:

    model = TaxRule



    def get_by_id(

        self, db: Session, business_id: uuid.UUID, rule_id: uuid.UUID

    ) -> Optional[TaxRule]:

        return db.scalar(

            select(TaxRule).where(

                TaxRule.business_id == business_id, TaxRule.id == rule_id

            )

        )



    def next_name(self, db: Session, business_id: uuid.UUID, on: date) -> str:

        """``ACC-TAX-RULE-<year>-<#####>``, counted per tenant per year."""

        count = int(

            db.scalar(

                select(func.count())

                .select_from(TaxRule)

                .where(TaxRule.business_id == business_id)

                .where(TaxRule.name.like(f"ACC-TAX-RULE-{on.year}-%"))

            )

            or 0

        )

        return f"ACC-TAX-RULE-{on.year}-{count + 1:05d}"



    def find_conflict(

        self,

        db: Session,

        business_id: uuid.UUID,

        row: TaxRule,

    ) -> Optional[TaxRule]:

        """

        Port of ``validate_filters``' lookup.



        Upstream finds any other rule whose every filter column matches this one

        -- comparing NULL and "" as equal -- and whose date window overlaps. A

        match at the *same priority* is the conflict, because two rules that tie

        are ambiguous.



        Returning the candidate rather than raising keeps the priority decision

        in the service, where the rest of the validation lives.

        """

        conditions = [

            TaxRule.business_id == business_id,

            TaxRule.id != row.id,

            TaxRule.tax_type == row.tax_type,

        ]



        for column in FILTER_COLUMNS:

            ours = getattr(row, column)

            column_ref = getattr(TaxRule, column)

            # IfNull(col, "") == cstr(value): treat NULL and empty as equal.

            conditions.append(func.coalesce(column_ref, "") == func.coalesce(ours, ""))



        if row.from_date and row.to_date:

            conditions.append(

                ((TaxRule.from_date > row.from_date) & (TaxRule.from_date < row.to_date))

                | ((TaxRule.to_date > row.from_date) & (TaxRule.to_date < row.to_date))

                | ((row.from_date > TaxRule.from_date) & (row.from_date < TaxRule.to_date))

                | ((TaxRule.from_date == row.from_date) & (TaxRule.to_date == row.to_date))

            )

        elif row.from_date:

            conditions.append(TaxRule.to_date > row.from_date)

        elif row.to_date:

            conditions.append(TaxRule.from_date < row.to_date)



        return db.scalar(select(TaxRule).where(*conditions).limit(1))



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        tax_type: Optional[str] = None,

        tax_category_id: Optional[uuid.UUID] = None,

        search: Optional[str] = None,

    ) -> tuple[Sequence[TaxRule], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [TaxRule.business_id == business_id]

        if tax_type is not None:

            conditions.append(TaxRule.tax_type == TaxRuleType(tax_type))

        if tax_category_id is not None:

            conditions.append(TaxRule.tax_category_id == tax_category_id)

        if search:

            like = f"%{search.strip()}%"

            conditions.append(TaxRule.name.ilike(like))



        total = int(

            db.scalar(select(func.count()).select_from(TaxRule).where(*conditions)) or 0

        )

        rows = db.scalars(

            select(TaxRule)

            .where(*conditions)

            .order_by(TaxRule.priority.asc(), TaxRule.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



    def add(self, db: Session, row: TaxRule) -> TaxRule:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: TaxRule) -> None:

        db.delete(row)

        db.flush()
