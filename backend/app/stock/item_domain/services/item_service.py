"""Business logic for Item -- port of

``erpnext/stock/doctype/item/item.py``.



Upstream has 61 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.item_domain.models.item import Item

from app.stock.item_domain.repositories.item_repository import (

    ItemRepository,

)

from app.stock.item_domain.schemas.item import (

    ItemCreate,

    ItemUpdate,

)

from app.stock.item_barcode_domain.models.item_barcode import ItemBarcode

from app.stock.item_reorder_domain.models.item_reorder import ItemReorder

from app.stock.uom_conversion_detail_domain.models.uom_conversion_detail import UomConversionDetail

from app.stock.item_variant_attribute_domain.models.item_variant_attribute import ItemVariantAttribute

from app.stock.item_default_domain.models.item_default import ItemDefault

from app.stock.item_supplier_domain.models.item_supplier import ItemSupplier

from app.stock.item_customer_detail_domain.models.item_customer_detail import ItemCustomerDetail

from app.stock.item_tax_domain.models.item_tax import ItemTax

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ItemService"]





class ItemService:

    def __init__(self, repository: Optional[ItemRepository] = None) -> None:

        self.repository = repository or ItemRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Item:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Item", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: Item

    ) -> None:

        """

        Upstream has 61 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Item:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[Item]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[Item].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    # ``autoname = 'field:item_code'``: the name is the value of

    # that field, derived at create time (Frappe derives it on every save;

    # the creation-time value is what migrated documents carry).



    def create(

        self, db: Session, business_id: uuid.UUID, payload: ItemCreate

    ) -> Item:

        row = Item(

            business_id=business_id,

            name=payload.item_code,

            naming_series=payload.naming_series,

            item_code=payload.item_code,

            variant_of_id=payload.variant_of_id,

            item_name=payload.item_name,

            item_group_id=payload.item_group_id,

            stock_uom_id=payload.stock_uom_id,

            disabled=payload.disabled,

            allow_alternative_item=payload.allow_alternative_item,

            is_stock_item=payload.is_stock_item,

            include_item_in_manufacturing=payload.include_item_in_manufacturing,

            opening_stock=payload.opening_stock,

            valuation_rate=payload.valuation_rate,

            standard_rate=payload.standard_rate,

            is_fixed_asset=payload.is_fixed_asset,

            asset_category=payload.asset_category,

            asset_naming_series=payload.asset_naming_series,

            image=payload.image,

            brand_id=payload.brand_id,

            description=payload.description,

            shelf_life_in_days=payload.shelf_life_in_days,

            end_of_life=payload.end_of_life,

            default_material_request_type=payload.default_material_request_type,

            valuation_method=payload.valuation_method,

            warranty_period=payload.warranty_period,

            weight_per_unit=payload.weight_per_unit,

            weight_uom_id=payload.weight_uom_id,

            has_batch_no=payload.has_batch_no,

            create_new_batch=payload.create_new_batch,

            batch_number_series=payload.batch_number_series,

            has_expiry_date=payload.has_expiry_date,

            retain_sample=payload.retain_sample,

            sample_quantity=payload.sample_quantity,

            has_serial_no=payload.has_serial_no,

            serial_no_series=payload.serial_no_series,

            has_variants=payload.has_variants,

            variant_based_on=payload.variant_based_on,

            is_purchase_item=payload.is_purchase_item,

            purchase_uom_id=payload.purchase_uom_id,

            min_order_qty=payload.min_order_qty,

            safety_stock=payload.safety_stock,

            lead_time_days=payload.lead_time_days,

            last_purchase_rate=payload.last_purchase_rate,

            is_customer_provided_item=payload.is_customer_provided_item,

            delivered_by_supplier=payload.delivered_by_supplier,

            country_of_origin=payload.country_of_origin,

            customs_tariff_number_id=payload.customs_tariff_number_id,

            sales_uom_id=payload.sales_uom_id,

            is_sales_item=payload.is_sales_item,

            max_discount=payload.max_discount,

            enable_deferred_revenue=payload.enable_deferred_revenue,

            no_of_months=payload.no_of_months,

            enable_deferred_expense=payload.enable_deferred_expense,

            no_of_months_exp=payload.no_of_months_exp,

            inspection_required_before_purchase=payload.inspection_required_before_purchase,

            inspection_required_before_delivery=payload.inspection_required_before_delivery,

            quality_inspection_template_id=payload.quality_inspection_template_id,

            default_bom=payload.default_bom,

            is_sub_contracted_item=payload.is_sub_contracted_item,

            customer_code=payload.customer_code,

            total_projected_qty=payload.total_projected_qty,

            over_delivery_receipt_allowance=payload.over_delivery_receipt_allowance,

            over_billing_allowance=payload.over_billing_allowance,

            auto_create_assets=payload.auto_create_assets,

            default_item_manufacturer_id=payload.default_item_manufacturer_id,

            default_manufacturer_part_no=payload.default_manufacturer_part_no,

            grant_commission=payload.grant_commission,

            is_grouped_asset=payload.is_grouped_asset,

            allow_negative_stock=payload.allow_negative_stock,

            production_capacity=payload.production_capacity,

            purchase_tax_withholding_category_id=payload.purchase_tax_withholding_category_id,

            sales_tax_withholding_category_id=payload.sales_tax_withholding_category_id,

            restrict_to_companies=payload.restrict_to_companies,

        )

        self._replace_barcodes(business_id, row, [x.model_dump() for x in payload.barcodes])

        self._replace_reorder_levels(business_id, row, [x.model_dump() for x in payload.reorder_levels])

        self._replace_uoms(business_id, row, [x.model_dump() for x in payload.uoms])

        self._replace_attributes(business_id, row, [x.model_dump() for x in payload.attributes])

        self._replace_item_defaults(business_id, row, [x.model_dump() for x in payload.item_defaults])

        self._replace_supplier_items(business_id, row, [x.model_dump() for x in payload.supplier_items])

        self._replace_customer_items(business_id, row, [x.model_dump() for x in payload.customer_items])

        self._replace_taxes(business_id, row, [x.model_dump() for x in payload.taxes])



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

        payload: ItemUpdate,

    ) -> Item:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "barcodes":

                    self._replace_barcodes(business_id, row, value or [])

                    continue

                if field_name == "reorder_levels":

                    self._replace_reorder_levels(business_id, row, value or [])

                    continue

                if field_name == "uoms":

                    self._replace_uoms(business_id, row, value or [])

                    continue

                if field_name == "attributes":

                    self._replace_attributes(business_id, row, value or [])

                    continue

                if field_name == "item_defaults":

                    self._replace_item_defaults(business_id, row, value or [])

                    continue

                if field_name == "supplier_items":

                    self._replace_supplier_items(business_id, row, value or [])

                    continue

                if field_name == "customer_items":

                    self._replace_customer_items(business_id, row, value or [])

                    continue

                if field_name == "taxes":

                    self._replace_taxes(business_id, row, value or [])

                    continue

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



    def _replace_barcodes(

        self, business_id: uuid.UUID, row: Item, barcodes: list[dict]

    ) -> None:

        row.barcodes.clear()

        for idx, entry in enumerate(barcodes, start=1):

            row.barcodes.append(

                ItemBarcode(

                    business_id=business_id,

                    idx=idx,

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_reorder_levels(

        self, business_id: uuid.UUID, row: Item, reorder_levels: list[dict]

    ) -> None:

        row.reorder_levels.clear()

        for idx, entry in enumerate(reorder_levels, start=1):

            row.reorder_levels.append(

                ItemReorder(

                    business_id=business_id,

                    idx=idx,

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_uoms(

        self, business_id: uuid.UUID, row: Item, uoms: list[dict]

    ) -> None:

        row.uoms.clear()

        for idx, entry in enumerate(uoms, start=1):

            row.uoms.append(

                UomConversionDetail(

                    business_id=business_id,

                    idx=idx,

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_attributes(

        self, business_id: uuid.UUID, row: Item, attributes: list[dict]

    ) -> None:

        row.attributes.clear()

        for idx, entry in enumerate(attributes, start=1):

            row.attributes.append(

                ItemVariantAttribute(

                    business_id=business_id,

                    idx=idx,

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_item_defaults(

        self, business_id: uuid.UUID, row: Item, item_defaults: list[dict]

    ) -> None:

        row.item_defaults.clear()

        for idx, entry in enumerate(item_defaults, start=1):

            row.item_defaults.append(

                ItemDefault(

                    business_id=business_id,

                    idx=idx,

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_supplier_items(

        self, business_id: uuid.UUID, row: Item, supplier_items: list[dict]

    ) -> None:

        row.supplier_items.clear()

        for idx, entry in enumerate(supplier_items, start=1):

            row.supplier_items.append(

                ItemSupplier(

                    business_id=business_id,

                    idx=idx,

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_customer_items(

        self, business_id: uuid.UUID, row: Item, customer_items: list[dict]

    ) -> None:

        row.customer_items.clear()

        for idx, entry in enumerate(customer_items, start=1):

            row.customer_items.append(

                ItemCustomerDetail(

                    business_id=business_id,

                    idx=idx,

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_taxes(

        self, business_id: uuid.UUID, row: Item, taxes: list[dict]

    ) -> None:

        row.taxes.clear()

        for idx, entry in enumerate(taxes, start=1):

            row.taxes.append(

                ItemTax(

                    business_id=business_id,

                    idx=idx,

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )
