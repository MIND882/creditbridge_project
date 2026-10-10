"""Business logic for Delivery Note -- port of

``erpnext/stock/doctype/delivery_note/delivery_note.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream has 8 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.delivery_note_domain.models.delivery_note import DeliveryNote

from app.stock.delivery_note_domain.repositories.delivery_note_repository import (

    DeliveryNoteRepository,

)

from app.stock.delivery_note_domain.schemas.delivery_note import (

    DeliveryNoteCreate,

    DeliveryNoteUpdate,

)

from app.stock.delivery_note_item_domain.models.delivery_note_item import DeliveryNoteItem

from app.stock.packed_item_domain.models.packed_item import PackedItem

from app.core.errors import NotFoundError

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.pagination import ResultPage



__all__ = ["DeliveryNoteService"]





class DeliveryNoteService:

    def __init__(self, repository: Optional[DeliveryNoteRepository] = None) -> None:

        self.repository = repository or DeliveryNoteRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> DeliveryNote:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Delivery Note", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: DeliveryNote

    ) -> None:

        """

        Upstream has 8 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> DeliveryNote:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[DeliveryNote]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[DeliveryNote].build(

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

                select(func.count()).select_from(DeliveryNote).where(

                    DeliveryNote.business_id == business_id

                )

            )

            or 0

        )

        return f"{prefix}{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: DeliveryNoteCreate

    ) -> DeliveryNote:

        row = DeliveryNote(

            business_id=business_id,

            name=self.next_name(db, business_id, payload.naming_series),

            naming_series=payload.naming_series,

            customer=payload.customer,

            customer_name=payload.customer_name,

            amended_from_id=payload.amended_from_id,

            company=payload.company,

            posting_date=payload.posting_date,

            posting_time=payload.posting_time,

            set_posting_time=payload.set_posting_time,

            is_return=payload.is_return,

            issue_credit_note=payload.issue_credit_note,

            return_against_id=payload.return_against_id,

            po_no=payload.po_no,

            po_date=payload.po_date,

            shipping_address_name=payload.shipping_address_name,

            shipping_address=payload.shipping_address,

            contact_person=payload.contact_person,

            contact_display=payload.contact_display,

            contact_mobile=payload.contact_mobile,

            contact_email=payload.contact_email,

            customer_address=payload.customer_address,

            tax_id=payload.tax_id,

            address_display=payload.address_display,

            company_address=payload.company_address,

            company_address_display=payload.company_address_display,

            currency=payload.currency,

            conversion_rate=payload.conversion_rate,

            selling_price_list_id=payload.selling_price_list_id,

            price_list_currency=payload.price_list_currency,

            plc_conversion_rate=payload.plc_conversion_rate,

            ignore_pricing_rule=payload.ignore_pricing_rule,

            set_warehouse_id=payload.set_warehouse_id,

            scan_barcode=payload.scan_barcode,

            total_qty=payload.total_qty,

            base_total=payload.base_total,

            base_net_total=payload.base_net_total,

            total=payload.total,

            net_total=payload.net_total,

            total_net_weight=payload.total_net_weight,

            tax_category_id=payload.tax_category_id,

            shipping_rule_id=payload.shipping_rule_id,

            taxes_and_charges_id=payload.taxes_and_charges_id,

            other_charges_calculation=payload.other_charges_calculation,

            base_total_taxes_and_charges=payload.base_total_taxes_and_charges,

            total_taxes_and_charges=payload.total_taxes_and_charges,

            apply_discount_on=payload.apply_discount_on,

            base_discount_amount=payload.base_discount_amount,

            additional_discount_percentage=payload.additional_discount_percentage,

            discount_amount=payload.discount_amount,

            base_grand_total=payload.base_grand_total,

            base_rounding_adjustment=payload.base_rounding_adjustment,

            base_rounded_total=payload.base_rounded_total,

            base_in_words=payload.base_in_words,

            grand_total=payload.grand_total,

            rounding_adjustment=payload.rounding_adjustment,

            rounded_total=payload.rounded_total,

            in_words=payload.in_words,

            tc_name=payload.tc_name,

            terms=payload.terms,

            transporter=payload.transporter,

            driver=payload.driver,

            lr_no=payload.lr_no,

            vehicle_no=payload.vehicle_no,

            transporter_name=payload.transporter_name,

            driver_name=payload.driver_name,

            lr_date=payload.lr_date,

            project=payload.project,

            per_billed=payload.per_billed,

            customer_group=payload.customer_group,

            territory=payload.territory,

            letter_head=payload.letter_head,

            select_print_heading=payload.select_print_heading,

            language=payload.language,

            print_without_amount=payload.print_without_amount,

            group_same_items=payload.group_same_items,

            status=payload.status,

            per_installed=payload.per_installed,

            installation_status=payload.installation_status,

            excise_page=payload.excise_page,

            instructions=payload.instructions,

            auto_repeat=payload.auto_repeat,

            sales_partner=payload.sales_partner,

            commission_rate=payload.commission_rate,

            total_commission=payload.total_commission,

            is_internal_customer=payload.is_internal_customer,

            inter_company_reference_id=payload.inter_company_reference_id,

            per_returned=payload.per_returned,

            set_target_warehouse_id=payload.set_target_warehouse_id,

            represents_company=payload.represents_company,

            disable_rounded_total=payload.disable_rounded_total,

            dispatch_address_name=payload.dispatch_address_name,

            dispatch_address=payload.dispatch_address,

            amount_eligible_for_commission=payload.amount_eligible_for_commission,

            cost_center_id=payload.cost_center_id,

            incoterm=payload.incoterm,

            named_place=payload.named_place,

            delivery_trip_id=payload.delivery_trip_id,

            utm_medium=payload.utm_medium,

            utm_content=payload.utm_content,

            utm_source=payload.utm_source,

            utm_campaign=payload.utm_campaign,

            company_contact_person=payload.company_contact_person,

            last_scanned_warehouse=payload.last_scanned_warehouse,

            title=payload.title,

        )

        self._replace_items(business_id, row, [x.model_dump() for x in payload.items])

        self._replace_packed_items(business_id, row, [x.model_dump() for x in payload.packed_items])



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

        payload: DeliveryNoteUpdate,

    ) -> DeliveryNote:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "items":

                    self._replace_items(business_id, row, value or [])

                    continue

                if field_name == "packed_items":

                    self._replace_packed_items(business_id, row, value or [])

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

    ) -> DeliveryNote:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Delivery Note")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> DeliveryNote:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Delivery Note")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row



    def _replace_items(

        self, business_id: uuid.UUID, row: DeliveryNote, items: list[dict]

    ) -> None:

        row.items.clear()

        for idx, entry in enumerate(items, start=1):

            row.items.append(

                DeliveryNoteItem(

                    business_id=business_id,

                    idx=idx,

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_packed_items(

        self, business_id: uuid.UUID, row: DeliveryNote, packed_items: list[dict]

    ) -> None:

        row.packed_items.clear()

        for idx, entry in enumerate(packed_items, start=1):

            row.packed_items.append(

                PackedItem(

                    business_id=business_id,

                    idx=idx,

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )
