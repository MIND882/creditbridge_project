"""

Item -- converted from ``erpnext/stock/doctype/item``.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, Enum as SAEnum, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.stock.item_barcode_domain.models.item_barcode import ItemBarcode

from app.stock.item_reorder_domain.models.item_reorder import ItemReorder

from app.stock.uom_conversion_detail_domain.models.uom_conversion_detail import UomConversionDetail

from app.stock.item_variant_attribute_domain.models.item_variant_attribute import ItemVariantAttribute

from app.stock.item_default_domain.models.item_default import ItemDefault

from app.stock.item_supplier_domain.models.item_supplier import ItemSupplier

from app.stock.item_customer_detail_domain.models.item_customer_detail import ItemCustomerDetail

from app.stock.item_tax_domain.models.item_tax import ItemTax



from app.core.base_model import TenantModel



__all__ = ["Item", "ItemNamingSeries", "ItemDefaultMaterialRequestType", "ItemValuationMethod", "ItemVariantBasedOn"]





class ItemNamingSeries(str, enum.Enum):

    STO_ITEM_YYYY = "STO-ITEM-.YYYY.-"



class ItemDefaultMaterialRequestType(str, enum.Enum):

    PURCHASE = "Purchase"

    MATERIAL_TRANSFER = "Material Transfer"

    MATERIAL_ISSUE = "Material Issue"

    MANUFACTURE = "Manufacture"

    CUSTOMER_PROVIDED = "Customer Provided"



class ItemValuationMethod(str, enum.Enum):

    FIFO = "FIFO"

    MOVING_AVERAGE = "Moving Average"

    LIFO = "LIFO"

    STANDARD_COST = "Standard Cost"



class ItemVariantBasedOn(str, enum.Enum):

    ITEM_ATTRIBUTE = "Item Attribute"

    MANUFACTURER = "Manufacturer"





class Item(TenantModel):

    __tablename__ = "items"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_items_business_name"),

    )



    #: ``autoname`` = 'field:item_code' -- derived in the service at create time.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    naming_series: Mapped[Optional[str]] = mapped_column(SAEnum(ItemNamingSeries, native_enum=False, length=20, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    item_code: Mapped[str] = mapped_column(String(140), nullable=False)

    variant_of_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    variant_of = relationship("Item", foreign_keys=[variant_of_id])

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    item_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("item_groups.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    item_group = relationship("ItemGroup", foreign_keys=[item_group_id])

    stock_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    stock_uom = relationship("Uom", foreign_keys=[stock_uom_id])

    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    allow_alternative_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    is_stock_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    include_item_in_manufacturing: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    opening_stock: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    valuation_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    standard_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    is_fixed_asset: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    asset_category: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    asset_naming_series: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    image: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    brand_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("brands.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    brand = relationship("Brand", foreign_keys=[brand_id])

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    shelf_life_in_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    end_of_life: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    default_material_request_type: Mapped[Optional[str]] = mapped_column(SAEnum(ItemDefaultMaterialRequestType, native_enum=False, length=21, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    valuation_method: Mapped[Optional[str]] = mapped_column(SAEnum(ItemValuationMethod, native_enum=False, length=18, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    warranty_period: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    weight_per_unit: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    weight_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    weight_uom = relationship("Uom", foreign_keys=[weight_uom_id])

    has_batch_no: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    create_new_batch: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    batch_number_series: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    has_expiry_date: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    retain_sample: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    sample_quantity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    has_serial_no: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    serial_no_series: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    has_variants: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    variant_based_on: Mapped[Optional[str]] = mapped_column(SAEnum(ItemVariantBasedOn, native_enum=False, length=18, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    is_purchase_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    purchase_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    purchase_uom = relationship("Uom", foreign_keys=[purchase_uom_id])

    min_order_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0.0)

    safety_stock: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    lead_time_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    last_purchase_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    is_customer_provided_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    delivered_by_supplier: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    country_of_origin: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    customs_tariff_number_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("customs_tariff_numbers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    customs_tariff_number = relationship("CustomsTariffNumber", foreign_keys=[customs_tariff_number_id])

    sales_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    sales_uom = relationship("Uom", foreign_keys=[sales_uom_id])

    is_sales_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    max_discount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    enable_deferred_revenue: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    no_of_months: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    enable_deferred_expense: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    no_of_months_exp: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    inspection_required_before_purchase: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    inspection_required_before_delivery: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    quality_inspection_template_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("quality_inspection_templates.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    quality_inspection_template = relationship("QualityInspectionTemplate", foreign_keys=[quality_inspection_template_id])

    default_bom: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_sub_contracted_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    customer_code: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    total_projected_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    over_delivery_receipt_allowance: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    over_billing_allowance: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    auto_create_assets: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    default_item_manufacturer_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("manufacturers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    default_item_manufacturer = relationship("Manufacturer", foreign_keys=[default_item_manufacturer_id])

    default_manufacturer_part_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    grant_commission: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    is_grouped_asset: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    allow_negative_stock: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    production_capacity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    purchase_tax_withholding_category_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("tax_withholding_categories.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    purchase_tax_withholding_category = relationship("TaxWithholdingCategory", foreign_keys=[purchase_tax_withholding_category_id])

    sales_tax_withholding_category_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("tax_withholding_categories.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    sales_tax_withholding_category = relationship("TaxWithholdingCategory", foreign_keys=[sales_tax_withholding_category_id])

    restrict_to_companies: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    barcodes: Mapped[list["ItemBarcode"]] = relationship(  # noqa: F821

        "ItemBarcode",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[ItemBarcode.parent_id]",

    )



    reorder_levels: Mapped[list["ItemReorder"]] = relationship(  # noqa: F821

        "ItemReorder",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[ItemReorder.parent_id]",

    )



    uoms: Mapped[list["UomConversionDetail"]] = relationship(  # noqa: F821

        "UomConversionDetail",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[UomConversionDetail.parent_id]",

    )



    attributes: Mapped[list["ItemVariantAttribute"]] = relationship(  # noqa: F821

        "ItemVariantAttribute",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[ItemVariantAttribute.parent_id]",

    )



    item_defaults: Mapped[list["ItemDefault"]] = relationship(  # noqa: F821

        "ItemDefault",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[ItemDefault.parent_id]",

    )



    supplier_items: Mapped[list["ItemSupplier"]] = relationship(  # noqa: F821

        "ItemSupplier",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[ItemSupplier.parent_id]",

    )



    customer_items: Mapped[list["ItemCustomerDetail"]] = relationship(  # noqa: F821

        "ItemCustomerDetail",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[ItemCustomerDetail.parent_id]",

    )



    taxes: Mapped[list["ItemTax"]] = relationship(  # noqa: F821

        "ItemTax",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[ItemTax.parent_id]",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<Item id={self.id}>"
