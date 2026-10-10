"""

Business logic for Dunning Type -- port of

``erpnext/accounts/doctype/dunning_type/dunning_type.py``.



Upstream hook -> here

-------------------

``autoname``                            :meth:`create`

``validate``                            :meth:`_validate`

  ``validate_dunning_letter_text``      :meth:`_validate_dunning_letter_text`

    ``validate_languages``              :meth:`_validate_languages`

    ``validate_is_default_language``    :meth:`_validate_is_default_language`

    ``validate_dunning_letter_text_templates``

                                        not ported (see note below)

  ``validate_income_account``           :meth:`_validate_income_account`

  ``validate_cost_center``              :meth:`_validate_cost_center`

  ``set_default_dunning_type``          :meth:`_set_default_dunning_type`



``validate_dunning_letter_text_templates`` runs Jinja's ``validate_template``

over the body and closing text to reject unsafe expressions. There is no

template engine here -- the text is stored as opaque HTML -- so that guard has

no equivalent and is deliberately not ported.



``autoname`` upstream is ``f"{dunning_type} - {company_abbr}"``; there is no

Company doctype, so ``name`` is the label alone, unique per tenant.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.account_domain.models.account import Account

from app.accounts.cost_center_domain.models.cost_center import CostCenter

from app.accounts.dunning_letter_text_domain.models.dunning_letter_text import DunningLetterText

from app.accounts.dunning_type_domain.models.dunning_type import DunningType

from app.accounts.dunning_type_domain.repositories.dunning_type_repository import (

    DunningTypeRepository,

)

from app.accounts.dunning_type_domain.schemas.dunning_type import (

    DunningTypeCreate,

    DunningTypeUpdate,

)

from app.accounts.enums import RootType

from app.core.errors import ConflictError, DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["DunningTypeService"]





class DunningTypeService:

    def __init__(self, repository: Optional[DunningTypeRepository] = None) -> None:

        self.repository = repository or DunningTypeRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, dunning_type_id: uuid.UUID

    ) -> DunningType:

        row = self.repository.get_by_id(db, business_id, dunning_type_id)

        if row is None:

            raise NotFoundError("Dunning Type", dunning_type_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    @staticmethod

    def _validate_languages(row: DunningType) -> None:

        """Port of ``validate_languages``."""

        languages = [letter.language for letter in row.dunning_letter_text]

        if len(languages) != len(set(languages)):

            raise DomainValidationError(

                "Duplicate languages found on Dunning Letter Text. Keep only one of them.",

                code="dunning_type_duplicate_language",

            )



    @staticmethod

    def _validate_is_default_language(row: DunningType) -> None:

        """Port of ``validate_is_default_language``."""

        defaults = [

            letter.language

            for letter in row.dunning_letter_text

            if letter.is_default_language

        ]

        if len(defaults) > 1:

            quoted = ", ".join(f'"{lang}"' for lang in defaults)

            raise DomainValidationError(

                f"{quoted} languages are marked as default languages. "

                f"Please select only one of them.",

                code="dunning_type_multiple_default_languages",

            )



    def _validate_dunning_letter_text(self, row: DunningType) -> None:

        """Port of ``validate_dunning_letter_text``."""

        self._validate_languages(row)

        self._validate_is_default_language(row)



    def _validate_income_account(

        self, db: Session, business_id: uuid.UUID, row: DunningType

    ) -> None:

        """

        Port of ``validate_income_account``.



        Upstream accumulates every problem into a list and raises once, so a

        caller fixing one issue is immediately shown the next. That shape is

        kept: the messages are joined into one error rather than raised one at

        a time. The company check is folded into the tenant-scoped lookup.

        """

        if row.income_account_id is None:

            return



        account = db.get(Account, row.income_account_id)

        if account is None or account.business_id != business_id:

            raise DomainValidationError(

                f"{row.income_account_id} is not an Account of this company. "

                f"Please select a valid Income Account.",

                code="dunning_type_income_account_not_found",

            )



        msg: list[str] = []

        if account.disabled:

            msg.append(

                f"{account.name} is disabled. Please select a valid Income Account."

            )

        if account.root_type is not RootType.INCOME:

            msg.append(

                f"{account.name} is not an Income Account. "

                f"Please select a valid Income Account."

            )

        if account.is_group:

            msg.append(

                f"{account.name} is a group account. "

                f"Please select a non-group Income Account."

            )



        if msg:

            raise DomainValidationError(

                " ".join(msg), code="dunning_type_invalid_income_account"

            )



    def _validate_cost_center(

        self, db: Session, business_id: uuid.UUID, row: DunningType

    ) -> None:

        """Port of ``validate_cost_center``, same accumulate-then-raise shape."""

        if row.cost_center_id is None:

            return



        cost_center = db.get(CostCenter, row.cost_center_id)

        if cost_center is None or cost_center.business_id != business_id:

            raise DomainValidationError(

                f"{row.cost_center_id} is not a Cost Center of this company. "

                f"Please select a valid Cost Center.",

                code="dunning_type_cost_center_not_found",

            )



        msg: list[str] = []

        if cost_center.disabled:

            msg.append(

                f"{cost_center.name} is disabled. Please select an enabled Cost Center."

            )

        if cost_center.is_group:

            msg.append(

                f"{cost_center.name} is a group Cost Center. "

                f"Please select a non-group Cost Center."

            )



        if msg:

            raise DomainValidationError(

                " ".join(msg), code="dunning_type_invalid_cost_center"

            )



    def _set_default_dunning_type(

        self, db: Session, business_id: uuid.UUID, row: DunningType

    ) -> None:

        """Port of ``set_default_dunning_type``."""

        if not row.is_default:

            return

        self.repository.clear_default(db, business_id, except_id=row.id)



    def _validate(self, db: Session, business_id: uuid.UUID, row: DunningType) -> None:

        # Upstream order.

        self._validate_dunning_letter_text(row)

        self._validate_income_account(db, business_id, row)

        self._validate_cost_center(db, business_id, row)



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, dunning_type_id: uuid.UUID

    ) -> DunningType:

        return self._get_or_404(db, business_id, dunning_type_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[DunningType]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[DunningType].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_letters(

        self, business_id: uuid.UUID, row: DunningType, letters: list[dict]

    ) -> None:

        row.dunning_letter_text.clear()

        for idx, item in enumerate(letters, start=1):

            row.dunning_letter_text.append(

                DunningLetterText(

                    business_id=business_id,

                    idx=idx,

                    language=item.get("language"),

                    is_default_language=bool(item.get("is_default_language")),

                    body_text=item.get("body_text"),

                    closing_text=item.get("closing_text"),

                )

            )



    def create(

        self, db: Session, business_id: uuid.UUID, payload: DunningTypeCreate

    ) -> DunningType:

        name = payload.dunning_type.strip()

        if not name:

            raise DomainValidationError(

                "Dunning Type is mandatory", code="dunning_type_name_mandatory"

            )

        if self.repository.get_by_name(db, business_id, name) is not None:

            raise ConflictError(

                f"Dunning Type '{name}' already exists", code="dunning_type_duplicate"

            )



        row = DunningType(

            business_id=business_id,

            name=name,

            dunning_type=name,

            dunning_fee=payload.dunning_fee,

            rate_of_interest=payload.rate_of_interest,

            is_default=bool(payload.is_default),

            income_account_id=payload.income_account_id,

            cost_center_id=payload.cost_center_id,

        )

        self._replace_letters(

            business_id, row, [letter.model_dump() for letter in payload.dunning_letter_text]

        )



        try:

            db.flush()          # children need ids before the duplicate checks

            self._validate(db, business_id, row)

            self.repository.add(db, row)

            self._set_default_dunning_type(db, business_id, row)

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

        dunning_type_id: uuid.UUID,

        payload: DunningTypeUpdate,

    ) -> DunningType:

        row = self._get_or_404(db, business_id, dunning_type_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "dunning_letter_text":

                    self._replace_letters(business_id, row, value)

                else:

                    setattr(row, field_name, value)

            db.flush()

            self._validate(db, business_id, row)

            self._set_default_dunning_type(db, business_id, row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def delete(self, db: Session, business_id: uuid.UUID, dunning_type_id: uuid.UUID) -> None:

        row = self._get_or_404(db, business_id, dunning_type_id)

        self.repository.delete(db, row)

        db.commit()
