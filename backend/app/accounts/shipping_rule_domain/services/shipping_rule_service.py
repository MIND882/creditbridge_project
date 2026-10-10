# HAND-WRITTEN

"""

Business logic for Shipping Rule -- port of

``erpnext/accounts/doctype/shipping_rule/shipping_rule.py``.







Upstream hooks:

    validate

    validate_from_to_values

    apply

    get_shipping_amount_from_rules

    validate_countries

    add_shipping_rule_to_tax_table

    sort_shipping_rule_conditions

    validate_overlapping_shipping_rule_conditions



**Upstream has 4 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.shipping_rule_domain.models.shipping_rule import ShippingRule

from app.accounts.shipping_rule_condition_domain.models.shipping_rule_condition import ShippingRuleCondition

from app.accounts.shipping_rule_country_domain.models.shipping_rule_country import ShippingRuleCountry

from app.accounts.shipping_rule_domain.repositories.shipping_rule_repository import (

    ShippingRuleRepository,

)

from app.accounts.shipping_rule_domain.schemas.shipping_rule import (

    ShippingRuleCreate,

    ShippingRuleUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ShippingRuleService"]





class ShippingRuleService:

    def __init__(self, repository: Optional[ShippingRuleRepository] = None) -> None:

        self.repository = repository or ShippingRuleRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ShippingRule:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Shipping Rule", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: ShippingRule

    ) -> None:

        """

        TODO(PORT-VALIDATION): upstream validation is NOT ported.



        This controller has **4 ``frappe.throw`` site(s)** upstream.

        None are enforced here, so writes upstream would reject

        currently succeed. It fails open deliberately rather than

        blocking the CRUD surface, but must not be read as complete.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ShippingRule:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ShippingRule]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ShippingRule].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_conditions(

        self, business_id: uuid.UUID, row: ShippingRule, items: list[dict]

    ) -> None:

        row.conditions.clear()

        for idx, item in enumerate(items, start=1):

            row.conditions.append(

                ShippingRuleCondition(

                    business_id=business_id,

                    idx=idx,

                    from_value=item.get('from_value'),

                    to_value=item.get('to_value'),

                    shipping_amount=item.get('shipping_amount'),

                )

            )



    def _replace_countries(

        self, business_id: uuid.UUID, row: ShippingRule, items: list[dict]

    ) -> None:

        row.countries.clear()

        for idx, item in enumerate(items, start=1):

            row.countries.append(

                ShippingRuleCountry(

                    business_id=business_id,

                    idx=idx,

                    country=item.get('country'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(ShippingRule).where(

                    ShippingRule.business_id == business_id

                )

            )

            or 0

        )

        return f"SHI-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: ShippingRuleCreate

    ) -> ShippingRule:

        row = ShippingRule(

            business_id=business_id,

            name=self.next_name(db, business_id),

            label=payload.label,

            disabled=payload.disabled,

            shipping_rule_type=payload.shipping_rule_type,

            account_id=payload.account_id,

            cost_center_id=payload.cost_center_id,

            calculate_based_on=payload.calculate_based_on,

            shipping_amount=payload.shipping_amount,

            project=payload.project,

        )

        self._replace_conditions(business_id, row, [x.model_dump() for x in payload.conditions])

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

        payload: ShippingRuleUpdate,

    ) -> ShippingRule:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "conditions":

                    self._replace_conditions(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "countries":

                    self._replace_countries(business_id, row, value or [])

                else:

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
