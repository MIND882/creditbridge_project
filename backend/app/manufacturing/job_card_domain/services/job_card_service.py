"""Business logic for Job Card -- port of

``erpnext/manufacturing/doctype/job_card/job_card.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.job_card_domain.models.job_card import JobCard

from app.manufacturing.job_card_domain.repositories.job_card_repository import (

    JobCardRepository,

)

from app.manufacturing.job_card_domain.schemas.job_card import (

    JobCardCreate,

    JobCardUpdate,

)

from app.manufacturing.job_card_item_domain.models.job_card_item import JobCardItem

from app.manufacturing.job_card_scheduled_time_domain.models.job_card_scheduled_time import JobCardScheduledTime

from app.manufacturing.job_card_time_log_domain.models.job_card_time_log import JobCardTimeLog

from app.manufacturing.job_card_operation_domain.models.job_card_operation import JobCardOperation

from app.manufacturing.job_card_secondary_item_domain.models.job_card_secondary_item import JobCardSecondaryItem

from app.core.errors import NotFoundError

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.pagination import ResultPage



__all__ = ["JobCardService"]





class JobCardService:

    def __init__(self, repository: Optional[JobCardRepository] = None) -> None:

        self.repository = repository or JobCardRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> JobCard:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Job Card", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: JobCard

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> JobCard:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[JobCard]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[JobCard].build(

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

                select(func.count()).select_from(JobCard).where(

                    JobCard.business_id == business_id

                )

            )

            or 0

        )

        return f"{prefix}{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: JobCardCreate

    ) -> JobCard:

        row = JobCard(

            business_id=business_id,

            name=self.next_name(db, business_id, payload.naming_series),

            work_order_id=payload.work_order_id,

            production_item_id=payload.production_item_id,

            bom_no_id=payload.bom_no_id,

            for_quantity=payload.for_quantity,

            stock_uom_id=payload.stock_uom_id,

            company=payload.company,

            naming_series=payload.naming_series,

            posting_date=payload.posting_date,

            finished_good_id=payload.finished_good_id,

            semi_fg_bom_id=payload.semi_fg_bom_id,

            pending_qty=payload.pending_qty,

            process_loss_qty=payload.process_loss_qty,

            total_completed_qty=payload.total_completed_qty,

            transferred_qty=payload.transferred_qty,

            manufactured_qty=payload.manufactured_qty,

            operation_id=payload.operation_id,

            source_warehouse_id=payload.source_warehouse_id,

            wip_warehouse_id=payload.wip_warehouse_id,

            skip_material_transfer=payload.skip_material_transfer,

            backflush_from_wip_warehouse=payload.backflush_from_wip_warehouse,

            workstation_type_id=payload.workstation_type_id,

            workstation_id=payload.workstation_id,

            target_warehouse_id=payload.target_warehouse_id,

            quality_inspection_template_id=payload.quality_inspection_template_id,

            quality_inspection_id=payload.quality_inspection_id,

            expected_start_date=payload.expected_start_date,

            time_required=payload.time_required,

            expected_end_date=payload.expected_end_date,

            actual_start_date=payload.actual_start_date,

            total_time_in_mins=payload.total_time_in_mins,

            actual_end_date=payload.actual_end_date,

            for_job_card_id=payload.for_job_card_id,

            is_corrective_job_card=payload.is_corrective_job_card,

            hour_rate=payload.hour_rate,

            for_operation_id=payload.for_operation_id,

            item_name=payload.item_name,

            requested_qty=payload.requested_qty,

            is_paused=payload.is_paused,

            is_subcontracted=payload.is_subcontracted,

            track_semi_finished_goods=payload.track_semi_finished_goods,

            project=payload.project,

            remarks=payload.remarks,

            status=payload.status,

            operation_row_id=payload.operation_row_id,

            amended_from_id=payload.amended_from_id,

            sequence_id=payload.sequence_id,

            serial_no=payload.serial_no,

            serial_and_batch_bundle_id=payload.serial_and_batch_bundle_id,

            batch_no_id=payload.batch_no_id,

        )

        self._replace_items(business_id, row, [x.model_dump() for x in payload.items])

        self._replace_scheduled_time_logs(business_id, row, [x.model_dump() for x in payload.scheduled_time_logs])

        self._replace_time_logs(business_id, row, [x.model_dump() for x in payload.time_logs])

        self._replace_sub_operations(business_id, row, [x.model_dump() for x in payload.sub_operations])

        self._replace_secondary_items(business_id, row, [x.model_dump() for x in payload.secondary_items])



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

        payload: JobCardUpdate,

    ) -> JobCard:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "items":

                    self._replace_items(business_id, row, value or [])

                    continue

                if field_name == "scheduled_time_logs":

                    self._replace_scheduled_time_logs(business_id, row, value or [])

                    continue

                if field_name == "time_logs":

                    self._replace_time_logs(business_id, row, value or [])

                    continue

                if field_name == "sub_operations":

                    self._replace_sub_operations(business_id, row, value or [])

                    continue

                if field_name == "secondary_items":

                    self._replace_secondary_items(business_id, row, value or [])

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

    ) -> JobCard:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Job Card")

        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> JobCard:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Job Card")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row



    def _replace_items(

        self, business_id: uuid.UUID, row: JobCard, items: list[dict]

    ) -> None:

        row.items.clear()

        for idx, entry in enumerate(items, start=1):

            row.items.append(

                JobCardItem(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Job Card",

                    parentfield="items",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_scheduled_time_logs(

        self, business_id: uuid.UUID, row: JobCard, scheduled_time_logs: list[dict]

    ) -> None:

        row.scheduled_time_logs.clear()

        for idx, entry in enumerate(scheduled_time_logs, start=1):

            row.scheduled_time_logs.append(

                JobCardScheduledTime(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Job Card",

                    parentfield="scheduled_time_logs",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_time_logs(

        self, business_id: uuid.UUID, row: JobCard, time_logs: list[dict]

    ) -> None:

        row.time_logs.clear()

        for idx, entry in enumerate(time_logs, start=1):

            row.time_logs.append(

                JobCardTimeLog(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Job Card",

                    parentfield="time_logs",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_sub_operations(

        self, business_id: uuid.UUID, row: JobCard, sub_operations: list[dict]

    ) -> None:

        row.sub_operations.clear()

        for idx, entry in enumerate(sub_operations, start=1):

            row.sub_operations.append(

                JobCardOperation(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Job Card",

                    parentfield="sub_operations",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_secondary_items(

        self, business_id: uuid.UUID, row: JobCard, secondary_items: list[dict]

    ) -> None:

        row.secondary_items.clear()

        for idx, entry in enumerate(secondary_items, start=1):

            row.secondary_items.append(

                JobCardSecondaryItem(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Job Card",

                    parentfield="secondary_items",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )
