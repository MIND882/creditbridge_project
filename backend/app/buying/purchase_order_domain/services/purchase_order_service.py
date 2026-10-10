"""Business logic for Purchase Order -- port of

``erpnext/buying/doctype/purchase_order/purchase_order.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.buying.purchase_order_domain.models.purchase_order import PurchaseOrder

from app.buying.purchase_order_domain.repositories.purchase_order_repository import (

    PurchaseOrderRepository,

)

from app.buying.purchase_order_domain.schemas.purchase_order import (

    PurchaseOrderCreate,

    PurchaseOrderUpdate,

)

from app.buying.purchase_order_item_domain.models.purchase_order_item import PurchaseOrderItem

from app.core.errors import NotFoundError

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.pagination import ResultPage



__all__ = ["PurchaseOrderService"]





class PurchaseOrderService:

    def __init__(self, repository: Optional[PurchaseOrderRepository] = None) -> None:

        self.repository = repository or PurchaseOrderRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PurchaseOrder:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Purchase Order", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: PurchaseOrder

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PurchaseOrder:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PurchaseOrder]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PurchaseOrder].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID, series: Optional[str] = None) -> str:

        """A per-tenant sequential name; upstream mints one from ``naming_series``."""

        # ``naming_series`` is optional on input (Frappe fills it from a

        # default), so fall back to the doctype prefix when it is absent.

        series = series or ""

        prefix = series.split(".")[0].split("#")[0]

        if prefix and not prefix.endswith("-"):

            prefix += "-"

        count = int(

            db.scalar(

                select(func.count()).select_from(PurchaseOrder).where(

                    PurchaseOrder.business_id == business_id

                )

            )

            or 0

        )

        return f"{prefix}{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: PurchaseOrderCreate

    ) -> PurchaseOrder:

        row = PurchaseOrder(

            business_id=business_id,

            name=self.next_name(db, business_id, payload.naming_series),

            title=payload.title,

            naming_series=payload.naming_series,

            supplier_id=payload.supplier_id,

            supplier_name=payload.supplier_name,

            company=payload.company,

            transaction_date=payload.transaction_date,

            schedule_date=payload.schedule_date,

            order_confirmation_no=payload.order_confirmation_no,

            order_confirmation_date=payload.order_confirmation_date,

            amended_from_id=payload.amended_from_id,

            customer=payload.customer,

            customer_name=payload.customer_name,

            customer_contact_person=payload.customer_contact_person,

            customer_contact_display=payload.customer_contact_display,

            customer_contact_mobile=payload.customer_contact_mobile,

            customer_contact_email=payload.customer_contact_email,

            supplier_address=payload.supplier_address,

            contact_person=payload.contact_person,

            address_display=payload.address_display,

            contact_display=payload.contact_display,

            contact_mobile=payload.contact_mobile,

            contact_email=payload.contact_email,

            shipping_address=payload.shipping_address,

            shipping_address_display=payload.shipping_address_display,

            currency=payload.currency,

            conversion_rate=payload.conversion_rate,

            buying_price_list_id=payload.buying_price_list_id,

            price_list_currency=payload.price_list_currency,

            plc_conversion_rate=payload.plc_conversion_rate,

            ignore_pricing_rule=payload.ignore_pricing_rule,

            set_warehouse_id=payload.set_warehouse_id,

            is_subcontracted=payload.is_subcontracted,

            supplier_warehouse_id=payload.supplier_warehouse_id,

            scan_barcode=payload.scan_barcode,

            total_qty=payload.total_qty,

            base_total=payload.base_total,

            base_net_total=payload.base_net_total,

            total=payload.total,

            net_total=payload.net_total,

            total_net_weight=payload.total_net_weight,

            taxes_and_charges_id=payload.taxes_and_charges_id,

            shipping_rule_id=payload.shipping_rule_id,

            other_charges_calculation=payload.other_charges_calculation,

            base_taxes_and_charges_added=payload.base_taxes_and_charges_added,

            base_taxes_and_charges_deducted=payload.base_taxes_and_charges_deducted,

            base_total_taxes_and_charges=payload.base_total_taxes_and_charges,

            taxes_and_charges_added=payload.taxes_and_charges_added,

            taxes_and_charges_deducted=payload.taxes_and_charges_deducted,

            total_taxes_and_charges=payload.total_taxes_and_charges,

            apply_discount_on=payload.apply_discount_on,

            base_discount_amount=payload.base_discount_amount,

            additional_discount_percentage=payload.additional_discount_percentage,

            discount_amount=payload.discount_amount,

            base_grand_total=payload.base_grand_total,

            base_rounding_adjustment=payload.base_rounding_adjustment,

            base_in_words=payload.base_in_words,

            base_rounded_total=payload.base_rounded_total,

            grand_total=payload.grand_total,

            rounding_adjustment=payload.rounding_adjustment,

            rounded_total=payload.rounded_total,

            disable_rounded_total=payload.disable_rounded_total,

            in_words=payload.in_words,

            advance_paid=payload.advance_paid,

            payment_terms_template_id=payload.payment_terms_template_id,

            tc_name=payload.tc_name,

            terms=payload.terms,

            status=payload.status,

            ref_sq_id=payload.ref_sq_id,

            party_account_currency=payload.party_account_currency,

            inter_company_order_reference=payload.inter_company_order_reference,

            per_received=payload.per_received,

            per_billed=payload.per_billed,

            letter_head=payload.letter_head,

            select_print_heading=payload.select_print_heading,

            group_same_items=payload.group_same_items,

            language=payload.language,

            from_date=payload.from_date,

            to_date=payload.to_date,

            auto_repeat=payload.auto_repeat,

            tax_category_id=payload.tax_category_id,

            set_reserve_warehouse_id=payload.set_reserve_warehouse_id,

            billing_address=payload.billing_address,

            billing_address_display=payload.billing_address_display,

            is_internal_supplier=payload.is_internal_supplier,

            represents_company=payload.represents_company,

            cost_center_id=payload.cost_center_id,

            project=payload.project,

            set_from_warehouse_id=payload.set_from_warehouse_id,

            incoterm=payload.incoterm,

            named_place=payload.named_place,

            advance_payment_status=payload.advance_payment_status,

            has_unit_price_items=payload.has_unit_price_items,

            dispatch_address=payload.dispatch_address,

            dispatch_address_display=payload.dispatch_address_display,

            supplier_group=payload.supplier_group,

            last_scanned_warehouse=payload.last_scanned_warehouse,

            mps=payload.mps,

            transaction_time=payload.transaction_time,

        )

        self._replace_items(business_id, row, [x.model_dump() for x in payload.items])



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

        payload: PurchaseOrderUpdate,

    ) -> PurchaseOrder:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "items":

                    self._replace_items(business_id, row, value or [])

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



    def submit(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PurchaseOrder:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Purchase Order")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PurchaseOrder:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Purchase Order")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row



    def _replace_items(

        self, business_id: uuid.UUID, row: PurchaseOrder, items: list[dict]

    ) -> None:

        row.items.clear()

        for idx, entry in enumerate(items, start=1):

            row.items.append(

                PurchaseOrderItem(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Purchase Order",

                    parentfield="items",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )
