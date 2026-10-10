"""

Business logic for Accounting Dimension Filter -- port of

``erpnext/accounts/doctype/accounting_dimension_filter/accounting_dimension_filter.py``.



Upstream's controller is thin (it resolves the dimension list from the

Accounting Dimension doctype and validates the child tables); the enforcement

itself lives in ``erpnext/accounts/doctype/accounting_dimension_filter/

accounting_dimension_filter.py::validate_dimension_filters``, called when a

transaction is saved.



Both halves are here:



:meth:`_validate`      -- the save-time rules (a filter must name a dimension

                          that exists, and must govern at least one account).

:meth:`assert_value_allowed` -- the transaction-time enforcement other domains

                          call before accepting a dimension value.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.accounting_dimension_domain.repositories.accounting_dimension_repository import (

    AccountingDimensionRepository,

)

from app.accounts.accounting_dimension_filter_domain.models.accounting_dimension_filter import (

    AccountingDimensionFilter,

    AllowOrRestrict,

)

from app.accounts.accounting_dimension_filter_domain.repositories.accounting_dimension_filter_repository import (

    AccountingDimensionFilterRepository,

)

from app.accounts.accounting_dimension_filter_domain.schemas.accounting_dimension_filter import (

    AccountingDimensionFilterCreate,

    AccountingDimensionFilterUpdate,

)

from app.accounts.allowed_dimension_domain.models.allowed_dimension import AllowedDimension

from app.accounts.applicable_on_account_domain.models.applicable_on_account import (

    ApplicableOnAccount,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["AccountingDimensionFilterService", "DimensionValueNotAllowedError"]





class DimensionValueNotAllowedError(DomainValidationError):

    """

    Raised when a transaction tries to use a dimension value a filter forbids.



    Distinct class so posting code can catch this one specifically rather than

    matching on message text.

    """



    def __init__(self, message: str, *, dimension: str, value: Optional[str]) -> None:

        super().__init__(message, code="dimension_value_not_allowed")

        self.dimension = dimension

        self.value = value





class AccountingDimensionFilterService:

    def __init__(

        self,

        repository: Optional[AccountingDimensionFilterRepository] = None,

        *,

        dimension_repository: Optional[AccountingDimensionRepository] = None,

    ) -> None:

        self.repository = repository or AccountingDimensionFilterRepository()

        self.dimensions = dimension_repository or AccountingDimensionRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, filter_id: uuid.UUID

    ) -> AccountingDimensionFilter:

        row = self.repository.get_by_id(db, business_id, filter_id)

        if row is None:

            raise NotFoundError("Accounting Dimension Filter", filter_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate_dimension_exists(

        self, db: Session, business_id: uuid.UUID, dimension_label: str

    ) -> None:

        """

        A filter must reference a registered Accounting Dimension.



        Upstream resolves the dimension from the Accounting Dimension doctype;

        a filter naming an unregistered one would simply never fire, so it is

        refused instead.

        """

        if self.dimensions.get_by_name(db, business_id, dimension_label) is None:

            raise DomainValidationError(

                f"Accounting Dimension '{dimension_label}' does not exist",

                code="accounting_dimension_not_found",

            )



    @staticmethod

    def _validate_accounts(row: AccountingDimensionFilter) -> None:

        """``accounts`` is ``reqd=1`` upstream -- a filter with no scope is a no-op."""

        if not row.accounts:

            raise DomainValidationError(

                "Please select at least one account for the filter",

                code="dimension_filter_accounts_mandatory",

            )



    @staticmethod

    def _validate_values(row: AccountingDimensionFilter) -> None:

        """

        When the restriction is expressed as a value list, the list must be

        non-empty -- an empty allow-list would block everything and an empty

        restrict-list would block nothing, neither of which is intended.

        """

        if row.apply_restriction_on_values and not row.dimensions:

            raise DomainValidationError(

                "Please add at least one dimension value, or turn off "

                "'Apply Restriction On Values'",

                code="dimension_filter_values_mandatory",

            )



    def _validate(

        self, db: Session, business_id: uuid.UUID, row: AccountingDimensionFilter

    ) -> None:

        self._validate_dimension_exists(db, business_id, row.accounting_dimension)

        self._validate_accounts(row)

        self._validate_values(row)



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, filter_id: uuid.UUID

    ) -> AccountingDimensionFilter:

        return self._get_or_404(db, business_id, filter_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[AccountingDimensionFilter]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[AccountingDimensionFilter].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_children(

        self,

        business_id: uuid.UUID,

        row: AccountingDimensionFilter,

        accounts: Optional[list[dict]],

        dimensions: Optional[list[dict]],

    ) -> None:

        if accounts is not None:

            row.accounts.clear()

            for idx, item in enumerate(accounts, start=1):

                row.accounts.append(

                    ApplicableOnAccount(

                        business_id=business_id,

                        idx=idx,

                        account_id=item["account_id"],

                        is_mandatory=bool(item.get("is_mandatory")),

                    )

                )

        if dimensions is not None:

            row.dimensions.clear()

            for idx, item in enumerate(dimensions, start=1):

                row.dimensions.append(

                    AllowedDimension(

                        business_id=business_id,

                        idx=idx,

                        accounting_dimension=item.get("accounting_dimension"),

                        dimension_value=item.get("dimension_value"),

                    )

                )



    def create(

        self,

        db: Session,

        business_id: uuid.UUID,

        payload: AccountingDimensionFilterCreate,

    ) -> AccountingDimensionFilter:

        row = AccountingDimensionFilter(

            business_id=business_id,

            name=self.repository.next_name(db, business_id, payload.accounting_dimension),

            accounting_dimension=payload.accounting_dimension,

            fieldname=payload.fieldname,

            allow_or_restrict=payload.allow_or_restrict,

            apply_restriction_on_values=payload.apply_restriction_on_values,

            disabled=payload.disabled,

        )

        self._replace_children(

            business_id,

            row,

            [a.model_dump() for a in payload.accounts],

            [d.model_dump() for d in payload.dimensions],

        )



        try:

            self.repository.add(db, row)

            self._validate(db, business_id, row)

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

        filter_id: uuid.UUID,

        payload: AccountingDimensionFilterUpdate,

    ) -> AccountingDimensionFilter:

        row = self._get_or_404(db, business_id, filter_id)

        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name in (

                "allow_or_restrict", "fieldname", "apply_restriction_on_values", "disabled"

            ):

                if field_name in changes:

                    setattr(row, field_name, changes[field_name])



            self._replace_children(

                business_id, row, changes.get("accounts"), changes.get("dimensions")

            )

            self._validate(db, business_id, row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def delete(

        self, db: Session, business_id: uuid.UUID, filter_id: uuid.UUID

    ) -> None:

        row = self._get_or_404(db, business_id, filter_id)

        self.repository.delete(db, row)

        db.commit()



    # ── the guard other domains call ─────────────────────────────────────────

    def assert_value_allowed(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        account_id: uuid.UUID,

        dimension_label: str,

        dimension_value: Optional[str],

    ) -> None:

        """

        Enforcement half, ported from ``validate_dimension_filters``.



        For every enabled filter that governs ``account_id`` and targets

        ``dimension_label``:



        * ``Allow``  -- the value must appear in the filter's value list;

        * ``Restrict`` -- the value must NOT appear in it.



        A filter with no value rows only bites when

        ``apply_restriction_on_values`` is on; otherwise it is a flag with

        nothing to compare against and is skipped.

        """

        for rule in self.repository.list_for_account(db, business_id, account_id):

            if rule.accounting_dimension != dimension_label:

                continue



            listed = {d.dimension_value for d in rule.dimensions if d.dimension_value}

            if rule.apply_restriction_on_values and not listed:

                continue



            if rule.allow_or_restrict is AllowOrRestrict.ALLOW:

                if dimension_value not in listed:

                    raise DimensionValueNotAllowedError(

                        f"{dimension_label} '{dimension_value}' is not allowed for this "

                        f"account (filter {rule.name})",

                        dimension=dimension_label,

                        value=dimension_value,

                    )

            elif dimension_value in listed:

                raise DimensionValueNotAllowedError(

                    f"{dimension_label} '{dimension_value}' is restricted for this "

                    f"account (filter {rule.name})",

                    dimension=dimension_label,

                    value=dimension_value,

                )



    def is_mandatory_for_account(

        self, db: Session, business_id: uuid.UUID, account_id: uuid.UUID, dimension_label: str

    ) -> bool:

        """

        Whether a value must be supplied for this dimension on this account.



        Driven by the ``is_mandatory`` flag on the filter's account rows.

        """

        for rule in self.repository.list_for_account(db, business_id, account_id):

            if rule.accounting_dimension != dimension_label:

                continue

            if any(

                row.account_id == account_id and row.is_mandatory for row in rule.accounts

            ):

                return True

        return False
