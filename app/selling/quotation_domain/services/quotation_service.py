"""Business logic for Quotation -- port of

``erpnext/selling/doctype/quotation/quotation.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.selling.quotation_domain.models.quotation import Quotation

from app.selling.quotation_domain.repositories.quotation_repository import (

    QuotationRepository,

)

from app.selling.quotation_domain.schemas.quotation import (

    QuotationCreate,

    QuotationUpdate,

)

from app.selling.quotation_item_domain.models.quotation_item import QuotationItem

from app.core.errors import NotFoundError

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.pagination import ResultPage



__all__ = ["QuotationService"]





class QuotationService:

    def __init__(self, repository: Optional[QuotationRepository] = None) -> None:

        self.repository = repository or QuotationRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Quotation:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Quotation", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: Quotation

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Quotation:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[Quotation]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[Quotation].build(

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

                select(func.count()).select_from(Quotation).where(

                    Quotation.business_id == business_id

                )

            )

            or 0

        )

        return f"{prefix}{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: QuotationCreate

    ) -> Quotation:

        row = Quotation(

            business_id=business_id,

            name=self.next_name(db, business_id, payload.naming_series),

            naming_series=payload.naming_series,

            quotation_to=payload.quotation_to,

            party_name=payload.party_name,

            customer_name=payload.customer_name,

            transaction_date=payload.transaction_date,

            valid_till=payload.valid_till,

            order_type=payload.order_type,

            company=payload.company,

            has_unit_price_items=payload.has_unit_price_items,

            amended_from_id=payload.amended_from_id,

            currency=payload.currency,

            conversion_rate=payload.conversion_rate,

            selling_price_list_id=payload.selling_price_list_id,

            price_list_currency=payload.price_list_currency,

            plc_conversion_rate=payload.plc_conversion_rate,

            ignore_pricing_rule=payload.ignore_pricing_rule,

            scan_barcode=payload.scan_barcode,

            last_scanned_warehouse=payload.last_scanned_warehouse,

            total_qty=payload.total_qty,

            total_net_weight=payload.total_net_weight,

            base_total=payload.base_total,

            base_net_total=payload.base_net_total,

            total=payload.total,

            net_total=payload.net_total,

            tax_category_id=payload.tax_category_id,

            taxes_and_charges_id=payload.taxes_and_charges_id,

            shipping_rule_id=payload.shipping_rule_id,

            incoterm=payload.incoterm,

            named_place=payload.named_place,

            base_total_taxes_and_charges=payload.base_total_taxes_and_charges,

            total_taxes_and_charges=payload.total_taxes_and_charges,

            grand_total=payload.grand_total,

            in_words=payload.in_words,

            rounded_total=payload.rounded_total,

            rounding_adjustment=payload.rounding_adjustment,

            disable_rounded_total=payload.disable_rounded_total,

            base_grand_total=payload.base_grand_total,

            base_in_words=payload.base_in_words,

            base_rounded_total=payload.base_rounded_total,

            base_rounding_adjustment=payload.base_rounding_adjustment,

            apply_discount_on=payload.apply_discount_on,

            base_discount_amount=payload.base_discount_amount,

            coupon_code_id=payload.coupon_code_id,

            additional_discount_percentage=payload.additional_discount_percentage,

            discount_amount=payload.discount_amount,

            referral_sales_partner=payload.referral_sales_partner,

            other_charges_calculation=payload.other_charges_calculation,

            customer_address=payload.customer_address,

            address_display=payload.address_display,

            contact_person=payload.contact_person,

            contact_display=payload.contact_display,

            contact_mobile=payload.contact_mobile,

            contact_email=payload.contact_email,

            shipping_address_name=payload.shipping_address_name,

            shipping_address=payload.shipping_address,

            company_address=payload.company_address,

            company_address_display=payload.company_address_display,

            company_contact_person=payload.company_contact_person,

            payment_terms_template_id=payload.payment_terms_template_id,

            tc_name=payload.tc_name,

            terms=payload.terms,

            auto_repeat=payload.auto_repeat,

            letter_head=payload.letter_head,

            group_same_items=payload.group_same_items,

            select_print_heading=payload.select_print_heading,

            language=payload.language,

            order_lost_reason=payload.order_lost_reason,

            utm_source=payload.utm_source,

            utm_medium=payload.utm_medium,

            utm_campaign=payload.utm_campaign,

            utm_content=payload.utm_content,

            status=payload.status,

            customer_group=payload.customer_group,

            territory=payload.territory,

            title=payload.title,

            opportunity=payload.opportunity,

            enq_det=payload.enq_det,

            supplier_quotation_id=payload.supplier_quotation_id,

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

        payload: QuotationUpdate,

    ) -> Quotation:

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

    ) -> Quotation:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Quotation")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Quotation:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Quotation")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row



    def _replace_items(

        self, business_id: uuid.UUID, row: Quotation, items: list[dict]

    ) -> None:

        row.items.clear()

        for idx, entry in enumerate(items, start=1):

            row.items.append(

                QuotationItem(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Quotation",

                    parentfield="items",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )
