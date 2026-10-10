"""Business logic for Supplier Quotation -- port of

``erpnext/buying/doctype/supplier_quotation/supplier_quotation.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.buying.supplier_quotation_domain.models.supplier_quotation import SupplierQuotation

from app.buying.supplier_quotation_domain.repositories.supplier_quotation_repository import (

    SupplierQuotationRepository,

)

from app.buying.supplier_quotation_domain.schemas.supplier_quotation import (

    SupplierQuotationCreate,

    SupplierQuotationUpdate,

)

from app.buying.supplier_quotation_item_domain.models.supplier_quotation_item import SupplierQuotationItem

from app.core.errors import NotFoundError

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.pagination import ResultPage



__all__ = ["SupplierQuotationService"]





class SupplierQuotationService:

    def __init__(self, repository: Optional[SupplierQuotationRepository] = None) -> None:

        self.repository = repository or SupplierQuotationRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SupplierQuotation:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Supplier Quotation", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: SupplierQuotation

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SupplierQuotation:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[SupplierQuotation]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SupplierQuotation].build(

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

                select(func.count()).select_from(SupplierQuotation).where(

                    SupplierQuotation.business_id == business_id

                )

            )

            or 0

        )

        return f"{prefix}{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: SupplierQuotationCreate

    ) -> SupplierQuotation:

        row = SupplierQuotation(

            business_id=business_id,

            name=self.next_name(db, business_id, payload.naming_series),

            title=payload.title,

            naming_series=payload.naming_series,

            supplier_id=payload.supplier_id,

            supplier_name=payload.supplier_name,

            transaction_date=payload.transaction_date,

            amended_from_id=payload.amended_from_id,

            company=payload.company,

            supplier_address=payload.supplier_address,

            contact_person=payload.contact_person,

            address_display=payload.address_display,

            contact_display=payload.contact_display,

            contact_mobile=payload.contact_mobile,

            contact_email=payload.contact_email,

            currency=payload.currency,

            conversion_rate=payload.conversion_rate,

            buying_price_list_id=payload.buying_price_list_id,

            price_list_currency=payload.price_list_currency,

            plc_conversion_rate=payload.plc_conversion_rate,

            ignore_pricing_rule=payload.ignore_pricing_rule,

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

            in_words=payload.in_words,

            disable_rounded_total=payload.disable_rounded_total,

            tc_name=payload.tc_name,

            terms=payload.terms,

            select_print_heading=payload.select_print_heading,

            group_same_items=payload.group_same_items,

            letter_head=payload.letter_head,

            language=payload.language,

            auto_repeat=payload.auto_repeat,

            status=payload.status,

            is_subcontracted=payload.is_subcontracted,

            opportunity=payload.opportunity,

            valid_till=payload.valid_till,

            quotation_number=payload.quotation_number,

            incoterm=payload.incoterm,

            named_place=payload.named_place,

            shipping_address=payload.shipping_address,

            shipping_address_display=payload.shipping_address_display,

            billing_address=payload.billing_address,

            billing_address_display=payload.billing_address_display,

            cost_center_id=payload.cost_center_id,

            project=payload.project,

            has_unit_price_items=payload.has_unit_price_items,

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

        payload: SupplierQuotationUpdate,

    ) -> SupplierQuotation:

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

    ) -> SupplierQuotation:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Supplier Quotation")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SupplierQuotation:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Supplier Quotation")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row



    def _replace_items(

        self, business_id: uuid.UUID, row: SupplierQuotation, items: list[dict]

    ) -> None:

        row.items.clear()

        for idx, entry in enumerate(items, start=1):

            row.items.append(

                SupplierQuotationItem(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Supplier Quotation",

                    parentfield="items",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )
