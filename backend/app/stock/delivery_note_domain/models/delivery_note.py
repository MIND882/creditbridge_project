"""

Delivery Note -- converted from ``erpnext/stock/doctype/delivery_note``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, Enum as SAEnum, ForeignKey, Numeric, String, Text, Time, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.stock.delivery_note_item_domain.models.delivery_note_item import DeliveryNoteItem

from app.stock.packed_item_domain.models.packed_item import PackedItem



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["DeliveryNote", "DeliveryNoteNamingSeries", "DeliveryNoteApplyDiscountOn", "DeliveryNoteStatus"]





class DeliveryNoteNamingSeries(str, enum.Enum):

    MAT_DN_YYYY = "MAT-DN-.YYYY.-"

    MAT_DN_RET_YYYY = "MAT-DN-RET-.YYYY.-"



class DeliveryNoteApplyDiscountOn(str, enum.Enum):

    GRAND_TOTAL = "Grand Total"

    NET_TOTAL = "Net Total"



class DeliveryNoteStatus(str, enum.Enum):

    DRAFT = "Draft"

    TO_BILL = "To Bill"

    PARTIALLY_BILLED = "Partially Billed"

    COMPLETED = "Completed"

    RETURN = "Return"

    RETURN_ISSUED = "Return Issued"

    CANCELLED = "Cancelled"

    CLOSED = "Closed"





class DeliveryNote(SubmittableModel, TenantModel):

    __tablename__ = "delivery_notes"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_delivery_notes_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    naming_series: Mapped[str] = mapped_column(SAEnum(DeliveryNoteNamingSeries, native_enum=False, length=22, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=False)

    customer: Mapped[str] = mapped_column(String(140), nullable=False)

    customer_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("delivery_notes.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("DeliveryNote", foreign_keys=[amended_from_id])

    company: Mapped[str] = mapped_column(String(140), nullable=False)

    posting_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    posting_time: Mapped[dt.time] = mapped_column(Time, nullable=False)

    set_posting_time: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    is_return: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    issue_credit_note: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    return_against_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("delivery_notes.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    return_against = relationship("DeliveryNote", foreign_keys=[return_against_id])

    po_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    po_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    shipping_address_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    shipping_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    contact_person: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    contact_display: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    contact_mobile: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    contact_email: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    customer_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    tax_id: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    address_display: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    company_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    company_address_display: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    currency: Mapped[str] = mapped_column(String(140), nullable=False)

    conversion_rate: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    selling_price_list_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("price_lists.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    selling_price_list = relationship("PriceList", foreign_keys=[selling_price_list_id])

    price_list_currency: Mapped[str] = mapped_column(String(140), nullable=False)

    plc_conversion_rate: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    ignore_pricing_rule: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    set_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    set_warehouse = relationship("Warehouse", foreign_keys=[set_warehouse_id])

    scan_barcode: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    total_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_net_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    net_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_net_weight: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    tax_category_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("tax_categories.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    tax_category = relationship("TaxCategory", foreign_keys=[tax_category_id])

    shipping_rule_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("shipping_rules.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    shipping_rule = relationship("ShippingRule", foreign_keys=[shipping_rule_id])

    taxes_and_charges_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("sales_taxes_and_charges_templates.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    taxes_and_charges = relationship("SalesTaxesAndChargesTemplate", foreign_keys=[taxes_and_charges_id])

    other_charges_calculation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    base_total_taxes_and_charges: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_taxes_and_charges: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    apply_discount_on: Mapped[Optional[str]] = mapped_column(SAEnum(DeliveryNoteApplyDiscountOn, native_enum=False, length=15, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    base_discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    additional_discount_percentage: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_grand_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_rounding_adjustment: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_rounded_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_in_words: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    grand_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rounding_adjustment: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rounded_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    in_words: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    tc_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    terms: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    transporter: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    driver: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    lr_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    vehicle_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    transporter_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    driver_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    lr_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    per_billed: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    customer_group: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    territory: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    letter_head: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    select_print_heading: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    language: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    print_without_amount: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    group_same_items: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    status: Mapped[str] = mapped_column(SAEnum(DeliveryNoteStatus, native_enum=False, length=20, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=False)

    per_installed: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    installation_status: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    excise_page: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    instructions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    auto_repeat: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    sales_partner: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    commission_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_commission: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    is_internal_customer: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    inter_company_reference_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("purchase_receipts.id", ondelete="RESTRICT", use_alter=True, name="fk_delivery_notes_inter_company_reference_id"),

        nullable=True, index=True,

    )

    inter_company_reference = relationship("PurchaseReceipt", foreign_keys=[inter_company_reference_id])

    per_returned: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    set_target_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    set_target_warehouse = relationship("Warehouse", foreign_keys=[set_target_warehouse_id])

    represents_company: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    disable_rounded_total: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    dispatch_address_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    dispatch_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    amount_eligible_for_commission: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])

    incoterm: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    named_place: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    delivery_trip_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("delivery_trips.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    delivery_trip = relationship("DeliveryTrip", foreign_keys=[delivery_trip_id])

    utm_medium: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    utm_content: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    utm_source: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    utm_campaign: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    company_contact_person: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    last_scanned_warehouse: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    title: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    items: Mapped[list["DeliveryNoteItem"]] = relationship(  # noqa: F821

        "DeliveryNoteItem",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[DeliveryNoteItem.parent_id]",

    )



    packed_items: Mapped[list["PackedItem"]] = relationship(  # noqa: F821

        "PackedItem",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[PackedItem.parent_id]",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<DeliveryNote id={self.id}>"
