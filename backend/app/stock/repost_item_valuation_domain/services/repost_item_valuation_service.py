"""Business logic for Repost Item Valuation -- port of

``erpnext/stock/doctype/repost_item_valuation/repost_item_valuation.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream has 7 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.repost_item_valuation_domain.models.repost_item_valuation import RepostItemValuation

from app.stock.repost_item_valuation_domain.repositories.repost_item_valuation_repository import (

    RepostItemValuationRepository,

)

from app.stock.repost_item_valuation_domain.schemas.repost_item_valuation import (

    RepostItemValuationCreate,

    RepostItemValuationUpdate,

)

from app.core.errors import NotFoundError

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.pagination import ResultPage



__all__ = ["RepostItemValuationService"]





class RepostItemValuationService:

    def __init__(self, repository: Optional[RepostItemValuationRepository] = None) -> None:

        self.repository = repository or RepostItemValuationRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> RepostItemValuation:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Repost Item Valuation", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: RepostItemValuation

    ) -> None:

        """

        Upstream has 7 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> RepostItemValuation:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[RepostItemValuation]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[RepostItemValuation].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def create(

        self, db: Session, business_id: uuid.UUID, payload: RepostItemValuationCreate

    ) -> RepostItemValuation:

        row = RepostItemValuation(

            business_id=business_id,

            item_code_id=payload.item_code_id,

            warehouse_id=payload.warehouse_id,

            posting_date=payload.posting_date,

            posting_time=payload.posting_time,

            status=payload.status,

            amended_from_id=payload.amended_from_id,

            error_log=payload.error_log,

            company=payload.company,

            voucher_type=payload.voucher_type,

            voucher_no=payload.voucher_no,

            based_on=payload.based_on,

            allow_negative_stock=payload.allow_negative_stock,

            via_landed_cost_voucher=payload.via_landed_cost_voucher,

            allow_zero_rate=payload.allow_zero_rate,

            items_to_be_repost=payload.items_to_be_repost,

            current_index=payload.current_index,

            gl_reposting_index=payload.gl_reposting_index,

            total_reposting_count=payload.total_reposting_count,

            recreate_stock_ledgers=payload.recreate_stock_ledgers,

            reposting_reference=payload.reposting_reference,

            repost_only_accounting_ledgers=payload.repost_only_accounting_ledgers,

            total_vouchers=payload.total_vouchers,

            vouchers_posted=payload.vouchers_posted,

            reposting_data_file=payload.reposting_data_file,

            recalculate_valuation_rate=payload.recalculate_valuation_rate,

        )



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

        payload: RepostItemValuationUpdate,

    ) -> RepostItemValuation:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

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

    ) -> RepostItemValuation:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Repost Item Valuation")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> RepostItemValuation:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Repost Item Valuation")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row
