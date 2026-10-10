# HAND-WRITTEN

"""

Business logic for Loyalty Program -- port of

``erpnext/accounts/doctype/loyalty_program/loyalty_program.py``.







Upstream hooks:

    validate

    validate_lowest_tier



Upstream's ``validate`` holds one rule, ``validate_lowest_tier``, and it is

ported. The other five throws in the file belong to module-level redemption

helpers that Sales Invoice calls, not to saving a program; see :meth:`_validate`.

"""



from __future__ import annotations



import uuid

from decimal import Decimal

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.loyalty_program_domain.models.loyalty_program import LoyaltyProgram

from app.accounts.loyalty_program_collection_domain.models.loyalty_program_collection import LoyaltyProgramCollection

from app.accounts.loyalty_program_domain.repositories.loyalty_program_repository import (

    LoyaltyProgramRepository,

)

from app.accounts.loyalty_program_domain.schemas.loyalty_program import (

    LoyaltyProgramCreate,

    LoyaltyProgramUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["LoyaltyProgramService"]





def _dec(value) -> Decimal:

    """

    Coerce a possibly-None ``min_spent`` to Decimal.



    Upstream would raise comparing None; treating a blank floor as "not zero"

    rejects it with a useful message instead of crashing.

    """

    return Decimal(str(value if value is not None else -1))





class LoyaltyProgramService:

    def __init__(self, repository: Optional[LoyaltyProgramRepository] = None) -> None:

        self.repository = repository or LoyaltyProgramRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> LoyaltyProgram:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Loyalty Program", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    # ══════════════════════════════════════════════════════════════════════

    # ported validators

    # ══════════════════════════════════════════════════════════════════════

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: LoyaltyProgram

    ) -> None:

        """

        Port of upstream ``validate``, which contains exactly one rule:



            validate_lowest_tier  -> ported



        Scope note: the other five ``frappe.throw`` sites in the upstream file

        live in *module-level* helpers -- ``get_loyalty_details``,

        ``validate_loyalty_points`` ("You don't have enough Loyalty Points to

        redeem", "You can't redeem Loyalty Points having more value than the

        Total Amount.") and ``get_loyalty_program_details`` ("The Loyalty

        Program isn't valid for the selected company"). Those are called by the

        Sales Invoice redemption flow, not by saving a program, so they do not

        belong to this doctype's validate. They are not ported here.

        """

        self._validate_lowest_tier(row)



    # ── validate_lowest_tier ──────────────────────────────────────────────

    def _validate_lowest_tier(self, row: LoyaltyProgram) -> None:

        """

        Tiers are matched by ``min_spent``, so a customer who has spent nothing

        must still land in one the moment they enrol. Without a zero-threshold

        floor a new member matches no tier and earns nothing.



        Upstream sorts before comparing, so the check is about the smallest

        value rather than the first row. An empty rule set is skipped, matching

        upstream's ``if tiers and ...`` guard.

        """

        rules = list(row.collection_rules)

        if not rules:

            return



        lowest = min(rules, key=lambda r: _dec(r.min_spent))

        if _dec(lowest.min_spent) != 0:

            raise DomainValidationError(

                "The lowest tier must have a minimum spent amount of 0. "

                "Customers need to be part of a tier as soon as they are "

                "enrolled in the program.",

                code="loyalty_program_lowest_tier_not_zero",

                details={

                    "lowest_tier": lowest.tier_name,

                    "min_spent": str(lowest.min_spent),

                },

            )





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> LoyaltyProgram:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[LoyaltyProgram]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[LoyaltyProgram].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_collection_rules(

        self, business_id: uuid.UUID, row: LoyaltyProgram, items: list[dict]

    ) -> None:

        row.collection_rules.clear()

        for idx, item in enumerate(items, start=1):

            row.collection_rules.append(

                LoyaltyProgramCollection(

                    business_id=business_id,

                    idx=idx,

                    tier_name=item.get('tier_name'),

                    min_spent=item.get('min_spent'),

                    collection_factor=item.get('collection_factor'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(LoyaltyProgram).where(

                    LoyaltyProgram.business_id == business_id

                )

            )

            or 0

        )

        return f"LOY-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: LoyaltyProgramCreate

    ) -> LoyaltyProgram:

        row = LoyaltyProgram(

            business_id=business_id,

            name=self.next_name(db, business_id),

            loyalty_program_name=payload.loyalty_program_name,

            loyalty_program_type=payload.loyalty_program_type,

            from_date=payload.from_date,

            to_date=payload.to_date,

            customer_group=payload.customer_group,

            customer_territory=payload.customer_territory,

            auto_opt_in=payload.auto_opt_in,

            conversion_factor=payload.conversion_factor,

            expiry_duration=payload.expiry_duration,

            expense_account_id=payload.expense_account_id,

            cost_center_id=payload.cost_center_id,

            project=payload.project,

        )

        self._replace_collection_rules(business_id, row, [x.model_dump() for x in payload.collection_rules])



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

        payload: LoyaltyProgramUpdate,

    ) -> LoyaltyProgram:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "collection_rules":

                    self._replace_collection_rules(business_id, row, value or [])

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
