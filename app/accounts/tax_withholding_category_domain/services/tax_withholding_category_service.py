"""

Business logic for Tax Withholding Category -- port of

``erpnext/accounts/doctype/tax_withholding_category/tax_withholding_category.py``.



Upstream hook -> here

-------------------

``autoname`` (Prompt)                   :meth:`create`

``validate``                            :meth:`_validate`

  ``validate_dates``                    :meth:`_validate_dates`

  ``validate_companies_and_accounts``   :meth:`_validate_companies_and_accounts`

  ``validate_thresholds``               :meth:`_validate_thresholds`

``validate_account_head`` (accounts/services/taxes.py)

                                        :meth:`_validate_account_head`



One deliberate narrowing: upstream's ``validate_companies_and_accounts`` rejects

a second row naming the same *company*, because one category can span companies.

Here tenancy is ``business_id``, so every row is the same company by

construction -- that check would fire on any second row and make multi-account

categories impossible. The duplicate-*account* half is ported unchanged, and the

company half is subsumed by the tenant scoping every repository query applies.

"""



from __future__ import annotations



import uuid

from collections import defaultdict

from datetime import date

from decimal import Decimal

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.account_domain.models.account import Account

from app.accounts.tax_withholding_account_domain.models.tax_withholding_account import (

    TaxWithholdingAccount,

)

from app.accounts.tax_withholding_category_domain.models.tax_withholding_category import (

    TaxWithholdingCategory,

)

from app.accounts.tax_withholding_category_domain.repositories.tax_withholding_category_repository import (  # noqa: E501

    TaxWithholdingCategoryRepository,

)

from app.accounts.tax_withholding_category_domain.schemas.tax_withholding_category import (

    TaxWithholdingCategoryCreate,

    TaxWithholdingCategoryUpdate,

)

from app.accounts.tax_withholding_rate_domain.models.tax_withholding_rate import (

    TaxWithholdingRate,

)

from app.core.errors import ConflictError, DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["TaxWithholdingCategoryService"]



ZERO = Decimal("0")





def _dec(value: object) -> Decimal:

    if value is None or value == "":

        return ZERO

    return Decimal(str(value))





