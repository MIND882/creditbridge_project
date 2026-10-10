"""

Business logic for Tax Rule -- port of

``erpnext/accounts/doctype/tax_rule/tax_rule.py``.



Upstream hook -> here

-------------------

``autoname`` (ACC-TAX-RULE-.YYYY.-.#####)  :meth:`TaxRuleRepository.next_name`

``validate``                               :meth:`_validate`

  ``validate_tax_template``                :meth:`_validate_tax_template`

  ``validate_from_to_dates``               :meth:`_validate_from_to_dates`

  ``validate_filters``                     :meth:`_validate_filters`



``validate_tax_template`` does two things, and the second is easy to miss: it

*clears* the half of the rule that does not apply. A Sales rule cannot carry a

supplier, and a Purchase rule cannot carry a customer. That is not cosmetic --

the conflict check in ``validate_filters`` compares every filter column, so a

stale supplier on a Sales rule would make two rules look different when they are

really the same.

"""



from __future__ import annotations



import uuid

from datetime import date

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.tax_enums import TaxRuleType

from app.accounts.tax_rule_domain.models.tax_rule import TaxRule

from app.accounts.tax_rule_domain.repositories.tax_rule_repository import TaxRuleRepository

from app.accounts.tax_rule_domain.schemas.tax_rule import TaxRuleCreate, TaxRuleUpdate

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["TaxRuleService"]





class TaxRuleService:

    def __init__(self, repository: Optional[TaxRuleRepository] = None) -> None:

        self.repository = repository or TaxRuleRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, rule_id: uuid.UUID

    ) -> TaxRule:

        row = self.repository.get_by_id(db, business_id, rule_id)

        if row is None:

            raise NotFoundError("Tax Rule", rule_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    @staticmethod

    def _validate_tax_template(row: TaxRule) -> None:

        """

        Port of ``validate_tax_template``.



        Blanks the inapplicable side, then requires that at least one template

        survives. Upstream also clears the matching *group* when a specific

        party is named, because the group is then redundant.

        """

        if row.tax_type is TaxRuleType.SALES:

            row.purchase_tax_template_id = None

            row.supplier = None

            row.supplier_group = None

            if row.customer:

                row.customer_group = None

        else:

            row.sales_tax_template_id = None

            row.customer = None

            row.customer_group = None

            if row.supplier:

                row.supplier_group = None



        if not (row.sales_tax_template_id or row.purchase_tax_template_id):

            raise DomainValidationError(

                "Tax Template is mandatory.", code="tax_rule_template_mandatory"

            )



    @staticmethod

    def _validate_from_to_dates(row: TaxRule) -> None:

        """Port of the base controller's ``validate_from_to_dates``."""

        if row.from_date and row.to_date and row.from_date > row.to_date:

            raise DomainValidationError(

                "From Date cannot be after To Date", code="tax_rule_bad_date_range"

            )



    def _validate_filters(self, db: Session, business_id: uuid.UUID, row: TaxRule) -> None:

        """

        Port of ``validate_filters``.



        Upstream raises ``ConflictingTaxRule`` only when the matching rule has

        the *same* priority; a different priority is a legitimate tie-break, so

        it is allowed.

        """

        conflict = self.repository.find_conflict(db, business_id, row)

        if conflict is not None and conflict.priority == row.priority:

            raise DomainValidationError(

                f"Tax Rule Conflicts with {conflict.name}", code="tax_rule_conflict"

            )



    def _validate(self, db: Session, business_id: uuid.UUID, row: TaxRule) -> None:

        # Upstream order.

        self._validate_tax_template(row)

        self._validate_from_to_dates(row)

        self._validate_filters(db, business_id, row)



    # ── public API ───────────────────────────────────────────────────────────

    def get(self, db: Session, business_id: uuid.UUID, rule_id: uuid.UUID) -> TaxRule:

        return self._get_or_404(db, business_id, rule_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[TaxRule]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[TaxRule].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    @staticmethod

    def _apply(row: TaxRule, payload: object, *, skip: tuple[str, ...] = ()) -> None:

        for field_name, value in payload.model_dump(exclude_unset=True).items():  # type: ignore[attr-defined]

            if field_name in skip:

                continue

            setattr(row, field_name, value)



    def create(self, db: Session, business_id: uuid.UUID, payload: TaxRuleCreate) -> TaxRule:

        naming_date: date = payload.from_date or date.today()

        row = TaxRule(

            business_id=business_id,

            name=self.repository.next_name(db, business_id, naming_date),

        )

        self._apply(row, payload)



        try:

            self._validate(db, business_id, row)

            self.repository.add(db, row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def update(

        self, db: Session, business_id: uuid.UUID, rule_id: uuid.UUID, payload: TaxRuleUpdate

    ) -> TaxRule:

        row = self._get_or_404(db, business_id, rule_id)



        if not payload.model_dump(exclude_unset=True):

            return row



        try:

            # tax_type drives which half of the rule is meaningful and is

            # excluded from the update schema, so it is skipped defensively too.

            self._apply(row, payload, skip=("tax_type",))

            self._validate(db, business_id, row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def delete(self, db: Session, business_id: uuid.UUID, rule_id: uuid.UUID) -> None:

        row = self._get_or_404(db, business_id, rule_id)

        self.repository.delete(db, row)

        db.commit()
