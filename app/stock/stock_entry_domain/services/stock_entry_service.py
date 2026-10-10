"""Business logic for Stock Entry -- port of

``erpnext/stock/doctype/stock_entry/stock_entry.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream has 15 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.stock_entry_domain.models.stock_entry import StockEntry

from app.stock.stock_entry_domain.repositories.stock_entry_repository import (

    StockEntryRepository,

)

from app.stock.stock_entry_domain.schemas.stock_entry import (

    StockEntryCreate,

    StockEntryUpdate,

)

from app.stock.stock_entry_detail_domain.models.stock_entry_detail import StockEntryDetail

from app.core.errors import NotFoundError

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.pagination import ResultPage



__all__ = ["StockEntryService"]





class StockEntryService:

    def __init__(self, repository: Optional[StockEntryRepository] = None) -> None:

        self.repository = repository or StockEntryRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> StockEntry:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Stock Entry", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: StockEntry

    ) -> None:

        """

        Upstream has 15 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> StockEntry:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[StockEntry]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[StockEntry].build(

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

                select(func.count()).select_from(StockEntry).where(

                    StockEntry.business_id == business_id

                )

            )

            or 0

        )

        return f"{prefix}{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: StockEntryCreate

    ) -> StockEntry:

        row = StockEntry(

            business_id=business_id,

            name=self.next_name(db, business_id, payload.naming_series),

            naming_series=payload.naming_series,

            stock_entry_type_id=payload.stock_entry_type_id,

            outgoing_stock_entry_id=payload.outgoing_stock_entry_id,

            source_stock_entry_id=payload.source_stock_entry_id,

            purpose=payload.purpose,

            company=payload.company,

            work_order=payload.work_order,

            purchase_order=payload.purchase_order,

            subcontracting_order=payload.subcontracting_order,

            delivery_note_no_id=payload.delivery_note_no_id,

            sales_invoice_no_id=payload.sales_invoice_no_id,

            purchase_receipt_no_id=payload.purchase_receipt_no_id,

            posting_date=payload.posting_date,

            posting_time=payload.posting_time,

            set_posting_time=payload.set_posting_time,

            inspection_required=payload.inspection_required,

            from_bom=payload.from_bom,

            bom_no=payload.bom_no,

            fg_completed_qty=payload.fg_completed_qty,

            use_multi_level_bom=payload.use_multi_level_bom,

            from_warehouse_id=payload.from_warehouse_id,

            source_warehouse_address=payload.source_warehouse_address,

            source_address_display=payload.source_address_display,

            to_warehouse_id=payload.to_warehouse_id,

            target_warehouse_address=payload.target_warehouse_address,

            target_address_display=payload.target_address_display,

            scan_barcode=payload.scan_barcode,

            total_incoming_value=payload.total_incoming_value,

            total_outgoing_value=payload.total_outgoing_value,

            value_difference=payload.value_difference,

            total_additional_costs=payload.total_additional_costs,

            supplier=payload.supplier,

            supplier_name=payload.supplier_name,

            supplier_address=payload.supplier_address,

            address_display=payload.address_display,

            select_print_heading=payload.select_print_heading,

            letter_head=payload.letter_head,

            is_opening=payload.is_opening,

            project=payload.project,

            remarks=payload.remarks,

            per_transferred=payload.per_transferred,

            total_amount=payload.total_amount,

            job_card=payload.job_card,

            amended_from_id=payload.amended_from_id,

            credit_note_id=payload.credit_note_id,

            pick_list_id=payload.pick_list_id,

            add_to_transit=payload.add_to_transit,

            apply_putaway_rule=payload.apply_putaway_rule,

            is_return=payload.is_return,

            process_loss_qty=payload.process_loss_qty,

            process_loss_percentage=payload.process_loss_percentage,

            asset_repair=payload.asset_repair,

            last_scanned_warehouse=payload.last_scanned_warehouse,

            is_additional_transfer_entry=payload.is_additional_transfer_entry,

            subcontracting_inward_order=payload.subcontracting_inward_order,

            cost_center_id=payload.cost_center_id,

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

        payload: StockEntryUpdate,

    ) -> StockEntry:

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

    ) -> StockEntry:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Stock Entry")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> StockEntry:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Stock Entry")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row



    def _replace_items(

        self, business_id: uuid.UUID, row: StockEntry, items: list[dict]

    ) -> None:

        row.items.clear()

        for idx, entry in enumerate(items, start=1):

            row.items.append(

                StockEntryDetail(

                    business_id=business_id,

                    idx=idx,

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )
