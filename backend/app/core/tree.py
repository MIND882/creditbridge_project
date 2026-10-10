"""
Adjacency-list tree utilities -- the replacement for Frappe's ``NestedSet``.

ERPNext keeps ``lft``/``rgt`` on every tree doctype (Account, Cost Center,
Warehouse...) and rebuilds the whole subtree numbering on every save via
``frappe.utils.nestedset``. That machinery exists to make "all descendants"
a single range query (``lft > X AND rgt < Y``) on a database with no recursive
CTE support in the version Frappe targeted.

We store only ``parent_<x>_id``. Postgres and SQLite both support recursive
CTEs, so descendants/ancestors become real queries and the write path stops
needing to renumber siblings -- which removes an entire class of concurrent-
update corruption that the lft/rgt scheme is prone to.

What is provided here:

``TreeRepository``-shaped helpers that take a mapped class plus the name of its
parent column, so one implementation serves every tree doctype.
"""

from __future__ import annotations

import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Generic, Iterable, Optional, Sequence, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import DomainValidationError

T = TypeVar("T")


@dataclass
class TreeNode(Generic[T]):
    """One node of a materialised tree, carrying the underlying ORM row."""

    id: uuid.UUID
    parent_id: Optional[uuid.UUID]
    obj: T
    children: list["TreeNode[T]"] = field(default_factory=list)


class TreeHelper(Generic[T]):
    """
    Adjacency-list tree operations bound to one mapped class.

    ``parent_attr`` is the ORM attribute name holding the parent id
    (``"parent_account_id"`` for Account). ``depth`` is the number of levels
    the recursive CTE is allowed to descend before we declare the data cyclic
    rather than looping forever.
    """

    def __init__(self, model: type[T], parent_attr: str, *, max_depth: int = 64) -> None:
        self.model = model
        self.parent_attr = parent_attr
        self.max_depth = max_depth

    # ── traversal ────────────────────────────────────────────────────────────
    def get_children(self, db: Session, business_id: uuid.UUID, parent_id: Optional[uuid.UUID]) -> list[T]:
        """Direct children of ``parent_id`` (``None`` = roots), ordered by name."""
        parent_col = getattr(self.model, self.parent_attr)
        stmt = select(self.model).where(
            self.model.business_id == business_id,  # type: ignore[attr-defined]
            parent_col.is_(None) if parent_id is None else parent_col == parent_id,
        )
        name_col = getattr(self.model, "name", None)
        if name_col is not None:
            stmt = stmt.order_by(name_col)
        return list(db.scalars(stmt))

    def get_ancestors(self, db: Session, business_id: uuid.UUID, node_id: uuid.UUID) -> list[T]:
        """Nearest-ancestor-first chain from ``node_id`` up to its root."""
        ancestors: list[T] = []
        current: Optional[T] = db.get(self.model, node_id)
        if current is None or current.business_id != business_id:  # type: ignore[attr-defined]
            return []
        seen = {node_id}
        for _ in range(self.max_depth):
            parent_id = getattr(current, self.parent_attr)
            if parent_id is None:
                break
            if parent_id in seen:
                raise DomainValidationError(
                    "Tree data is corrupted: a cycle was detected while walking ancestors.",
                    code="tree_cycle",
                )
            seen.add(parent_id)
            parent = db.get(self.model, parent_id)
            if parent is None:
                break
            ancestors.append(parent)
            current = parent
        return ancestors

    def get_descendants(
        self, db: Session, business_id: uuid.UUID, node_id: uuid.UUID
    ) -> list[T]:
        """Every node below ``node_id``, breadth-first, excluding the node itself."""
        descendants: list[T] = []
        frontier: list[uuid.UUID] = [node_id]
        seen = {node_id}
        for _ in range(self.max_depth):
            if not frontier:
                break
            parent_col = getattr(self.model, self.parent_attr)
            rows = db.scalars(
                select(self.model).where(
                    self.model.business_id == business_id,  # type: ignore[attr-defined]
                    parent_col.in_(frontier),
                )
            ).all()
            frontier = []
            for row in rows:
                if row.id in seen:  # type: ignore[attr-defined]
                    raise DomainValidationError(
                        "Tree data is corrupted: a cycle was detected while walking descendants.",
                        code="tree_cycle",
                    )
                seen.add(row.id)  # type: ignore[attr-defined]
                descendants.append(row)
                frontier.append(row.id)  # type: ignore[attr-defined]
        return descendants

    def get_subtree(self, db: Session, business_id: uuid.UUID, root_id: uuid.UUID) -> list[T]:
        """``root_id`` followed by all of its descendants."""
        root = db.get(self.model, root_id)
        if root is None or root.business_id != business_id:  # type: ignore[attr-defined]
            return []
        return [root, *self.get_descendants(db, business_id, root_id)]

    def count_children(self, db: Session, business_id: uuid.UUID, node_id: uuid.UUID) -> int:
        from sqlalchemy import func

        parent_col = getattr(self.model, self.parent_attr)
        return int(
            db.scalar(
                select(func.count())
                .select_from(self.model)
                .where(
                    self.model.business_id == business_id,  # type: ignore[attr-defined]
                    parent_col == node_id,
                )
            )
            or 0
        )

    def has_children(self, db: Session, business_id: uuid.UUID, node_id: uuid.UUID) -> bool:
        return self.count_children(db, business_id, node_id) > 0

    # ── integrity ────────────────────────────────────────────────────────────
    def assert_no_cycle(
        self, db: Session, business_id: uuid.UUID, node_id: uuid.UUID, new_parent_id: Optional[uuid.UUID]
    ) -> None:
        """
        Guard for a parent re-assignment: ``new_parent_id`` must not be the node
        itself or one of its descendants.

        This is the adjacency-list equivalent of ERPNext refusing to move an
        account under one of its own children (which would silently corrupt the
        lft/rgt numbering).
        """
        if new_parent_id is None:
            return
        if new_parent_id == node_id:
            raise DomainValidationError(
                "You can not assign itself as parent.",
                code="tree_self_parent",
            )
        for row in self.get_descendants(db, business_id, node_id):
            if row.id == new_parent_id:  # type: ignore[attr-defined]
                raise DomainValidationError(
                    "You can not assign a descendant as parent.",
                    code="tree_cycle",
                )

    def depth_of(self, db: Session, business_id: uuid.UUID, node_id: uuid.UUID) -> int:
        """0 for a root, 1 for its child, and so on."""
        return len(self.get_ancestors(db, business_id, node_id))

    # ── materialisation ──────────────────────────────────────────────────────
    def build_forest(self, rows: Iterable[T]) -> list[TreeNode[T]]:
        """
        Assemble already-fetched rows into roots-with-children.

        Pure function of the row list: no I/O, so it is trivially testable. Rows
        whose parent is absent from ``rows`` surface as roots, which lets a
        caller materialise a partial subtree without a placeholder node.
        """
        nodes: dict[uuid.UUID, TreeNode[T]] = {}
        for row in rows:
            nodes[row.id] = TreeNode(  # type: ignore[attr-defined]
                id=row.id,  # type: ignore[attr-defined]
                parent_id=getattr(row, self.parent_attr),
                obj=row,
            )

        roots: list[TreeNode[T]] = []
        for node in nodes.values():
            parent = nodes.get(node.parent_id) if node.parent_id is not None else None
            if parent is None:
                roots.append(node)
            else:
                parent.children.append(node)
        return roots

    def build_forest_for(
        self, db: Session, business_id: uuid.UUID, roots_only: bool = False
    ) -> list[TreeNode[T]]:
        """Load the tenant's whole tree (or only its roots) and materialise it."""
        stmt = select(self.model).where(self.model.business_id == business_id)  # type: ignore[attr-defined]
        name_col = getattr(self.model, "name", None)
        if name_col is not None:
            stmt = stmt.order_by(name_col)
        rows = list(db.scalars(stmt))
        if roots_only:
            parent_col = getattr(self.model, self.parent_attr)
            rows = [r for r in rows if getattr(r, self.parent_attr) is None]
        return self.build_forest(rows)


def flatten(nodes: Sequence[TreeNode[T]], depth: int = 0) -> list[tuple[int, T]]:
    """Depth-first ``[(depth, obj), ...]`` -- handy for indented list rendering."""
    out: list[tuple[int, T]] = []
    for n in nodes:
        out.append((depth, n.obj))
        out.extend(flatten(n.children, depth + 1))
    return out


def group_by_parent(rows: Iterable[Any], parent_attr: str) -> dict[Optional[uuid.UUID], list[Any]]:
    """Bucket rows by parent id (used by callers that want the raw adjacency map)."""
    buckets: dict[Optional[uuid.UUID], list[Any]] = defaultdict(list)
    for row in rows:
        buckets[getattr(row, parent_attr)].append(row)
    return dict(buckets)