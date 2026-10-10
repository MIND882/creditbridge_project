# HAND-WRITTEN

"""

Business logic for Process Period Closing Voucher -- port of

``erpnext/accounts/doctype/process_period_closing_voucher/process_period_closing_voucher.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream hooks:

    on_discard

    validate

    populate_processing_tables

    get_dates

    generate_pcv_dates

    generate_opening_balances_dates

    on_submit

    on_cancel



Upstream declares no validation, so `_validate` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.process_period_closing_voucher_domain.models.process_period_closing_voucher import ProcessPeriodClosingVoucher

from app.accounts.process_period_closing_voucher_detail_domain.models.process_period_closing_voucher_detail import ProcessPeriodClosingVoucherDetail

from app.accounts.process_period_closing_voucher_detail_domain.models.process_period_closing_voucher_detail import ProcessPeriodClosingVoucherDetail

from app.accounts.process_period_closing_voucher_domain.repositories.process_period_closing_voucher_repository import (

    ProcessPeriodClosingVoucherRepository,

)

from app.accounts.process_period_closing_voucher_domain.schemas.process_period_closing_voucher import (

    ProcessPeriodClosingVoucherCreate,

    ProcessPeriodClosingVoucherUpdate,

)

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ProcessPeriodClosingVoucherService"]





class ProcessPeriodClosingVoucherService:

    def __init__(self, repository: Optional[ProcessPeriodClosingVoucherRepository] = None) -> None:

        self.repository = repository or ProcessPeriodClosingVoucherRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProcessPeriodClosingVoucher:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Process Period Closing Voucher", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: ProcessPeriodClosingVoucher

    ) -> None:

        """

        Upstream's controller defines no ``frappe.throw``, so there is

        no rule to port. Empty by design, not by omission.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProcessPeriodClosingVoucher:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ProcessPeriodClosingVoucher]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ProcessPeriodClosingVoucher].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_normal_balances(

        self, business_id: uuid.UUID, row: ProcessPeriodClosingVoucher, items: list[dict]

    ) -> None:

        row.normal_balances.clear()

        for idx, item in enumerate(items, start=1):

            row.normal_balances.append(

                ProcessPeriodClosingVoucherDetail(

                    business_id=business_id,

                    idx=idx,

                    parenttype='Process Period Closing Voucher',

                    processing_date=item.get('processing_date'),

                    status=item.get('status'),

                    closing_balance=item.get('closing_balance'),

                    report_type=item.get('report_type'),

                )

            )



    def _replace_z_opening_balances(

        self, business_id: uuid.UUID, row: ProcessPeriodClosingVoucher, items: list[dict]

    ) -> None:

        row.z_opening_balances.clear()

        for idx, item in enumerate(items, start=1):

            row.z_opening_balances.append(

                ProcessPeriodClosingVoucherDetail(

                    business_id=business_id,

                    idx=idx,

                    parenttype='Process Period Closing Voucher',

                    processing_date=item.get('processing_date'),

                    status=item.get('status'),

                    closing_balance=item.get('closing_balance'),

                    report_type=item.get('report_type'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(ProcessPeriodClosingVoucher).where(

                    ProcessPeriodClosingVoucher.business_id == business_id

                )

            )

            or 0

        )

        return f"PRO-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: ProcessPeriodClosingVoucherCreate

    ) -> ProcessPeriodClosingVoucher:

        row = ProcessPeriodClosingVoucher(

            business_id=business_id,

            name=self.next_name(db, business_id),

            parent_pcv=payload.parent_pcv,

            status=payload.status,

            amended_from=payload.amended_from,

            p_l_closing_balance=payload.p_l_closing_balance,

            bs_closing_balance=payload.bs_closing_balance,

        )

        self._replace_normal_balances(business_id, row, [x.model_dump() for x in payload.normal_balances])

        self._replace_z_opening_balances(business_id, row, [x.model_dump() for x in payload.z_opening_balances])



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

        payload: ProcessPeriodClosingVoucherUpdate,

    ) -> ProcessPeriodClosingVoucher:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "normal_balances":

                    self._replace_normal_balances(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "z_opening_balances":

                    self._replace_z_opening_balances(business_id, row, value or [])

                else:

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

    ) -> ProcessPeriodClosingVoucher:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Process Period Closing Voucher")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProcessPeriodClosingVoucher:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Process Period Closing Voucher")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row
