"""

Business logic for Cost Center Allocation -- port of

``erpnext/accounts/doctype/cost_center_allocation/cost_center_allocation.py``.



Upstream hook -> here

-------------------

``autoname`` (CC-ALLOC-.#####)              ``repository.next_name``

``validate``                                :meth:`_validate` (same order)

``validate_total_allocation_percentage``    :meth:`_validate_total_percentage`

``validate_from_date_based_on_existing_gle`` :meth:`_validate_from_date_vs_gle`

``validate_backdated_allocation``           :meth:`_warn_backdated_allocation`

``validate_main_cost_center``               :meth:`_validate_main_cost_center`

``validate_child_cost_centers``             :meth:`_validate_child_cost_centers`

submit / cancel / amend                     :meth:`submit` / :meth:`cancel` / :meth:`amend`



``frappe.throw`` -> DomainValidationError (400). ``frappe.msgprint`` (the

backdated-allocation notice) is a warning that does not abort, so it is

returned rather than raised -- there is no server-push channel here.

"""



from __future__ import annotations



import uuid

from dataclasses import dataclass, field

from datetime import date, timedelta

from decimal import Decimal

from typing import Optional, Protocol, Sequence



from sqlalchemy.orm import Session



from app.accounts.cost_center_allocation_domain.models.cost_center_allocation import (

    CostCenterAllocation,

)

from app.accounts.cost_center_allocation_domain.repositories.cost_center_allocation_repository import (

    CostCenterAllocationRepository,

)

from app.accounts.cost_center_allocation_domain.schemas.cost_center_allocation import (

    CostCenterAllocationCreate,

    CostCenterAllocationUpdate,

)

from app.accounts.cost_center_allocation_percentage_domain.models.cost_center_allocation_percentage import (

    CostCenterAllocationPercentage,

)

from app.accounts.cost_center_domain.repositories.cost_center_repository import (

    CostCenterRepository,

)

from app.core.docstatus import (

    DocStatus,

    assert_can_amend,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = [

    "CostCenterAllocationService",

    "AllocationGLGateway",

    "NullAllocationGLGateway",

    "SaveOutcome",

]



#: The split must total exactly this. Compared as Decimal, never float.

TOTAL_PERCENTAGE = Decimal("100")





class AllocationGLGateway(Protocol):

    """

    Last GL Entry date for a cost centre.



    Port of ``validate_from_date_based_on_existing_gle``'s lookup. GL Entry is

    not converted yet, so this is the seam where it plugs in.

    """



    def last_entry_date(

        self, db: Session, business_id: uuid.UUID, cost_center_id: uuid.UUID

    ) -> Optional[date]: ...





class NullAllocationGLGateway:

    """

    Reports "no entries" regardless of the ledger.



    Kept for tests that need to exercise allocation dates without standing up a

    GL. It is no longer the default -- :class:`GLEntryAllocationGateway` is.

    """



    def last_entry_date(

        self, db: Session, business_id: uuid.UUID, cost_center_id: uuid.UUID

    ) -> Optional[date]:

        return None





class GLEntryAllocationGateway:

    """

    The real implementation, backed by ``gl_entries``.



    Imported lazily inside the method: ``gl_entry`` models import ``CostCenter``,

    so a module-level import here would be circular.

    """



    def last_entry_date(

        self, db: Session, business_id: uuid.UUID, cost_center_id: uuid.UUID

    ) -> Optional[date]:

        from app.accounts.gl_entry_domain.repositories.gl_entry_repository import (

            GLEntryRepository,

        )



        return GLEntryRepository().last_entry_date_for_cost_center(

            db, business_id, cost_center_id

        )





@dataclass

class SaveOutcome:

    allocation: CostCenterAllocation

    warnings: list[str] = field(default_factory=list)





class CostCenterAllocationService:

    def __init__(

        self,

        repository: Optional[CostCenterAllocationRepository] = None,

        *,

        gl_gateway: Optional[AllocationGLGateway] = None,

        cost_center_repository: Optional[CostCenterRepository] = None,

    ) -> None:

        self.repository = repository or CostCenterAllocationRepository()

        self.gl = gl_gateway or GLEntryAllocationGateway()

        self.cost_centers = cost_center_repository or CostCenterRepository()



    # ── helpers ──────────────────────────────────────────────────────────────

    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, allocation_id: uuid.UUID

    ) -> CostCenterAllocation:

        row = self.repository.get_by_id(db, business_id, allocation_id)

        if row is None:

            raise NotFoundError("Cost Center Allocation", allocation_id)

        return row



    def _assert_cost_center_exists(

        self, db: Session, business_id: uuid.UUID, cost_center_id: uuid.UUID, label: str

    ) -> None:

        if self.cost_centers.get_by_id(db, business_id, cost_center_id) is None:

            raise DomainValidationError(

                f"{label} {cost_center_id} does not exist",

                code="cost_center_not_found",

            )



    # ── ported validators ────────────────────────────────────────────────────

    @staticmethod

    def _validate_total_percentage(percentages: Sequence[Decimal]) -> None:

        """

        Port of ``validate_total_allocation_percentage``.



        Compared exactly, so the column must be Decimal -- summing floats would

        make a legitimate 100% split fail on representation error.

        """

        total = sum((Decimal(str(p)) for p in percentages), Decimal("0"))

        if total != TOTAL_PERCENTAGE:

            raise DomainValidationError(

                f"Total percentage against cost centers should be 100 (got {total})",

                code="allocation_percentage_not_100",

            )



    def _validate_from_date_vs_gle(

        self,

        db: Session,

        business_id: uuid.UUID,

        main_cost_center_id: uuid.UUID,

        valid_from: date,

    ) -> None:

        """

        Port of ``validate_from_date_based_on_existing_gle``.



        ``valid_from`` must be strictly *after* the last GL Entry against the

        main cost centre -- an allocation cannot retroactively re-split

        postings that already exist.

        """

        last_gle_date = self.gl.last_entry_date(db, business_id, main_cost_center_id)

        if last_gle_date is not None and valid_from <= last_gle_date:

            raise DomainValidationError(

                f"Valid From must be after {last_gle_date} as last GL Entry against "

                "the cost center posted on this date",

                code="allocation_valid_from_before_gle",

            )



    def _warn_backdated_allocation(

        self,

        db: Session,

        business_id: uuid.UUID,

        main_cost_center_id: uuid.UUID,

        valid_from: date,

        *,

        exclude_id: Optional[uuid.UUID] = None,

    ) -> Optional[str]:

        """

        Port of ``validate_backdated_allocation``.



        Upstream this is a ``msgprint`` alert, not a throw -- it informs the

        user that a later allocation truncates this one. Returned as a string.

        """

        future = self.repository.find_future_allocation(

            db, business_id, main_cost_center_id, valid_from, exclude_id=exclude_id

        )

        if future is None:

            return None

        applicable_upto = future.valid_from - timedelta(days=1)

        return (

            f"Another Cost Center Allocation record {future.name} applicable from "

            f"{future.valid_from}, hence this allocation will be applicable upto {applicable_upto}"

        )



    def _validate_main_cost_center(

        self,

        db: Session,

        business_id: uuid.UUID,

        main_cost_center_id: uuid.UUID,

        child_ids: Sequence[uuid.UUID],

    ) -> None:

        """

        Port of ``validate_main_cost_center`` -- two distinct rules.



        1. the main cost centre may not appear in its own child table;

        2. a cost centre already used as a *child* in a submitted allocation

           may not become a main (that would nest allocations).

        """

        if main_cost_center_id in child_ids:

            raise DomainValidationError(

                "Main Cost Center cannot be entered in the child table",

                code="allocation_main_in_child_table",

            )



        from sqlalchemy import func, select



        from app.accounts.cost_center_allocation_percentage_domain.models.cost_center_allocation_percentage import (

            CostCenterAllocationPercentage,

        )



        used_as_child_parent_id = db.scalar(

            select(CostCenterAllocationPercentage.parent_id)

            .join(

                CostCenterAllocation,

                CostCenterAllocationPercentage.parent_id == CostCenterAllocation.id,

            )

            .where(

                CostCenterAllocationPercentage.business_id == business_id,

                CostCenterAllocationPercentage.cost_center_id == main_cost_center_id,

                CostCenterAllocation.docstatus == 1,

            )

            .limit(1)

        )

        if used_as_child_parent_id is not None:

            parent = self.repository.get_by_id(db, business_id, used_as_child_parent_id)

            parent_name = parent.name if parent else used_as_child_parent_id

            raise DomainValidationError(

                "This cost center cannot be used as a Main Cost Center because it has "

                f"been used as child in Cost Center Allocation {parent_name}",

                code="allocation_main_used_as_child",

            )



    def _validate_child_cost_centers(

        self,

        db: Session,

        business_id: uuid.UUID,

        child_ids: Sequence[uuid.UUID],

    ) -> None:

        """

        Port of ``validate_child_cost_centers``.



        A cost centre that is a *main* somewhere cannot be a child here.

        """

        main_ids = self.repository.list_main_cost_center_ids(db, business_id)

        for child_id in child_ids:

            if child_id in main_ids:

                raise DomainValidationError(

                    "Cost Center cannot be used for allocation as it is used as main "

                    "cost center in other allocation record.",

                    code="allocation_child_used_as_main",

                )



    # ── the chain ────────────────────────────────────────────────────────────

    def _validate(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        main_cost_center_id: uuid.UUID,

        valid_from: date,

        percentages: Sequence[Decimal],

        child_ids: Sequence[uuid.UUID],

        exclude_id: Optional[uuid.UUID] = None,

        skip_from_date_validation: bool = False,

    ) -> list[str]:

        """Port of ``validate``, preserving upstream call order."""

        warnings: list[str] = []



        self._validate_total_percentage(percentages)

        if not skip_from_date_validation:

            self._validate_from_date_vs_gle(db, business_id, main_cost_center_id, valid_from)

        warning = self._warn_backdated_allocation(

            db, business_id, main_cost_center_id, valid_from, exclude_id=exclude_id

        )

        if warning:

            warnings.append(warning)

        self._validate_main_cost_center(db, business_id, main_cost_center_id, child_ids)

        self._validate_child_cost_centers(db, business_id, child_ids)

        return warnings



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, allocation_id: uuid.UUID

    ) -> CostCenterAllocation:

        return self._get_or_404(db, business_id, allocation_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[CostCenterAllocation]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[CostCenterAllocation].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def create(

        self, db: Session, business_id: uuid.UUID, payload: CostCenterAllocationCreate

    ) -> SaveOutcome:

        self._assert_cost_center_exists(

            db, business_id, payload.main_cost_center_id, "Main Cost Center"

        )

        for row in payload.allocation_percentages:

            self._assert_cost_center_exists(db, business_id, row.cost_center_id, "Cost Center")



        child_ids = [r.cost_center_id for r in payload.allocation_percentages]

        warnings = self._validate(

            db,

            business_id,

            main_cost_center_id=payload.main_cost_center_id,

            valid_from=payload.valid_from,

            percentages=[r.percentage for r in payload.allocation_percentages],

            child_ids=child_ids,

        )



        allocation = CostCenterAllocation(

            business_id=business_id,

            name=self.repository.next_name(db, business_id),

            main_cost_center_id=payload.main_cost_center_id,

            valid_from=payload.valid_from,

            amended_from_id=payload.amended_from_id,

            docstatus=DocStatus.DRAFT.value,

        )

        # idx is 1-based, matching Frappe's row numbering.

        for idx, row in enumerate(payload.allocation_percentages, start=1):

            allocation.allocation_percentages.append(

                CostCenterAllocationPercentage(

                    business_id=business_id,

                    idx=idx,

                    cost_center_id=row.cost_center_id,

                    percentage=row.percentage,

                )

            )



        try:

            self.repository.add(db, allocation)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(allocation)

        return SaveOutcome(allocation=allocation, warnings=warnings)



    def update(

        self,

        db: Session,

        business_id: uuid.UUID,

        allocation_id: uuid.UUID,

        payload: CostCenterAllocationUpdate,

    ) -> SaveOutcome:

        allocation = self._get_or_404(db, business_id, allocation_id)

        if not allocation.is_draft:

            raise DomainValidationError(

                "Only a draft Cost Center Allocation can be edited. "

                "Cancel and amend it instead.",

                code="allocation_not_editable",

            )



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return SaveOutcome(allocation=allocation)



        try:

            if "valid_from" in changes:

                allocation.valid_from = changes["valid_from"]



            if "allocation_percentages" in changes:

                allocation.allocation_percentages.clear()

                for idx, row in enumerate(changes["allocation_percentages"], start=1):

                    self._assert_cost_center_exists(

                        db, business_id, row["cost_center_id"], "Cost Center"

                    )

                    allocation.allocation_percentages.append(

                        CostCenterAllocationPercentage(

                            business_id=business_id,

                            idx=idx,

                            cost_center_id=row["cost_center_id"],

                            percentage=row["percentage"],

                        )

                    )

            db.flush()



            child_ids = [r.cost_center_id for r in allocation.allocation_percentages]

            warnings = self._validate(

                db,

                business_id,

                main_cost_center_id=allocation.main_cost_center_id,

                valid_from=allocation.valid_from,

                percentages=[r.percentage for r in allocation.allocation_percentages],

                child_ids=child_ids,

                exclude_id=allocation.id,

            )

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(allocation)

        return SaveOutcome(allocation=allocation, warnings=warnings)



    def delete(self, db: Session, business_id: uuid.UUID, allocation_id: uuid.UUID) -> None:

        """Only a draft can be deleted; a submitted one must be cancelled first."""

        allocation = self._get_or_404(db, business_id, allocation_id)

        if not allocation.is_draft:

            raise DomainValidationError(

                "Only a draft Cost Center Allocation can be deleted. Cancel it first.",

                code="allocation_not_deletable",

            )

        self.repository.delete(db, allocation)

        db.commit()



    # ── lifecycle ────────────────────────────────────────────────────────────

    def submit(

        self, db: Session, business_id: uuid.UUID, allocation_id: uuid.UUID

    ) -> CostCenterAllocation:

        allocation = self._get_or_404(db, business_id, allocation_id)

        assert_can_submit(allocation, "Cost Center Allocation")

        allocation.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(allocation)

        return allocation



    def cancel(

        self, db: Session, business_id: uuid.UUID, allocation_id: uuid.UUID

    ) -> CostCenterAllocation:

        allocation = self._get_or_404(db, business_id, allocation_id)

        assert_can_cancel(allocation, "Cost Center Allocation")

        allocation.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(allocation)

        return allocation



    def amend(

        self, db: Session, business_id: uuid.UUID, allocation_id: uuid.UUID

    ) -> CostCenterAllocation:

        """

        Copy a cancelled allocation into a new draft, linked by ``amended_from``.



        Upstream's ``copy_doc`` + amend flow. The name is regenerated so the

        cancelled original keeps its identity.

        """

        source = self._get_or_404(db, business_id, allocation_id)

        assert_can_amend(source, "Cost Center Allocation")



        clone = CostCenterAllocation(

            business_id=business_id,

            name=self.repository.next_name(db, business_id),

            main_cost_center_id=source.main_cost_center_id,

            valid_from=source.valid_from,

            amended_from_id=source.id,

            docstatus=DocStatus.DRAFT.value,

        )

        for row in source.allocation_percentages:

            clone.allocation_percentages.append(

                CostCenterAllocationPercentage(

                    business_id=business_id,

                    idx=row.idx,

                    cost_center_id=row.cost_center_id,

                    percentage=row.percentage,

                )

            )



        self.repository.add(db, clone)

        db.commit()

        db.refresh(clone)

        return clone
