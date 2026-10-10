"""

Business logic for Item Tax Template -- port of

``erpnext/accounts/doctype/item_tax_template/item_tax_template.py``.



Upstream hook -> here

-------------------

``autoname``                             :meth:`create`

``validate``                             :meth:`_validate`

  ``set_zero_rate_for_not_applicable_tax`` :meth:`_set_zero_rate_for_not_applicable_tax`

  ``validate_tax_accounts``              :meth:`_validate_tax_accounts`



``autoname`` upstream is ``f"{title} - {company_abbr}"``; with no Company doctype

here, ``name`` is the title alone, unique per tenant.

"""



from __future__ import annotations



import uuid

from decimal import Decimal

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.account_domain.models.account import Account

from app.accounts.enums import AccountType

from app.accounts.item_tax_template_detail_domain.models.item_tax_template_detail import (

    ItemTaxTemplateDetail,

)

from app.accounts.item_tax_template_domain.models.item_tax_template import ItemTaxTemplate

from app.accounts.item_tax_template_domain.repositories.item_tax_template_repository import (

    ItemTaxTemplateRepository,

)

from app.accounts.item_tax_template_domain.schemas.item_tax_template import (

    ItemTaxTemplateCreate,

    ItemTaxTemplateUpdate,

)

from app.core.errors import ConflictError, DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ItemTaxTemplateService"]



#: Port of the list literal in ``validate_tax_accounts``. Only these account

#: types may carry an item tax.

ALLOWED_TAX_ACCOUNT_TYPES = {

    AccountType.TAX,

    AccountType.CHARGEABLE,

    AccountType.INCOME_ACCOUNT,

    AccountType.EXPENSE_ACCOUNT,

    AccountType.EXPENSES_INCLUDED_IN_VALUATION,

}





class ItemTaxTemplateService:

    def __init__(self, repository: Optional[ItemTaxTemplateRepository] = None) -> None:

        self.repository = repository or ItemTaxTemplateRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, template_id: uuid.UUID

    ) -> ItemTaxTemplate:

        row = self.repository.get_by_id(db, business_id, template_id)

        if row is None:

            raise NotFoundError("Item Tax Template", template_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    @staticmethod

    def _set_zero_rate_for_not_applicable_tax(row: ItemTaxTemplate) -> None:

        """

        Port of ``set_zero_rate_for_not_applicable_tax``.



        An exempt tax keeps its row -- the exemption stays visible -- but its

        rate is forced to zero so nothing is charged by accident.

        """

        for tax in row.taxes:

            if tax.not_applicable:

                tax.tax_rate = Decimal("0")



    def _validate_tax_accounts(

        self, db: Session, business_id: uuid.UUID, row: ItemTaxTemplate

    ) -> None:

        """

        Port of ``validate_tax_accounts``.



        Upstream checks the account's company, then its type, then that the same

        account is not listed twice. The company check is structural here

        (tenant scoping), so what remains is type and duplicates.

        """

        seen: list[uuid.UUID] = []

        for tax in row.taxes:

            if tax.tax_type_id is None:

                continue



            account = db.get(Account, tax.tax_type_id)

            if account is None or account.business_id != business_id:

                raise DomainValidationError(

                    f"Item Tax Row {tax.idx}: Account must belong to this company",

                    code="item_tax_template_account_not_found",

                )



            if account.account_type not in ALLOWED_TAX_ACCOUNT_TYPES:

                raise DomainValidationError(

                    f"Item Tax Row {tax.idx} must have account of type Tax or Income "

                    f"or Expense or Chargeable",

                    code="item_tax_template_wrong_account_type",

                )



            if tax.tax_type_id in seen:

                raise DomainValidationError(

                    f"{account.name} entered twice in Item Tax",

                    code="item_tax_template_duplicate_account",

                )

            seen.append(tax.tax_type_id)



    def _validate(self, db: Session, business_id: uuid.UUID, row: ItemTaxTemplate) -> None:

        # Upstream order: zero the exempt rates first, then validate.

        self._set_zero_rate_for_not_applicable_tax(row)

        self._validate_tax_accounts(db, business_id, row)



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, template_id: uuid.UUID

    ) -> ItemTaxTemplate:

        return self._get_or_404(db, business_id, template_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ItemTaxTemplate]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ItemTaxTemplate].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_taxes(

        self, business_id: uuid.UUID, row: ItemTaxTemplate, taxes: list[dict]

    ) -> None:

        row.taxes.clear()

        for idx, item in enumerate(taxes, start=1):

            row.taxes.append(

                ItemTaxTemplateDetail(

                    business_id=business_id,

                    idx=idx,

                    tax_type_id=item["tax_type_id"],

                    tax_rate=item.get("tax_rate"),

                    not_applicable=bool(item.get("not_applicable")),

                )

            )



    def create(

        self, db: Session, business_id: uuid.UUID, payload: ItemTaxTemplateCreate

    ) -> ItemTaxTemplate:

        name = payload.title.strip()

        if not name:

            raise DomainValidationError(

                "Title is mandatory", code="item_tax_template_title_mandatory"

            )

        if self.repository.get_by_name(db, business_id, name) is not None:

            raise ConflictError(

                f"Item Tax Template '{name}' already exists",

                code="item_tax_template_duplicate",

            )



        row = ItemTaxTemplate(

            business_id=business_id,

            name=name,

            title=name,

            disabled=bool(payload.disabled),

        )

        self._replace_taxes(business_id, row, [t.model_dump() for t in payload.taxes])



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

        template_id: uuid.UUID,

        payload: ItemTaxTemplateUpdate,

    ) -> ItemTaxTemplate:

        row = self._get_or_404(db, business_id, template_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "taxes":

                    self._replace_taxes(business_id, row, value)

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



    def delete(self, db: Session, business_id: uuid.UUID, template_id: uuid.UUID) -> None:

        row = self._get_or_404(db, business_id, template_id)

        self.repository.delete(db, row)

        db.commit()
