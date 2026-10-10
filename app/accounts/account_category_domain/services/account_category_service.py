


from __future__ import annotations



import uuid

from typing import Any, Iterable, Optional, Sequence



from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError



from app.accounts.account_category_domain.models.account_category import AccountCategory

from app.accounts.account_category_domain.repositories.account_category_repository import (

    AccountCategoryRepository,

)

from app.accounts.account_category_domain.schemas.account_category import (

    AccountCategoryCreate,

    AccountCategoryUpdate,

)

from app.accounts.enums import RootType

from app.core.errors import ConflictError, DomainValidationError, NotFoundError
from app.core.db_helpers import commit_or_conflict

from app.core.pagination import ResultPage



__all__ = ["AccountCategoryService"]





class AccountCategoryService:

    def __init__(self, repository: Optional[AccountCategoryRepository] = None) -> None:

        self.repository = repository or AccountCategoryRepository()



    # ── helpers ──────────────────────────────────────────────────────────────

    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, category_id: uuid.UUID

    ) -> AccountCategory:

        category = self.repository.get_by_id(db, business_id, category_id)

        if category is None:

            raise NotFoundError("Account Category", category_id)

        return category



    @staticmethod

    def _validate(payload: AccountCategoryCreate | AccountCategoryUpdate, *, partial: bool) -> None:

        """

        Port of ERPNext's implicit ``reqd`` handling plus a shape check.



        Frappe raises ``MandatoryError`` for a blank required field; that

        surfaces as a 400 here with a stable code.

        """

        if partial:

            return

        name = getattr(payload, "account_category_name", None)

        if not name or not str(name).strip():

            raise DomainValidationError(

                "Account Category Name is mandatory",

                code="account_category_name_mandatory",

            )



    def _assert_name_free(

        self,

        db: Session,

        business_id: uuid.UUID,

        account_category_name: str,

        *,

        exclude_id: Optional[uuid.UUID] = None,

    ) -> None:

        existing = self.repository.get_by_name(db, business_id, account_category_name)

        if existing is not None and existing.id != exclude_id:

            raise ConflictError(

                f"Account Category '{account_category_name}' already exists",

                code="account_category_duplicate",

                details={"account_category_name": account_category_name},

            )



    # ── reads ────────────────────────────────────────────────────────────────

    def get(self, db: Session, business_id: uuid.UUID, category_id: uuid.UUID) -> AccountCategory:

        return self._get_or_404(db, business_id, category_id)



    def get_by_name(

        self, db: Session, business_id: uuid.UUID, account_category_name: str

    ) -> AccountCategory:

        category = self.repository.get_by_name(db, business_id, account_category_name)

        if category is None:

            raise NotFoundError("Account Category", account_category_name)

        return category



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        search: Optional[str] = None,

        root_type: Optional[RootType] = None,

    ) -> ResultPage[AccountCategory]:

        rows, total = self.repository.list(

            db,

            business_id,

            offset=offset,

            limit=limit,

            search=search,

            root_type=root_type.value if root_type else None,

        )

        return ResultPage[AccountCategory].build(rows, total=total, offset=offset, limit=limit)



    # ── writes ───────────────────────────────────────────────────────────────

    def create(

        self, db: Session, business_id: uuid.UUID, payload: AccountCategoryCreate

    ) -> AccountCategory:

        self._validate(payload, partial=False)

        self._assert_name_free(db, business_id, payload.account_category_name)



        category = AccountCategory(

            business_id=business_id,

            account_category_name=payload.account_category_name,

            description=payload.description,

            root_type=payload.root_type,

        )

        self.repository.add(db, category)

        commit_or_conflict(
            db,
            message=f"Account Category '{payload.account_category_name}' already exists",
            code="account_category_duplicate",
        )

        db.refresh(category)

        return category



    def update(

        self,

        db: Session,

        business_id: uuid.UUID,

        category_id: uuid.UUID,

        payload: AccountCategoryUpdate,

    ) -> AccountCategory:

        category = self._get_or_404(db, business_id, category_id)

        self._validate(payload, partial=True)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return category



        old_name = category.account_category_name

        new_name = changes.get("account_category_name")



        if new_name is not None and new_name != old_name:

            if not str(new_name).strip():

                raise DomainValidationError(

                    "Account Category Name is mandatory",

                    code="account_category_name_mandatory",

                )

            self._assert_name_free(db, business_id, new_name, exclude_id=category.id)

            category.account_category_name = new_name



        if "description" in changes:

            category.description = changes["description"]

        if "root_type" in changes:

            category.root_type = changes["root_type"]



        commit_or_conflict(
        db,
        message=f"Account Category '{new_name or old_name}' already exists",
        code="account_category_duplicate",
       )

        db.refresh(category)



        if new_name is not None and new_name != old_name:

            self.after_rename(db, business_id, category, old_name, new_name)

            db.commit()

        return category



    def delete(self, db: Session, business_id: uuid.UUID, category_id: uuid.UUID) -> None:

        category = self._get_or_404(db, business_id, category_id)



        # Accounts still point at this category. ERPNext's Link field makes the

        # delete fail with a LinkExistsError; we surface the same outcome.

        from app.accounts.account_domain.repositories.account_repository import AccountRepository



        in_use = AccountRepository().count_by_category(db, business_id, category.account_category_name)

        if in_use:

            raise DomainValidationError(

                f"Cannot delete Account Category '{category.account_category_name}': "

                f"{in_use} Account(s) still reference it",

                code="account_category_in_use",

                details={"account_count": in_use},

            )



        self.repository.delete(db, category)

        db.commit()



    # ── ported module functions ──────────────────────────────────────────────

    def bulk_create(
        self, db: Session, business_id: uuid.UUID, categories: Iterable[dict[str, Any]]
    ) -> list[AccountCategory]:

        created: list[AccountCategory] = []
        existing = set(self.repository.list_all_names(db, business_id))

        for data in categories:
            name = data.get("account_category_name")

            if not name or name in existing:
                continue

            category = AccountCategory(
                business_id=business_id,
                account_category_name=name,
                description=data.get("description"),
                root_type=data.get("root_type") or None,
            )

            try:
                with db.begin_nested():
                    self.repository.add(db, category)

            except IntegrityError:
                continue

            created.append(category)
            existing.add(name)

        if created:
            db.commit()

        return created



    def after_rename(

        self,

        db: Session,

        business_id: uuid.UUID,

        category: AccountCategory,

        old_name: str,

        new_name: str,

    ) -> None:

        """

        Port of ``AccountCategory.after_rename``.



        TODO(accounts-conversion): upstream rewrites

        ``Financial Report Row.calculation_formula`` for every row whose formula

        contains ``old_name``. That doctype is not converted yet, so there is

        nothing to rewrite. When ``financial_report_row`` lands, this is the

        hook that must call its formula updater -- it is deliberately kept as a

        named method (rather than folded into :meth:`update`) so the call site

        already exists.

        """

        return None



    # ── convenience for other domains ────────────────────────────────────────

    def root_type_for(

        self, db: Session, business_id: uuid.UUID, account_category_name: Optional[str]

    ) -> Optional[RootType]:

        """

        Resolve a category label to its root type.



        ``Account.create`` uses this to pre-fill ``root_type``, which is what

        makes the category worth having. Unknown labels yield ``None`` instead

        of raising: a stale label on an imported account should not block the

        account's creation.

        """

        if not account_category_name:

            return None

        category = self.repository.get_by_name(db, business_id, account_category_name)

        return category.root_type if category else None



    def all_as_rows(

        self, db: Session, business_id: uuid.UUID

    ) -> Sequence[AccountCategory]:  # pragma: no cover - convenience

        rows, _ = self.repository.list(db, business_id, offset=0, limit=100)

        return rows
