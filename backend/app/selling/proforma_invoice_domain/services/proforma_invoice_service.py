"""Business logic for Proforma Invoice -- port of

``erpnext/selling/doctype/proforma_invoice/proforma_invoice.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.selling.proforma_invoice_domain.models.proforma_invoice import ProformaInvoice

from app.selling.proforma_invoice_domain.repositories.proforma_invoice_repository import (

    ProformaInvoiceRepository,

)

from app.selling.proforma_invoice_domain.schemas.proforma_invoice import (

    ProformaInvoiceCreate,

    ProformaInvoiceUpdate,

)

from app.selling.proforma_invoice_item_domain.models.proforma_invoice_item import ProformaInvoiceItem

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ProformaInvoiceService"]





class ProformaInvoiceService:

    def __init__(self, repository: Optional[ProformaInvoiceRepository] = None) -> None:

        self.repository = repository or ProformaInvoiceRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProformaInvoice:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Proforma Invoice", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: ProformaInvoice

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProformaInvoice:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ProformaInvoice]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ProformaInvoice].build(

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

                select(func.count()).select_from(ProformaInvoice).where(

                    ProformaInvoice.business_id == business_id

                )

            )

            or 0

        )

        return f"{prefix}{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: ProformaInvoiceCreate

    ) -> ProformaInvoice:

        row = ProformaInvoice(

            business_id=business_id,

            name=self.next_name(db, business_id, payload.naming_series),

            naming_series=payload.naming_series,

            sales_order_id=payload.sales_order_id,

            customer_id=payload.customer_id,

            customer_name=payload.customer_name,

            company=payload.company,

            proforma_date=payload.proforma_date,

            currency=payload.currency,

            based_on=payload.based_on,

            hide_item_qty=payload.hide_item_qty,

            total_qty=payload.total_qty,

            grand_total=payload.grand_total,

            print_format=payload.print_format,

            letter_head=payload.letter_head,

            proforma_pdf=payload.proforma_pdf,

            status=payload.status,

            sent_on=payload.sent_on,

            emailed_to=payload.emailed_to,

            amended_from_id=payload.amended_from_id,

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

        payload: ProformaInvoiceUpdate,

    ) -> ProformaInvoice:

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



    def _replace_items(

        self, business_id: uuid.UUID, row: ProformaInvoice, items: list[dict]

    ) -> None:

        row.items.clear()

        for idx, entry in enumerate(items, start=1):

            row.items.append(

                ProformaInvoiceItem(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Proforma Invoice",

                    parentfield="items",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )
