"""

Buying Settings -- converted from ``erpnext/buying/doctype/buying_settings``.



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



__all__ = ["BuyingSettings", "BuyingSettingsSuppMasterName", "BuyingSettingsPoRequired", "BuyingSettingsPrRequired", "BuyingSettingsBackflushRawMaterialsOfSubcontractBasedOn", "BuyingSettingsMaintainSameRateAction", "BuyingSettingsProjectUpdateFrequency"]





class BuyingSettingsSuppMasterName(str, enum.Enum):

    SUPPLIER_NAME = "Supplier Name"

    NAMING_SERIES = "Naming Series"

    AUTO_NAME = "Auto Name"



class BuyingSettingsPoRequired(str, enum.Enum):

    NO = "No"

    YES = "Yes"



class BuyingSettingsPrRequired(str, enum.Enum):

    NO = "No"

    YES = "Yes"



class BuyingSettingsBackflushRawMaterialsOfSubcontractBasedOn(str, enum.Enum):

    BOM = "BOM"

    MATERIAL_TRANSFERRED_FOR_SUBCONTRACT = "Material Transferred for Subcontract"



class BuyingSettingsMaintainSameRateAction(str, enum.Enum):

    STOP = "Stop"

    WARN = "Warn"



class BuyingSettingsProjectUpdateFrequency(str, enum.Enum):

    EACH_TRANSACTION = "Each Transaction"

    MANUAL = "Manual"





class BuyingSettings(TenantModel):

    __tablename__ = "buying_settings"

    __table_args__ = (

        UniqueConstraint("business_id", name="uq_buying_settingss_business"),

    )



    supp_master_name: Mapped[Optional[str]] = mapped_column(SAEnum(BuyingSettingsSuppMasterName, native_enum=False, length=17, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    supplier_group: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    buying_price_list_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("price_lists.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    buying_price_list = relationship("app.stock.price_list_domain.models.price_list.PriceList", foreign_keys=[buying_price_list_id])

    po_required: Mapped[Optional[str]] = mapped_column(SAEnum(BuyingSettingsPoRequired, native_enum=False, length=7, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    pr_required: Mapped[Optional[str]] = mapped_column(SAEnum(BuyingSettingsPrRequired, native_enum=False, length=7, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    maintain_same_rate: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    allow_multiple_items: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    backflush_raw_materials_of_subcontract_based_on: Mapped[Optional[str]] = mapped_column(SAEnum(BuyingSettingsBackflushRawMaterialsOfSubcontractBasedOn, native_enum=False, length=40, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    over_transfer_allowance: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    maintain_same_rate_action: Mapped[Optional[str]] = mapped_column(SAEnum(BuyingSettingsMaintainSameRateAction, native_enum=False, length=8, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    role_to_override_stop_action: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    bill_for_rejected_quantity_in_purchase_invoice: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    disable_last_purchase_rate: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    show_pay_button: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    set_landed_cost_based_on_purchase_invoice_rate: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    use_transaction_date_exchange_rate: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    blanket_order_allowance: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0)

    auto_create_subcontracting_order: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    auto_create_purchase_receipt: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    project_update_frequency: Mapped[Optional[str]] = mapped_column(SAEnum(BuyingSettingsProjectUpdateFrequency, native_enum=False, length=20, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    allow_zero_qty_in_purchase_order: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    allow_zero_qty_in_request_for_quotation: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    allow_zero_qty_in_supplier_quotation: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    set_valuation_rate_for_rejected_materials: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    fixed_email: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    validate_consumed_qty: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    allow_negative_rates_for_items: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    naming_series_details: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    over_order_allowance: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<BuyingSettings id={self.id}>"
