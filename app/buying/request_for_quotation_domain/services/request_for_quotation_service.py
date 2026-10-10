"""Business logic for Request for Quotation -- port of

``erpnext/buying/doctype/request_for_quotation/request_for_quotation.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.buying.request_for_quotation_domain.models.request_for_quotation import RequestForQuotation

from app.buying.request_for_quotation_domain.repositories.request_for_quotation_repository import (

    RequestForQuotationRepository,

)

from app.buying.request_for_quotation_domain.schemas.request_for_quotation import (

    RequestForQuotationCreate,

    RequestForQuotationUpdate,

)

from app.buying.request_for_quotation_supplier_domain.models.request_for_quotation_supplier import RequestForQuotationSupplier

from app.buying.request_for_quotation_item_domain.models.request_for_quotation_item import RequestForQuotationItem

from app.core.errors import NotFoundError

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.pagination import ResultPage



__all__ = ["RequestForQuotationService"]





class RequestForQuotationService:

    def __init__(self, repository: Optional[RequestForQuotationRepository] = None) -> None:

        self.repository = repository or RequestForQuotationRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> RequestForQuotation:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Request for Quotation", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: RequestForQuotation

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> RequestForQuotation:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[RequestForQuotation]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[RequestForQuotation].build(

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

                select(func.count()).select_from(RequestForQuotation).where(

                    RequestForQuotation.business_id == business_id

                )

            )

            or 0

        )

        return f"{prefix}{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: RequestForQuotationCreate

    ) -> RequestForQuotation:

        row = RequestForQuotation(

            business_id=business_id,

            name=self.next_name(db, business_id, payload.naming_series),

            naming_series=payload.naming_series,

            company=payload.company,

            vendor_id=payload.vendor_id,

            transaction_date=payload.transaction_date,

            email_template=payload.email_template,

            message_for_supplier=payload.message_for_supplier,

            tc_name=payload.tc_name,

            terms=payload.terms,

            select_print_heading=payload.select_print_heading,

            letter_head=payload.letter_head,

            opportunity=payload.opportunity,

            status=payload.status,

            amended_from_id=payload.amended_from_id,

            schedule_date=payload.schedule_date,

            incoterm=payload.incoterm,

            named_place=payload.named_place,

            send_attached_files=payload.send_attached_files,

            send_document_print=payload.send_document_print,

            billing_address=payload.billing_address,

            billing_address_display=payload.billing_address_display,

            has_unit_price_items=payload.has_unit_price_items,

            subject=payload.subject,

            mfs_html=payload.mfs_html,

            use_html=payload.use_html,

            shipping_address=payload.shipping_address,

            shipping_address_display=payload.shipping_address_display,

            title=payload.title,

        )

        self._replace_suppliers(business_id, row, [x.model_dump() for x in payload.suppliers])

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

        payload: RequestForQuotationUpdate,

    ) -> RequestForQuotation:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "suppliers":

                    self._replace_suppliers(business_id, row, value or [])

                    continue

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

    ) -> RequestForQuotation:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Request for Quotation")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> RequestForQuotation:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Request for Quotation")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row



    def _replace_suppliers(

        self, business_id: uuid.UUID, row: RequestForQuotation, suppliers: list[dict]

    ) -> None:

        row.suppliers.clear()

        for idx, entry in enumerate(suppliers, start=1):

            row.suppliers.append(

                RequestForQuotationSupplier(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Request for Quotation",

                    parentfield="suppliers",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_items(

        self, business_id: uuid.UUID, row: RequestForQuotation, items: list[dict]

    ) -> None:

        row.items.clear()

        for idx, entry in enumerate(items, start=1):

            row.items.append(

                RequestForQuotationItem(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Request for Quotation",

                    parentfield="items",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )
