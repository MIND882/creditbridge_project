"""

Data access for Account.



Every statement filters on ``business_id``. Note in particular

:meth:`get_by_name` and :meth:`find_by_account_number`: both take

``business_id`` as a required first argument, so there is no overload that can

be called without it.

"""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.account_domain.models.account import Account

from app.core.pagination import normalise_paging



__all__ = ["AccountRepository"]





class AccountRepository:

    model = Account



    # ── single-row reads ─────────────────────────────────────────────────────

    def get_by_id(

        self, db: Session, business_id: uuid.UUID, account_id: uuid.UUID

    ) -> Optional[Account]:

        return db.scalar(

            select(Account).where(

                Account.business_id == business_id,

                Account.id == account_id,

            )

        )



    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[Account]:

        """

        Lookup by the ERPNext document ``name``.



        This is what makes ``frappe.get_doc("Account", name)`` calls portable --

        upstream code refers to accounts by name everywhere.

        """

        return db.scalar(

            select(Account).where(

                Account.business_id == business_id,

                Account.name == name,

            )

        )



    def find_by_account_number(

        self,

        db: Session,

        business_id: uuid.UUID,

        account_number: str,

        *,

        exclude_id: Optional[uuid.UUID] = None,

    ) -> Optional[Account]:

        """

        Port of the lookup inside ``validate_account_number``.



        Upstream excludes the row itself with ``name != self.name``; here the

        exclusion is by id, which is the equivalent on a UUID key.

        """

        conditions = [

            Account.business_id == business_id,

            Account.account_number == account_number,

        ]

        if exclude_id is not None:

            conditions.append(Account.id != exclude_id)

        return db.scalar(select(Account).where(*conditions))



    def find_by_account_name(

        self,

        db: Session,

        business_id: uuid.UUID,

        account_name: str,

        *,

        parent_account_id: Optional[uuid.UUID] = None,

    ) -> Optional[Account]:

        """Used to keep sibling names distinct under one parent."""

        conditions = [

            Account.business_id == business_id,

            Account.account_name == account_name,

        ]

        if parent_account_id is None:

            conditions.append(Account.parent_account_id.is_(None))

        else:

            conditions.append(Account.parent_account_id == parent_account_id)

        return db.scalar(select(Account).where(*conditions))



    # ── collection reads ─────────────────────────────────────────────────────

    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        search: Optional[str] = None,

        root_type: Optional[str] = None,

        account_type: Optional[str] = None,

        is_group: Optional[bool] = None,

        include_disabled: bool = True,

        parent_account_id: Optional[uuid.UUID] = None,

        roots_only: bool = False,

    ) -> tuple[Sequence[Account], int]:

        offset, limit = normalise_paging(offset, limit)



        conditions = [Account.business_id == business_id]

        if search:

            pattern = f"%{search}%"

            conditions.append(

                Account.account_name.ilike(pattern) | Account.name.ilike(pattern)

            )

        if root_type:

            conditions.append(Account.root_type == root_type)

        if account_type:

            conditions.append(Account.account_type == account_type)

        if is_group is not None:

            conditions.append(Account.is_group.is_(is_group))

        if not include_disabled:

            conditions.append(Account.disabled.is_(False))

        if roots_only:

            conditions.append(Account.parent_account_id.is_(None))

        elif parent_account_id is not None:

            conditions.append(Account.parent_account_id == parent_account_id)



        total = int(db.scalar(select(func.count()).select_from(Account).where(*conditions)) or 0)

        rows = db.scalars(

            select(Account)

            .where(*conditions)

            .order_by(Account.account_name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total



    def list_all(self, db: Session, business_id: uuid.UUID) -> list[Account]:

        """Whole tenant tree -- the input to the tree builder."""

        return list(

            db.scalars(

                select(Account)

                .where(Account.business_id == business_id)

                .order_by(Account.account_name.asc())

            )

        )



    def list_groups(

        self, db: Session, business_id: uuid.UUID, *, search: Optional[str] = None

    ) -> list[Account]:

        """

        Port of ``get_parent_account``: the picker source for choosing a parent.



        Upstream filters ``is_group == 1``, ``docstatus != 2`` and the company.

        Account has no docstatus, so that clause drops out.

        """

        conditions = [

            Account.business_id == business_id,

            Account.is_group.is_(True),

        ]

        if search:

            conditions.append(Account.account_name.ilike(f"%{search}%"))

        return list(

            db.scalars(select(Account).where(*conditions).order_by(Account.account_name.asc()))

        )



    # ── counts used by guards ────────────────────────────────────────────────

    def count_children(

        self, db: Session, business_id: uuid.UUID, account_id: uuid.UUID

    ) -> int:

        """

        Port of ``check_if_child_exists``.



        Upstream adds ``docstatus != 2`` (not cancelled). Account is not

        submittable, so the filter reduces to the parent match.

        """

        return int(

            db.scalar(

                select(func.count())

                .select_from(Account)

                .where(

                    Account.business_id == business_id,

                    Account.parent_account_id == account_id,

                )

            )

            or 0

        )



    def count_by_category(

        self, db: Session, business_id: uuid.UUID, account_category: str

    ) -> int:

        """How many Accounts reference a category label (delete guard)."""

        return int(

            db.scalar(

                select(func.count())

                .select_from(Account)

                .where(

                    Account.business_id == business_id,

                    Account.account_category == account_category,

                )

            )

            or 0

        )



    # ── writes ───────────────────────────────────────────────────────────────

    def add(self, db: Session, account: Account) -> Account:

        db.add(account)

        db.flush()

        return account



    def delete(self, db: Session, account: Account) -> None:

        db.delete(account)

        db.flush()



    def update_subtree_classification(

        self,

        db: Session,

        business_id: uuid.UUID,

        descendant_ids: Sequence[uuid.UUID],

        *,

        root_type: Optional[str] = None,

        report_type: Optional[str] = None,

    ) -> int:

        """

        Port of the bulk update inside ``set_root_and_report_type``.



        Upstream scopes it with ``(Account.lft > self.lft) & (Account.rgt < self.rgt)``

        -- the NestedSet spelling of "everything below me". The adjacency-list

        spelling is an explicit id list produced by the tree helper, which is

        why the caller passes ``descendant_ids``.

        """

        from sqlalchemy import update



        if not descendant_ids:

            return 0



        values: dict[str, object] = {}

        if root_type is not None:

            values["root_type"] = root_type

        if report_type is not None:

            values["report_type"] = report_type

        if not values:

            return 0



        result = db.execute(

            update(Account)

            .where(

                Account.business_id == business_id,

                Account.id.in_(descendant_ids),

            )

            .values(**values)

        )

        db.flush()

        return int(result.rowcount or 0)