class TaxWithholdingCategoryService:

    def __init__(

        self, repository: Optional[TaxWithholdingCategoryRepository] = None

    ) -> None:

        self.repository = repository or TaxWithholdingCategoryRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, category_id: uuid.UUID

    ) -> TaxWithholdingCategory:

        row = self.repository.get_by_id(db, business_id, category_id)

        if row is None:

            raise NotFoundError("Tax Withholding Category", category_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    @staticmethod

    def _validate_dates(row: TaxWithholdingCategory) -> None:

        """

        Port of ``validate_dates``.



        Two rules: each window must be ordered, and windows sharing a

        ``tax_withholding_group`` must not overlap. Upstream sorts by

        ``from_date`` and walks the list comparing each start to the previous

        end; reproduced exactly, because an unsorted input would otherwise let

        an overlap through.

        """

        groups: dict[str, list[TaxWithholdingRate]] = defaultdict(list)

        for rate in row.rates:

            if rate.from_date >= rate.to_date:

                raise DomainValidationError(

                    f"Row #{rate.idx}: From Date cannot be before To Date",

                    code="tax_withholding_category_bad_date_range",

                )

            groups[rate.tax_withholding_group or ""].append(rate)



        for group, rates in groups.items():

            rates = sorted(rates, key=lambda r: r.from_date)

            last_to_date: Optional[date] = None

            for rate in rates:

                if last_to_date and rate.from_date < last_to_date:

                    raise DomainValidationError(

                        f"Row #{rate.idx}: Dates overlapping with other row in group "

                        f"{group or 'Default'}",

                        code="tax_withholding_category_overlapping_dates",

                    )

                last_to_date = rate.to_date



    def _validate_account_head(

        self, db: Session, business_id: uuid.UUID, idx: int, account_id: Optional[uuid.UUID]

    ) -> None:

        """

        Port of ``validate_account_head`` from ``accounts/services/taxes.py``.



        Upstream's first check is that the account belongs to the same company;

        tenancy makes that structurally true here, so what remains is the

        group-account rule.

        """

        if account_id is None:

            raise DomainValidationError(

                f"Row {idx}: Account is mandatory",

                code="tax_withholding_category_account_mandatory",

            )



        account = db.get(Account, account_id)

        if account is None or account.business_id != business_id:

            raise DomainValidationError(

                f"Row {idx}: The Account {account_id} does not belong to this company",

                code="tax_withholding_category_account_not_found",

            )

        if account.is_group:

            raise DomainValidationError(

                f"You selected the account group {account.name} as Account in row {idx}. "

                f"Please select a single account.",

                code="tax_withholding_category_account_is_group",

            )



    def _validate_companies_and_accounts(

        self, db: Session, business_id: uuid.UUID, row: TaxWithholdingCategory

    ) -> None:

        """Port of ``validate_companies_and_accounts``, minus the company check."""

        existing_accounts: set[uuid.UUID] = set()

        for account_row in row.accounts:

            account_id = account_row.account_id

            if account_id in existing_accounts:

                raise DomainValidationError(

                    f"Account {account_id} added multiple times",

                    code="tax_withholding_category_duplicate_account",

                )

            self._validate_account_head(

                db, business_id, account_row.idx, account_id

            )

            existing_accounts.add(account_id)



    @staticmethod

    def _validate_thresholds(row: TaxWithholdingCategory) -> None:

        """Port of ``validate_thresholds``."""

        for rate in row.rates:

            cumulative = _dec(rate.cumulative_threshold)

            single = _dec(rate.single_threshold)

            if cumulative and single and cumulative < single:

                raise DomainValidationError(

                    f"Row #{rate.idx}: Cumulative threshold cannot be less than Single "

                    f"Transaction threshold",

                    code="tax_withholding_category_threshold_inverted",

                )



    def _validate(self, db: Session, business_id: uuid.UUID, row: TaxWithholdingCategory) -> None:

        # Upstream order: dates, then accounts, then thresholds.

        self._validate_dates(row)

        self._validate_companies_and_accounts(db, business_id, row)

        self._validate_thresholds(row)



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, category_id: uuid.UUID

    ) -> TaxWithholdingCategory:

        return self._get_or_404(db, business_id, category_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[TaxWithholdingCategory]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[TaxWithholdingCategory].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_rates(

        self, business_id: uuid.UUID, row: TaxWithholdingCategory, rates: list[dict]

    ) -> None:

        row.rates.clear()

        for idx, item in enumerate(rates, start=1):

            row.rates.append(

                TaxWithholdingRate(

                    business_id=business_id,

                    idx=idx,

                    tax_withholding_rate=item["tax_withholding_rate"],

                    single_threshold=item.get("single_threshold"),

                    cumulative_threshold=item.get("cumulative_threshold"),

                    from_date=item["from_date"],

                    to_date=item["to_date"],

                    tax_withholding_group=item.get("tax_withholding_group"),

                )

            )



    def _replace_accounts(

        self, business_id: uuid.UUID, row: TaxWithholdingCategory, accounts: list[dict]

    ) -> None:

        row.accounts.clear()

        for idx, item in enumerate(accounts, start=1):

            row.accounts.append(

                TaxWithholdingAccount(

                    business_id=business_id,

                    idx=idx,

                    account_id=item["account_id"],

                )

            )



    def create(

        self,

        db: Session,

        business_id: uuid.UUID,

        payload: TaxWithholdingCategoryCreate,

    ) -> TaxWithholdingCategory:

        name = payload.category_name.strip()

        if not name:

            raise DomainValidationError(

                "Category Name is mandatory",

                code="tax_withholding_category_name_mandatory",

            )

        if self.repository.get_by_name(db, business_id, name) is not None:

            raise ConflictError(

                f"Tax Withholding Category '{name}' already exists",

                code="tax_withholding_category_duplicate",

            )



        row = TaxWithholdingCategory(

            business_id=business_id,

            name=name,

            category_name=name,

            tax_on_excess_amount=bool(payload.tax_on_excess_amount),

            round_off_tax_amount=bool(payload.round_off_tax_amount),

            tax_deduction_basis=payload.tax_deduction_basis,

            disable_cumulative_threshold=bool(payload.disable_cumulative_threshold),

            disable_transaction_threshold=bool(payload.disable_transaction_threshold),

        )

        self._replace_rates(business_id, row, [r.model_dump() for r in payload.rates])

        self._replace_accounts(business_id, row, [a.model_dump() for a in payload.accounts])



        try:

            db.flush()          # children need ids before validation reads them

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

        category_id: uuid.UUID,

        payload: TaxWithholdingCategoryUpdate,

    ) -> TaxWithholdingCategory:

        row = self._get_or_404(db, business_id, category_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "rates":

                    self._replace_rates(business_id, row, value)

                elif field_name == "accounts":

                    self._replace_accounts(business_id, row, value)

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



    def delete(self, db: Session, business_id: uuid.UUID, category_id: uuid.UUID) -> None:

        row = self._get_or_404(db, business_id, category_id)

        self.repository.delete(db, row)

        db.commit()
