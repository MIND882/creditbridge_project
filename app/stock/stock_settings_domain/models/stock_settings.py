"""

Stock Settings -- converted from ``erpnext/stock/doctype/stock_settings``.



A Frappe Single (``issingle: 1``): one row per ``business_id``, enforced by a unique constraint on ``business_id`` alone.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, Enum as SAEnum, ForeignKey, Integer, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel



__all__ = ["StockSettings", "StockSettingsItemNamingBy", "StockSettingsValuationMethod", "StockSettingsActionIfQualityInspectionIsNotSubmitted", "StockSettingsActionIfQualityInspectionIsRejected", "StockSettingsPickSerialAndBatchBasedOn", "StockSettingsUpdatePriceListBasedOn"]





class StockSettingsItemNamingBy(str, enum.Enum):

    ITEM_CODE = "Item Code"

    NAMING_SERIES = "Naming Series"



class StockSettingsValuationMethod(str, enum.Enum):

    FIFO = "FIFO"

    MOVING_AVERAGE = "Moving Average"

    LIFO = "LIFO"

    STANDARD_COST = "Standard Cost"



class StockSettingsActionIfQualityInspectionIsNotSubmitted(str, enum.Enum):

    STOP = "Stop"

    WARN = "Warn"



class StockSettingsActionIfQualityInspectionIsRejected(str, enum.Enum):

    STOP = "Stop"

    WARN = "Warn"



class StockSettingsPickSerialAndBatchBasedOn(str, enum.Enum):

    FIFO = "FIFO"

    LIFO = "LIFO"

    EXPIRY = "Expiry"



class StockSettingsUpdatePriceListBasedOn(str, enum.Enum):

    RATE = "Rate"

    PRICE_LIST_RATE = "Price List Rate"





class StockSettings(TenantModel):

    __tablename__ = "stock_settingss"

    __table_args__ = (

        UniqueConstraint("business_id", name="uq_stock_settingss_business"),

    )



    item_naming_by: Mapped[Optional[str]] = mapped_column(SAEnum(StockSettingsItemNamingBy, native_enum=False, length=17, validate_strings=True), nullable=True)

    item_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("item_groups.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item_group = relationship("ItemGroup", foreign_keys=[item_group_id])

    stock_uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    stock_uom = relationship("Uom", foreign_keys=[stock_uom_id])

    valuation_method: Mapped[Optional[str]] = mapped_column(SAEnum(StockSettingsValuationMethod, native_enum=False, length=18, validate_strings=True), nullable=True)

    over_delivery_receipt_allowance: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    action_if_quality_inspection_is_not_submitted: Mapped[Optional[str]] = mapped_column(SAEnum(StockSettingsActionIfQualityInspectionIsNotSubmitted, native_enum=False, length=8, validate_strings=True), nullable=True)

    show_barcode_field: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    clean_description_html: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    auto_insert_price_list_rate_if_missing: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    allow_negative_stock: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    auto_indent: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    reorder_email_notify: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    stock_frozen_upto: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    stock_frozen_upto_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    stock_auth_role: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    use_naming_series: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    naming_series_prefix: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    role_allowed_to_create_edit_back_dated_transactions: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    disable_serial_no_and_batch_selector: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    role_allowed_to_over_deliver_receive: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    action_if_quality_inspection_is_rejected: Mapped[Optional[str]] = mapped_column(SAEnum(StockSettingsActionIfQualityInspectionIsRejected, native_enum=False, length=8, validate_strings=True), nullable=True)

    mr_qty_allowance: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    update_existing_price_list_rate: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    enable_stock_reservation: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    allow_partial_reservation: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    pick_serial_and_batch_based_on: Mapped[Optional[str]] = mapped_column(SAEnum(StockSettingsPickSerialAndBatchBasedOn, native_enum=False, length=10, validate_strings=True), nullable=True)

    auto_create_serial_and_batch_bundle_for_outward: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    auto_reserve_serial_and_batch: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    allow_to_edit_stock_uom_qty_for_sales: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    allow_to_edit_stock_uom_qty_for_purchase: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    allow_to_edit_stock_uom_qty_for_stock_entry: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    auto_reserve_stock_for_sales_order_on_purchase: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    use_serial_batch_fields: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    do_not_update_serial_batch_on_creation_of_auto_bundle: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    allow_internal_transfer_at_arms_length_price: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    do_not_use_batchwise_valuation: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    over_picking_allowance: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    allow_existing_serial_no: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    auto_reserve_stock: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    set_serial_and_batch_bundle_naming_based_on_naming_series: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    allow_uom_with_conversion_rate_defined_in_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    allow_to_make_quality_inspection_after_purchase_or_delivery: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    update_price_list_based_on: Mapped[Optional[str]] = mapped_column(SAEnum(StockSettingsUpdatePriceListBasedOn, native_enum=False, length=19, validate_strings=True), nullable=True)

    validate_material_transfer_warehouses: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    allow_negative_stock_for_batch: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    enable_serial_and_batch_no_for_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    naming_series_details: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    naming_series_preview: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    use_inline_serial_batch_editor: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<StockSettings id={self.id}>"
