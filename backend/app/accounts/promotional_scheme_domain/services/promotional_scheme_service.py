# HAND-WRITTEN

"""

Business logic for Promotional Scheme -- port of

``erpnext/accounts/doctype/promotional_scheme/promotional_scheme.py``.







Upstream hooks:

    validate

    validate_applicable_for

    validate_pricing_rules

    get_invalid_pricing_rules

    on_update

    validate_mixed_with_recursion

    update_pricing_rules

    on_trash



**Upstream has 5 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.promotional_scheme_domain.models.promotional_scheme import PromotionalScheme

from app.accounts.pos_invoice_item_domain.models.pos_invoice_item import POSInvoiceItem

from app.accounts.pos_item_group_domain.models.pos_item_group import POSItemGroup

from app.accounts.pricing_rule_brand_domain.models.pricing_rule_brand import PricingRuleBrand

from app.accounts.customer_item_domain.models.customer_item import CustomerItem

from app.accounts.customer_group_item_domain.models.customer_group_item import CustomerGroupItem

from app.accounts.territory_item_domain.models.territory_item import TerritoryItem

from app.accounts.sales_partner_item_domain.models.sales_partner_item import SalesPartnerItem

from app.accounts.campaign_item_domain.models.campaign_item import CampaignItem

from app.accounts.supplier_item_domain.models.supplier_item import SupplierItem

from app.accounts.supplier_group_item_domain.models.supplier_group_item import SupplierGroupItem

from app.accounts.promotional_scheme_price_discount_domain.models.promotional_scheme_price_discount import PromotionalSchemePriceDiscount

from app.accounts.promotional_scheme_product_discount_domain.models.promotional_scheme_product_discount import PromotionalSchemeProductDiscount

from app.accounts.promotional_scheme_domain.repositories.promotional_scheme_repository import (

    PromotionalSchemeRepository,

)

from app.accounts.promotional_scheme_domain.schemas.promotional_scheme import (

    PromotionalSchemeCreate,

    PromotionalSchemeUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PromotionalSchemeService"]





class PromotionalSchemeService:

    def __init__(self, repository: Optional[PromotionalSchemeRepository] = None) -> None:

        self.repository = repository or PromotionalSchemeRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PromotionalScheme:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Promotional Scheme", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: PromotionalScheme

    ) -> None:

        """

        TODO(PORT-VALIDATION): upstream validation is NOT ported.



        This controller has **5 ``frappe.throw`` site(s)** upstream.

        None are enforced here, so writes upstream would reject

        currently succeed. It fails open deliberately rather than

        blocking the CRUD surface, but must not be read as complete.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PromotionalScheme:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PromotionalScheme]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PromotionalScheme].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_items(

        self, business_id: uuid.UUID, row: PromotionalScheme, items: list[dict]

    ) -> None:

        row.items.clear()

        for idx, item in enumerate(items, start=1):

            row.items.append(

                PricingRuleItemCode(

                    business_id=business_id,

                    idx=idx,

                    parenttype='Promotional Scheme',

                    item_code=item.get('item_code'),

                    uom=item.get('uom'),

                )

            )



    def _replace_item_groups(

        self, business_id: uuid.UUID, row: PromotionalScheme, items: list[dict]

    ) -> None:

        row.item_groups.clear()

        for idx, item in enumerate(items, start=1):

            row.item_groups.append(

                PricingRuleItemGroup(

                    business_id=business_id,

                    idx=idx,

                    parenttype='Promotional Scheme',

                    item_group=item.get('item_group'),

                    uom=item.get('uom'),

                )

            )



    def _replace_brands(

        self, business_id: uuid.UUID, row: PromotionalScheme, items: list[dict]

    ) -> None:

        row.brands.clear()

        for idx, item in enumerate(items, start=1):

            row.brands.append(

                PricingRuleBrand(

                    business_id=business_id,

                    idx=idx,

                    parenttype='Promotional Scheme',

                    brand=item.get('brand'),

                    uom=item.get('uom'),

                )

            )



    def _replace_customer(

        self, business_id: uuid.UUID, row: PromotionalScheme, items: list[dict]

    ) -> None:

        row.customer.clear()

        for idx, item in enumerate(items, start=1):

            row.customer.append(

                CustomerItem(

                    business_id=business_id,

                    idx=idx,

                    customer=item.get('customer'),

                )

            )



    def _replace_customer_group(

        self, business_id: uuid.UUID, row: PromotionalScheme, items: list[dict]

    ) -> None:

        row.customer_group.clear()

        for idx, item in enumerate(items, start=1):

            row.customer_group.append(

                CustomerGroupItem(

                    business_id=business_id,

                    idx=idx,

                    customer_group=item.get('customer_group'),

                )

            )



    def _replace_territory(

        self, business_id: uuid.UUID, row: PromotionalScheme, items: list[dict]

    ) -> None:

        row.territory.clear()

        for idx, item in enumerate(items, start=1):

            row.territory.append(

                TerritoryItem(

                    business_id=business_id,

                    idx=idx,

                    territory=item.get('territory'),

                )

            )



    def _replace_sales_partner(

        self, business_id: uuid.UUID, row: PromotionalScheme, items: list[dict]

    ) -> None:

        row.sales_partner.clear()

        for idx, item in enumerate(items, start=1):

            row.sales_partner.append(

                SalesPartnerItem(

                    business_id=business_id,

                    idx=idx,

                    sales_partner=item.get('sales_partner'),

                )

            )



    def _replace_campaign(

        self, business_id: uuid.UUID, row: PromotionalScheme, items: list[dict]

    ) -> None:

        row.campaign.clear()

        for idx, item in enumerate(items, start=1):

            row.campaign.append(

                CampaignItem(

                    business_id=business_id,

                    idx=idx,

                    campaign=item.get('campaign'),

                )

            )



    def _replace_supplier(

        self, business_id: uuid.UUID, row: PromotionalScheme, items: list[dict]

    ) -> None:

        row.supplier.clear()

        for idx, item in enumerate(items, start=1):

            row.supplier.append(

                SupplierItem(

                    business_id=business_id,

                    idx=idx,

                    supplier=item.get('supplier'),

                )

            )



    def _replace_supplier_group(

        self, business_id: uuid.UUID, row: PromotionalScheme, items: list[dict]

    ) -> None:

        row.supplier_group.clear()

        for idx, item in enumerate(items, start=1):

            row.supplier_group.append(

                SupplierGroupItem(

                    business_id=business_id,

                    idx=idx,

                    supplier_group=item.get('supplier_group'),

                )

            )



    def _replace_price_discount_slabs(

        self, business_id: uuid.UUID, row: PromotionalScheme, items: list[dict]

    ) -> None:

        row.price_discount_slabs.clear()

        for idx, item in enumerate(items, start=1):

            row.price_discount_slabs.append(

                PromotionalSchemePriceDiscount(

                    business_id=business_id,

                    idx=idx,

                    disable=item.get('disable'),

                    rule_description=item.get('rule_description'),

                    min_qty=item.get('min_qty'),

                    max_qty=item.get('max_qty'),

                    min_amount=item.get('min_amount'),

                    max_amount=item.get('max_amount'),

                    rate_or_discount=item.get('rate_or_discount'),

                    rate=item.get('rate'),

                    discount_amount=item.get('discount_amount'),

                    discount_percentage=item.get('discount_percentage'),

                    for_price_list=item.get('for_price_list'),

                    warehouse=item.get('warehouse'),

                    threshold_percentage=item.get('threshold_percentage'),

                    validate_applied_rule=item.get('validate_applied_rule'),

                    priority=item.get('priority'),

                    apply_multiple_pricing_rules=item.get('apply_multiple_pricing_rules'),

                    apply_discount_on_rate=item.get('apply_discount_on_rate'),

                )

            )



    def _replace_product_discount_slabs(

        self, business_id: uuid.UUID, row: PromotionalScheme, items: list[dict]

    ) -> None:

        row.product_discount_slabs.clear()

        for idx, item in enumerate(items, start=1):

            row.product_discount_slabs.append(

                PromotionalSchemeProductDiscount(

                    business_id=business_id,

                    idx=idx,

                    disable=item.get('disable'),

                    rule_description=item.get('rule_description'),

                    min_qty=item.get('min_qty'),

                    max_qty=item.get('max_qty'),

                    min_amount=item.get('min_amount'),

                    max_amount=item.get('max_amount'),

                    same_item=item.get('same_item'),

                    free_item=item.get('free_item'),

                    free_qty=item.get('free_qty'),

                    free_item_uom=item.get('free_item_uom'),

                    free_item_rate=item.get('free_item_rate'),

                    warehouse=item.get('warehouse'),

                    threshold_percentage=item.get('threshold_percentage'),

                    priority=item.get('priority'),

                    apply_multiple_pricing_rules=item.get('apply_multiple_pricing_rules'),

                    is_recursive=item.get('is_recursive'),

                    recurse_for=item.get('recurse_for'),

                    apply_recursion_over=item.get('apply_recursion_over'),

                    round_free_qty=item.get('round_free_qty'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(PromotionalScheme).where(

                    PromotionalScheme.business_id == business_id

                )

            )

            or 0

        )

        return f"PRO-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: PromotionalSchemeCreate

    ) -> PromotionalScheme:

        row = PromotionalScheme(

            business_id=business_id,

            name=self.next_name(db, business_id),

            apply_on=payload.apply_on,

            disable=payload.disable,

            mixed_conditions=payload.mixed_conditions,

            is_cumulative=payload.is_cumulative,

            apply_rule_on_other=payload.apply_rule_on_other,

            other_item_code=payload.other_item_code,

            other_item_group=payload.other_item_group,

            other_brand=payload.other_brand,

            selling=payload.selling,

            buying=payload.buying,

            applicable_for=payload.applicable_for,

            valid_from=payload.valid_from,

            valid_upto=payload.valid_upto,

            currency=payload.currency,

        )

        self._replace_items(business_id, row, [x.model_dump() for x in payload.items])

        self._replace_item_groups(business_id, row, [x.model_dump() for x in payload.item_groups])

        self._replace_brands(business_id, row, [x.model_dump() for x in payload.brands])

        self._replace_customer(business_id, row, [x.model_dump() for x in payload.customer])

        self._replace_customer_group(business_id, row, [x.model_dump() for x in payload.customer_group])

        self._replace_territory(business_id, row, [x.model_dump() for x in payload.territory])

        self._replace_sales_partner(business_id, row, [x.model_dump() for x in payload.sales_partner])

        self._replace_campaign(business_id, row, [x.model_dump() for x in payload.campaign])

        self._replace_supplier(business_id, row, [x.model_dump() for x in payload.supplier])

        self._replace_supplier_group(business_id, row, [x.model_dump() for x in payload.supplier_group])

        self._replace_price_discount_slabs(business_id, row, [x.model_dump() for x in payload.price_discount_slabs])

        self._replace_product_discount_slabs(business_id, row, [x.model_dump() for x in payload.product_discount_slabs])



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

        payload: PromotionalSchemeUpdate,

    ) -> PromotionalScheme:

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

                if field_name == "customer":

                    self._replace_customer(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "customer_group":

                    self._replace_customer_group(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "territory":

                    self._replace_territory(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "sales_partner":

                    self._replace_sales_partner(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "campaign":

                    self._replace_campaign(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "supplier":

                    self._replace_supplier(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "supplier_group":

                    self._replace_supplier_group(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "price_discount_slabs":

                    self._replace_price_discount_slabs(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "product_discount_slabs":

                    self._replace_product_discount_slabs(business_id, row, value or [])

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
