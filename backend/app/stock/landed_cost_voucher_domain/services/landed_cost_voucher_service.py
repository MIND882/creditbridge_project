"""Business logic for Landed Cost Voucher -- port of

``erpnext/stock/doctype/landed_cost_voucher/landed_cost_voucher.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream has 15 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.landed_cost_voucher_domain.models.landed_cost_voucher import LandedCostVoucher

from app.stock.landed_cost_voucher_domain.repositories.landed_cost_voucher_repository import (

    LandedCostVoucherRepository,

)

from app.stock.landed_cost_voucher_domain.schemas.landed_cost_voucher import (

    LandedCostVoucherCreate,

    LandedCostVoucherUpdate,

)

from app.stock.landed_cost_purchase_receipt_domain.models.landed_cost_purchase_receipt import LandedCostPurchaseReceipt

from app.stock.landed_cost_item_domain.models.landed_cost_item import LandedCostItem

from app.stock.landed_cost_taxes_and_charges_domain.models.landed_cost_taxes_and_charges import LandedCostTaxesAndCharges

from app.stock.landed_cost_vendor_invoice_domain.models.landed_cost_vendor_invoice import LandedCostVendorInvoice

from app.core.errors import NotFoundError

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.pagination import ResultPage



__all__ = ["LandedCostVoucherService"]





class LandedCostVoucherService:

    def __init__(self, repository: Optional[LandedCostVoucherRepository] = None) -> None:

        self.repository = repository or LandedCostVoucherRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> LandedCostVoucher:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Landed Cost Voucher", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: LandedCostVoucher

    ) -> None:

        """

        Upstream has 15 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> LandedCostVoucher:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[LandedCostVoucher]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[LandedCostVoucher].build(

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

                select(func.count()).select_from(LandedCostVoucher).where(

                    LandedCostVoucher.business_id == business_id

                )

            )

            or 0

        )

        return f"{prefix}{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: LandedCostVoucherCreate

    ) -> LandedCostVoucher:

        row = LandedCostVoucher(

            business_id=business_id,

            name=self.next_name(db, business_id, payload.naming_series),

            naming_series=payload.naming_series,

            company=payload.company,

            total_taxes_and_charges=payload.total_taxes_and_charges,

            distribute_charges_based_on=payload.distribute_charges_based_on,

            amended_from_id=payload.amended_from_id,

            posting_date=payload.posting_date,

            total_vendor_invoices_cost=payload.total_vendor_invoices_cost,

        )

        self._replace_purchase_receipts(business_id, row, [x.model_dump() for x in payload.purchase_receipts])

        self._replace_items(business_id, row, [x.model_dump() for x in payload.items])

        self._replace_taxes(business_id, row, [x.model_dump() for x in payload.taxes])

        self._replace_vendor_invoices(business_id, row, [x.model_dump() for x in payload.vendor_invoices])



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

        payload: LandedCostVoucherUpdate,

    ) -> LandedCostVoucher:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "purchase_receipts":

                    self._replace_purchase_receipts(business_id, row, value or [])

                    continue

                if field_name == "items":

                    self._replace_items(business_id, row, value or [])

                    continue

                if field_name == "taxes":

                    self._replace_taxes(business_id, row, value or [])

                    continue

                if field_name == "vendor_invoices":

                    self._replace_vendor_invoices(business_id, row, value or [])

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

    ) -> LandedCostVoucher:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Landed Cost Voucher")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> LandedCostVoucher:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Landed Cost Voucher")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row



    def _replace_purchase_receipts(

        self, business_id: uuid.UUID, row: LandedCostVoucher, purchase_receipts: list[dict]

    ) -> None:

        row.purchase_receipts.clear()

        for idx, entry in enumerate(purchase_receipts, start=1):

            row.purchase_receipts.append(

                LandedCostPurchaseReceipt(

                    business_id=business_id,

                    idx=idx,

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_items(

        self, business_id: uuid.UUID, row: LandedCostVoucher, items: list[dict]

    ) -> None:

        row.items.clear()

        for idx, entry in enumerate(items, start=1):

            row.items.append(

                LandedCostItem(

                    business_id=business_id,

                    idx=idx,

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_taxes(

        self, business_id: uuid.UUID, row: LandedCostVoucher, taxes: list[dict]

    ) -> None:

        row.taxes.clear()

        for idx, entry in enumerate(taxes, start=1):

            row.taxes.append(

                LandedCostTaxesAndCharges(

                    business_id=business_id,

                    idx=idx,

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_vendor_invoices(

        self, business_id: uuid.UUID, row: LandedCostVoucher, vendor_invoices: list[dict]

    ) -> None:

        row.vendor_invoices.clear()

        for idx, entry in enumerate(vendor_invoices, start=1):

            row.vendor_invoices.append(

                LandedCostVendorInvoice(

                    business_id=business_id,

                    idx=idx,

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )
