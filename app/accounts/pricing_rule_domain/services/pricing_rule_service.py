# HAND-WRITTEN

"""

Business logic for Pricing Rule -- port of

``erpnext/accounts/doctype/pricing_rule/pricing_rule.py``.







Upstream hooks:

    validate

    validate_duplicate_apply_on

    validate_template_with_variant

    validate_mandatory

    validate_applicable_for_selling_or_buying

    validate_min_max_qty

    validate_min_max_amt

    validate_recursion

    cleanup_fields_value

    validate_rate_or_discount

    validate_max_discount

    validate_price_list_with_currency

    validate_dates

    validate_condition

    validate_mixed_with_recursion



**Upstream has 8 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.pricing_rule_domain.models.pricing_rule import PricingRule

from app.accounts.pos_invoice_item_domain.models.pos_invoice_item import POSInvoiceItem

from app.accounts.pos_item_group_domain.models.pos_item_group import POSItemGroup

from app.accounts.pricing_rule_brand_domain.models.pricing_rule_brand import PricingRuleBrand

from app.accounts.pricing_rule_domain.repositories.pricing_rule_repository import (

    PricingRuleRepository,

)

from app.accounts.pricing_rule_domain.schemas.pricing_rule import (

    PricingRuleCreate,

    PricingRuleUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PricingRuleService"]





class PricingRuleService:

    def __init__(self, repository: Optional[PricingRuleRepository] = None) -> None:

        self.repository = repository or PricingRuleRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PricingRule:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Pricing Rule", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: PricingRule

    ) -> None:

        """

        TODO(PORT-VALIDATION): upstream validation is NOT ported.



        This controller has **8 ``frappe.throw`` site(s)** upstream.

        None are enforced here, so writes upstream would reject

        currently succeed. It fails open deliberately rather than

        blocking the CRUD surface, but must not be read as complete.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PricingRule:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PricingRule]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PricingRule].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_items(

        self, business_id: uuid.UUID, row: PricingRule, items: list[dict]

    ) -> None:

        row.items.clear()

        for idx, item in enumerate(items, start=1):

            row.items.append(

                PricingRuleItemCode(

                    business_id=business_id,

                    idx=idx,

                    parenttype='Pricing Rule',

                    item_code=item.get('item_code'),

                    uom=item.get('uom'),

                )

            )



    def _replace_item_groups(

        self, business_id: uuid.UUID, row: PricingRule, items: list[dict]

    ) -> None:

        row.item_groups.clear()

        for idx, item in enumerate(items, start=1):

            row.item_groups.append(

                PricingRuleItemGroup(

                    business_id=business_id,

                    idx=idx,

                    parenttype='Pricing Rule',

                    item_group=item.get('item_group'),

                    uom=item.get('uom'),

                )

            )



    def _replace_brands(

        self, business_id: uuid.UUID, row: PricingRule, items: list[dict]

    ) -> None:

        row.brands.clear()

        for idx, item in enumerate(items, start=1):

            row.brands.append(

                PricingRuleBrand(

                    business_id=business_id,

                    idx=idx,

                    parenttype='Pricing Rule',

                    brand=item.get('brand'),

                    uom=item.get('uom'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(PricingRule).where(

                    PricingRule.business_id == business_id

                )

            )

            or 0

        )

        return f"PRI-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: PricingRuleCreate

    ) -> PricingRule:

        row = PricingRule(

            business_id=business_id,

            name=self.next_name(db, business_id),

            title=payload.title,

            disable=payload.disable,

            apply_on=payload.apply_on,

            price_or_product_discount=payload.price_or_product_discount,

            warehouse=payload.warehouse,

            mixed_conditions=payload.mixed_conditions,

            is_cumulative=payload.is_cumulative,

            coupon_code_based=payload.coupon_code_based,

            apply_rule_on_other=payload.apply_rule_on_other,

            other_item_code=payload.other_item_code,

            other_item_group=payload.other_item_group,

            other_brand=payload.other_brand,

            selling=payload.selling,

            buying=payload.buying,

            applicable_for=payload.applicable_for,

            customer=payload.customer,

            customer_group=payload.customer_group,

            territory=payload.territory,

            sales_partner=payload.sales_partner,

            campaign=payload.campaign,

            supplier=payload.supplier,

            supplier_group=payload.supplier_group,

            min_qty=payload.min_qty,

            max_qty=payload.max_qty,

            min_amt=payload.min_amt,

            max_amt=payload.max_amt,

            valid_from=payload.valid_from,

            valid_upto=payload.valid_upto,

            currency=payload.currency,

            margin_type=payload.margin_type,

            margin_rate_or_amount=payload.margin_rate_or_amount,

            rate_or_discount=payload.rate_or_discount,

            apply_discount_on=payload.apply_discount_on,

            rate=payload.rate,

            discount_amount=payload.discount_amount,

            discount_percentage=payload.discount_percentage,

            for_price_list=payload.for_price_list,

            same_item=payload.same_item,

            free_item=payload.free_item,

            free_qty=payload.free_qty,

            free_item_uom=payload.free_item_uom,

            free_item_rate=payload.free_item_rate,

            threshold_percentage=payload.threshold_percentage,

            priority=payload.priority,

            apply_multiple_pricing_rules=payload.apply_multiple_pricing_rules,

            apply_discount_on_rate=payload.apply_discount_on_rate,

            validate_applied_rule=payload.validate_applied_rule,

            rule_description=payload.rule_description,

            promotional_scheme=payload.promotional_scheme,

            condition=payload.condition,

            is_recursive=payload.is_recursive,

            naming_series=payload.naming_series,

            round_free_qty=payload.round_free_qty,

            recurse_for=payload.recurse_for,

            apply_recursion_over=payload.apply_recursion_over,

            has_priority=payload.has_priority,

            dont_enforce_free_item_qty=payload.dont_enforce_free_item_qty,

        )

        self._replace_items(business_id, row, [x.model_dump() for x in payload.items])

        self._replace_item_groups(business_id, row, [x.model_dump() for x in payload.item_groups])

        self._replace_brands(business_id, row, [x.model_dump() for x in payload.brands])



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

        payload: PricingRuleUpdate,

    ) -> PricingRule:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "items":

                    self._replace_items(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "item_groups":

                    self._replace_item_groups(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "brands":

                    self._replace_brands(business_id, row, value or [])

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
