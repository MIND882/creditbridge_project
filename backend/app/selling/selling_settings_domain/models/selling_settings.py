"""

Selling Settings -- converted from ``erpnext/selling/doctype/selling_settings``.



A Frappe Single (``issingle: 1``): one row per ``business_id``, enforced by a unique constraint on ``business_id`` alone.

"""



from __future__ import annotations



import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel



__all__ = ["SellingSettings", "SellingSettingsCustMasterName", "SellingSettingsMaintainSameRateAction", "SellingSettingsSoRequired", "SellingSettingsDnRequired", "SellingSettingsSalesUpdateFrequency"]





class SellingSettingsCustMasterName(str, enum.Enum):

    CUSTOMER_NAME = "Customer Name"

    NAMING_SERIES = "Naming Series"

    AUTO_NAME = "Auto Name"



class SellingSettingsMaintainSameRateAction(str, enum.Enum):

    STOP = "Stop"

    WARN = "Warn"



class SellingSettingsSoRequired(str, enum.Enum):

    NO = "No"

    YES = "Yes"



class SellingSettingsDnRequired(str, enum.Enum):

    NO = "No"

    YES = "Yes"



class SellingSettingsSalesUpdateFrequency(str, enum.Enum):

    MONTHLY = "Monthly"

    EACH_TRANSACTION = "Each Transaction"

    DAILY = "Daily"





class SellingSettings(TenantModel):

    __tablename__ = "selling_settings"

    __table_args__ = (

        UniqueConstraint("business_id", name="uq_selling_settingss_business"),

    )



    cust_master_name: Mapped[Optional[str]] = mapped_column(SAEnum(SellingSettingsCustMasterName, native_enum=False, length=17, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    naming_series_details: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    customer_group: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    territory: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    selling_price_list_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("price_lists.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    selling_price_list = relationship("app.stock.price_list_domain.models.price_list.PriceList", foreign_keys=[selling_price_list_id])

    fallback_to_default_price_list: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    editable_price_list_rate: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    maintain_same_sales_rate: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    maintain_same_rate_action: Mapped[Optional[str]] = mapped_column(SAEnum(SellingSettingsMaintainSameRateAction, values_callable=lambda x: [e.value for e in x], native_enum=False, length=8, validate_strings=True), nullable=True)

    role_to_override_stop_action: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    validate_selling_price: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    editable_bundle_item_rates: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    allow_negative_rates_for_items: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    so_required: Mapped[Optional[str]] = mapped_column(SAEnum(SellingSettingsSoRequired,values_callable=lambda x: [e.value for e in x],  native_enum=False, length=7, validate_strings=True), nullable=True)

    dn_required: Mapped[Optional[str]] = mapped_column(SAEnum(SellingSettingsDnRequired, values_callable=lambda x: [e.value for e in x], native_enum=False, length=7, validate_strings=True), nullable=True)

    sales_update_frequency: Mapped[Optional[str]] = mapped_column(SAEnum(SellingSettingsSalesUpdateFrequency, values_callable=lambda x: [e.value for e in x], native_enum=False, length=20, validate_strings=True), nullable=True)

    allow_multiple_items: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    allow_against_multiple_purchase_orders: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    hide_tax_id: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    allow_sales_order_creation_for_expired_quotation: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    dont_reserve_sales_order_qty_on_sales_return: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    enable_cutoff_date_on_bulk_delivery_note_creation: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    set_zero_rate_for_expired_batch: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    allow_zero_qty_in_quotation: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    allow_zero_qty_in_sales_order: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    blanket_order_allowance: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    enable_proforma_invoice: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    default_proforma_print_format: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    enable_tracking_sales_commissions: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    enable_discount_accounting: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    enable_utm: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    use_legacy_js_reactivity: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    allow_delivery_of_overproduced_qty: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    deliver_secondary_items: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SellingSettings id={self.id}>"
