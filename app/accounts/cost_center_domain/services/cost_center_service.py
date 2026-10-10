"""

Business logic for Cost Center -- port of

``erpnext/accounts/doctype/cost_center/cost_center.py``.



Upstream hook -> here

-------------------

``autoname`` / ``get_name_with_number``  :func:`build_cost_center_name`

``validate``                             :meth:`_validate`

``validate_mandatory``                   :meth:`_validate_mandatory`

``validate_parent_cost_center``          :meth:`_validate_parent`

``convert_group_to_ledger``              :meth:`convert_to_ledger`

``convert_ledger_to_group``              :meth:`convert_to_group`

``check_if_child_exists``                ``TreeHelper.has_children``

``check_gle_exists``                     ``CostCenterGLGateway``

``if_allocation_exists_against_cost_center``     :meth:`_allocation_as_main_exists`

``check_if_part_of_cost_center_allocation``      :meth:`_allocation_as_child_exists`

``before_rename`` / ``after_rename``     not ported -- see note below



**Root detection.** Upstream decides "is this the root?" by comparing

``cost_center_name == company``, because ERPNext seeds the root cost centre

with the company's name. There is no Company doctype here, so the equivalent

test is ``parent_cost_center_id IS NULL`` -- which is the distinction

``validate_mandatory`` is really making.



**Rename hooks not ported.** ``before_rename`` / ``after_rename`` exist to keep

Frappe's name-derived ``cost_center_name`` / ``cost_center_number`` in sync

when a document is renamed in place. Here ``name`` is a stored column the

service regenerates from its inputs, so there is no rename event to hook.

"""



from __future__ import annotations



import uuid

from typing import Optional, Protocol, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.cost_center_domain.models.cost_center import CostCenter

from app.accounts.cost_center_domain.repositories.cost_center_repository import (

    CostCenterRepository,

)

from app.accounts.cost_center_domain.schemas.cost_center import (

    CostCenterCreate,

    CostCenterTreeNode,

    CostCenterUpdate,

)

from app.core.errors import ConflictError, DomainValidationError, NotFoundError

from app.core.pagination import ResultPage

from app.core.tree import TreeHelper



__all__ = [

    "CostCenterService",

    "CostCenterGLGateway",

    "GLEntryCostCenterGateway",

    "NullCostCenterGLGateway",

    "build_cost_center_name",

]





class CostCenterGLGateway(Protocol):

    """

    GL Entry lookups keyed on ``cost_center``.



    Port of ``check_gle_exists``: ``frappe.db.get_value("GL Entry",

    {"cost_center": self.name})``. GL Entry is not converted yet, so this is

    the seam where it plugs in.

    """



    def any_entry_exists(self, db: Session, business_id: uuid.UUID, cost_center_id: uuid.UUID) -> bool: ...





class NullCostCenterGLGateway:

    """

    Reports "no entries" regardless of the ledger.



    Kept for tests that need to exercise cost-centre deletion without standing up

    a GL. It is no longer the default -- :class:`GLEntryCostCenterGateway` is.

    """



    def any_entry_exists(self, db: Session, business_id: uuid.UUID, cost_center_id: uuid.UUID) -> bool:

        return False





class GLEntryCostCenterGateway:

    """

    The real implementation, backed by ``gl_entries``.



    The GL Entry repository is imported inside the method: ``gl_entry`` models

    import ``CostCenter``, so a module-level import here would be circular.

    """



    def any_entry_exists(self, db: Session, business_id: uuid.UUID, cost_center_id: uuid.UUID) -> bool:

        from app.accounts.gl_entry_domain.repositories.gl_entry_repository import (

            GLEntryRepository,

        )



        return GLEntryRepository().has_entries_for_cost_center(db, business_id, cost_center_id)





def build_cost_center_name(

    cost_center_number: Optional[str],

    cost_center_name: str,

    company_abbr: Optional[str] = None,

) -> str:

    """

    Port of ``get_name_with_number`` + ``get_autoname_with_number``.



    Upstream::



        if account_number and not new_account[0].isdigit():

            new_account = account_number + " - " + new_account



    i.e. the number is prefixed unless the name already starts with one, so

    renaming does not double-prefix.

    """

    name = (cost_center_name or "").strip()

    parts = [name] + ([company_abbr.strip()] if company_abbr and company_abbr.strip() else [])

    number = (cost_center_number or "").strip()

    if number and not name[:1].isdigit():

        parts.insert(0, number)

    return " - ".join(parts)





class CostCenterService:

    def __init__(

        self,

        repository: Optional[CostCenterRepository] = None,

        *,

        gl_gateway: Optional[CostCenterGLGateway] = None,

        company_abbr: Optional[str] = None,

    ) -> None:

        self.repository = repository or CostCenterRepository()

        self.gl = gl_gateway or GLEntryCostCenterGateway()

        self.company_abbr = company_abbr

        self.tree: TreeHelper[CostCenter] = TreeHelper(CostCenter, "parent_cost_center_id")



    # ── helpers ──────────────────────────────────────────────────────────────

    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, cost_center_id: uuid.UUID

    ) -> CostCenter:

        row = self.repository.get_by_id(db, business_id, cost_center_id)

        if row is None:

            raise NotFoundError("Cost Center", cost_center_id)

        return row



    def _build_name(self, number: Optional[str], name: str) -> str:

        return build_cost_center_name(number, name, self.company_abbr)



    def _allocation_as_main_exists(

        self, db: Session, business_id: uuid.UUID, cost_center_id: uuid.UUID

    ) -> bool:

        """

        Port of ``if_allocation_exists_against_cost_center``.



        Upstream filters ``main_cost_center == self.name, docstatus == 1``.

        """

        from app.accounts.cost_center_allocation_domain.models.cost_center_allocation import (

            CostCenterAllocation,

        )



        return bool(

            db.scalar(

                select(func.count())

                .select_from(CostCenterAllocation)

                .where(

                    CostCenterAllocation.business_id == business_id,

                    CostCenterAllocation.main_cost_center_id == cost_center_id,

                    CostCenterAllocation.docstatus == 1,

                )

            )

        )



    def _allocation_as_child_exists(

        self, db: Session, business_id: uuid.UUID, cost_center_id: uuid.UUID

    ) -> bool:

        """

        Port of ``check_if_part_of_cost_center_allocation``.



        Upstream filters the percentage child table by ``cost_center`` and

        ``docstatus == 1``.

        """

        from app.accounts.cost_center_allocation_domain.models.cost_center_allocation import (

            CostCenterAllocation,

        )

        from app.accounts.cost_center_allocation_percentage_domain.models.cost_center_allocation_percentage import (

            CostCenterAllocationPercentage,

        )



        return bool(

            db.scalar(

                select(func.count())

                .select_from(CostCenterAllocationPercentage)

                .join(

                    CostCenterAllocation,

                    CostCenterAllocationPercentage.parent_id == CostCenterAllocation.id,

                )

                .where(

                    CostCenterAllocationPercentage.business_id == business_id,

                    CostCenterAllocationPercentage.cost_center_id == cost_center_id,

                    CostCenterAllocation.docstatus == 1,

                )

            )

        )



    # ── ported validators ────────────────────────────────────────────────────

    def _validate_mandatory(self, cost_center: CostCenter) -> None:

        """

        Port of ``validate_mandatory``.



        Upstream::



            if self.cost_center_name != self.company and not self.parent_cost_center:

                throw("Please enter parent cost center")

            elif self.cost_center_name == self.company and self.parent_cost_center:

                throw("Root cannot have a parent cost center")



        ``cost_center_name == company`` is ERPNext's "this is the root" test,

        which becomes ``parent_cost_center_id is None`` here.

        """

        if cost_center.parent_cost_center_id is None and not cost_center.is_group:

            raise DomainValidationError(

                f"The root cost center {cost_center.cost_center_name} must be a group",

                code="cost_center_root_must_be_group",

            )



    def _validate_parent(

        self,

        db: Session,

        business_id: uuid.UUID,

        parent_id: Optional[uuid.UUID],

        self_id: Optional[uuid.UUID],

    ) -> Optional[CostCenter]:

        """Port of ``validate_parent_cost_center`` -- parent must be a group."""

        if parent_id is None:

            return None



        parent = self.repository.get_by_id(db, business_id, parent_id)

        if parent is None:

            raise DomainValidationError(

                f"Parent cost center {parent_id} does not exist",

                code="cost_center_parent_not_found",

            )

        if self_id is not None and parent.id == self_id:

            raise DomainValidationError(

                "You can not assign itself as parent cost center",

                code="cost_center_parent_is_self",

            )

        if not parent.is_group:

            raise DomainValidationError(

                f"{parent.cost_center_name} is not a group node. "

                "Please select a group node as parent cost center",

                code="cost_center_parent_not_group",

            )

        return parent



    def _validate_number(

        self,

        db: Session,

        business_id: uuid.UUID,

        number: Optional[str],

        *,

        exclude_id: Optional[uuid.UUID] = None,

    ) -> None:

        if not number:

            return

        clash = self.repository.find_by_number(db, business_id, number, exclude_id=exclude_id)

        if clash is not None:

            raise ConflictError(

                f"Cost Center Number {number} already used in cost center {clash.cost_center_name}",

                code="cost_center_number_duplicate",

            )



    # ── public API ───────────────────────────────────────────────────────────

    def get(self, db: Session, business_id: uuid.UUID, cost_center_id: uuid.UUID) -> CostCenter:

        return self._get_or_404(db, business_id, cost_center_id)



    def list(self, db: Session, business_id: uuid.UUID, **filters: object) -> ResultPage[CostCenter]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[CostCenter].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def create(

        self, db: Session, business_id: uuid.UUID, payload: CostCenterCreate

    ) -> CostCenter:

        self._validate_parent(db, business_id, payload.parent_cost_center_id, None)

        self._validate_number(db, business_id, payload.cost_center_number)



        row = CostCenter(

            business_id=business_id,

            name=self._build_name(payload.cost_center_number, payload.cost_center_name),

            cost_center_name=payload.cost_center_name,

            cost_center_number=payload.cost_center_number,

            parent_cost_center_id=payload.parent_cost_center_id,

            is_group=payload.is_group,

            disabled=payload.disabled,

        )

        try:

            self.repository.add(db, row)

            self._validate_mandatory(row)

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

        cost_center_id: uuid.UUID,

        payload: CostCenterUpdate,

    ) -> CostCenter:

        row = self._get_or_404(db, business_id, cost_center_id)

        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            if "parent_cost_center_id" in changes:

                self.tree.assert_no_cycle(db, business_id, row.id, changes["parent_cost_center_id"])

                row.parent_cost_center_id = changes["parent_cost_center_id"]



            for field_name in ("cost_center_name", "cost_center_number", "disabled"):

                if field_name in changes:

                    setattr(row, field_name, changes[field_name])



            if "cost_center_name" in changes or "cost_center_number" in changes:

                row.name = self._build_name(row.cost_center_number, row.cost_center_name)



            self._validate_parent(db, business_id, row.parent_cost_center_id, row.id)

            self._validate_number(

                db, business_id, row.cost_center_number, exclude_id=row.id

            )

            self._validate_mandatory(row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def delete(self, db: Session, business_id: uuid.UUID, cost_center_id: uuid.UUID) -> None:

        row = self._get_or_404(db, business_id, cost_center_id)



        if self.gl.any_entry_exists(db, business_id, row.id):

            raise DomainValidationError(

                "Cost Center with existing transactions can not be deleted",

                code="cost_center_has_gl_entries",

            )

        if self.tree.has_children(db, business_id, row.id):

            raise DomainValidationError(

                "Cannot delete Cost Center as it has child nodes",

                code="cost_center_has_children",

            )



        self.repository.delete(db, row)

        db.commit()



    # ── conversion ───────────────────────────────────────────────────────────

    def convert_to_ledger(

        self, db: Session, business_id: uuid.UUID, cost_center_id: uuid.UUID

    ) -> CostCenter:

        """Port of ``convert_group_to_ledger``."""

        row = self._get_or_404(db, business_id, cost_center_id)



        if row.parent_cost_center_id is None:

            raise DomainValidationError(

                f"The root cost center {row.cost_center_name} must be a group",

                code="cost_center_root_must_be_group",

            )

        if self.tree.has_children(db, business_id, row.id):

            raise DomainValidationError(

                "Cannot convert Cost Center to ledger as it has child nodes",

                code="cost_center_has_children",

            )

        if self.gl.any_entry_exists(db, business_id, row.id):

            raise DomainValidationError(

                "Cost Center with existing transactions can not be converted to ledger",

                code="cost_center_has_gl_entries",

            )



        row.is_group = False

        db.commit()

        db.refresh(row)

        return row



    def convert_to_group(

        self, db: Session, business_id: uuid.UUID, cost_center_id: uuid.UUID

    ) -> CostCenter:

        """

        Port of ``convert_ledger_to_group``.



        Three guards, in upstream order: an allocation record *against* this

        cost centre, this cost centre appearing *inside* another allocation,

        then GL entries.

        """

        row = self._get_or_404(db, business_id, cost_center_id)



        if self._allocation_as_main_exists(db, business_id, row.id):

            raise DomainValidationError(

                "Cost Center with Allocation records can not be converted to a group",

                code="cost_center_has_allocation",

            )

        if self._allocation_as_child_exists(db, business_id, row.id):

            raise DomainValidationError(

                "Cost Center is a part of Cost Center Allocation, "

                "hence cannot be converted to a group",

                code="cost_center_part_of_allocation",

            )

        if self.gl.any_entry_exists(db, business_id, row.id):

            raise DomainValidationError(

                "Cost Center with existing transactions can not be converted to group",

                code="cost_center_has_gl_entries",

            )



        row.is_group = True

        db.commit()

        db.refresh(row)

        return row



    # ── tree ─────────────────────────────────────────────────────────────────

    def get_tree(

        self, db: Session, business_id: uuid.UUID

    ) -> tuple[list[CostCenterTreeNode], int]:

        rows = self.repository.list_all(db, business_id)

        forest = self.tree.build_forest(rows)



        def convert(nodes: Sequence[object], depth: int = 0) -> list[CostCenterTreeNode]:

            out: list[CostCenterTreeNode] = []

            for node in nodes:  # type: ignore[union-attr]

                obj = node.obj  # type: ignore[attr-defined]

                out.append(

                    CostCenterTreeNode(

                        id=obj.id,

                        name=obj.name,

                        cost_center_name=obj.cost_center_name,

                        cost_center_number=obj.cost_center_number,

                        parent_cost_center_id=obj.parent_cost_center_id,

                        is_group=obj.is_group,

                        disabled=obj.disabled,

                        depth=depth,

                        children=convert(node.children, depth + 1),  # type: ignore[attr-defined]

                    )

                )

            return out



        return convert(forest), len(rows)



    def list_parent_options(

        self, db: Session, business_id: uuid.UUID, *, search: Optional[str] = None

    ) -> list[CostCenter]:

        return self.repository.list_groups(db, business_id, search=search)
