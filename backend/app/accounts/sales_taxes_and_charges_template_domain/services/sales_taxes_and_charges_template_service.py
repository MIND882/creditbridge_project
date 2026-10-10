"""

Business logic for Sales Taxes and Charges Template -- port of

``erpnext/accounts/doctype/sales_taxes_and_charges_template``.



Upstream hook -> here

-------------------

``autoname``                              :meth:`create`

``validate`` -> ``valdiate_taxes_and_charges_template``

  clear other defaults for the company    :meth:`_clear_other_defaults`

  ``validate_disabled``                   :meth:`_validate_disabled`

  ``validate_for_tax_category``           :meth:`_validate_for_tax_category`

  ``validate_taxes_and_charges`` (per row)  shared ``tax_validators``

  ``validate_account_head``  (per row)      shared ``tax_validators``

  ``validate_cost_center``   (per row)      shared ``tax_validators``

  ``validate_inclusive_tax`` (per row)      shared ``tax_validators``

``set_missing_values``                    :meth:`_set_missing_rates`



Upstream's module-level function name is misspelled ``valdiate_...``; the

docstring here keeps the real spelling.

"""



from __future__ import annotations



import uuid

from decimal import Decimal

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.account_domain.models.account import Account

from app.accounts.sales_taxes_and_charges_domain.models.sales_taxes_and_charges import (

    SalesTaxesAndCharges,

)

from app.accounts.sales_taxes_and_charges_template_domain.models.sales_taxes_and_charges_template import (  # noqa: E501

    SalesTaxesAndChargesTemplate,

)

from app.accounts.sales_taxes_and_charges_template_domain.repositories.sales_taxes_and_charges_template_repository import (  # noqa: E501

    SalesTaxesAndChargesTemplateRepository,

)

from app.accounts.sales_taxes_and_charges_template_domain.schemas.sales_taxes_and_charges_template import (  # noqa: E501

    SalesTaxesAndChargesTemplateCreate,

    SalesTaxesAndChargesTemplateUpdate,

)

from app.accounts.tax_enums import ChargeType

from app.accounts.tax_validators import (

    validate_account_head,

    validate_cost_center,

    validate_inclusive_tax,

    validate_taxes_and_charges,

)

from app.core.errors import ConflictError, DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SalesTaxesAndChargesTemplateService"]



CONTEXT = "Taxes and Charges"





class SalesTaxesAndChargesTemplateService:

    def __init__(

        self, repository: Optional[SalesTaxesAndChargesTemplateRepository] = None

    ) -> None:

        self.repository = repository or SalesTaxesAndChargesTemplateRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, template_id: uuid.UUID

    ) -> SalesTaxesAndChargesTemplate:

        row = self.repository.get_by_id(db, business_id, template_id)

        if row is None:

            raise NotFoundError("Sales Taxes and Charges Template", template_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    @staticmethod

    def _validate_disabled(row: SalesTaxesAndChargesTemplate) -> None:

        """Port of ``validate_disabled``."""

        if row.is_default and row.disabled:

            raise DomainValidationError(

                "Disabled template must not be default template",

                code="sales_tax_template_disabled_default",

            )



    def _validate_for_tax_category(

        self, db: Session, business_id: uuid.UUID, row: SalesTaxesAndChargesTemplate

    ) -> None:

        """Port of ``validate_for_tax_category``."""

        if row.tax_category_id is None:

            return

        if self.repository.exists_enabled_for_tax_category(

            db, business_id, row.tax_category_id, except_id=row.id

        ):

            raise DomainValidationError(

                f"A template with tax category {row.tax_category_id} already exists. "

                f"Only one template is allowed with each tax category",

                code="sales_tax_template_category_taken",

            )



    def _set_missing_rates(

        self, db: Session, business_id: uuid.UUID, row: SalesTaxesAndChargesTemplate

    ) -> None:

        """

        Port of ``set_missing_values``.



        An "On Net Total" row with no rate takes the rate stored on its account,

        so a template can be saved before the rate is typed in.

        """

        for tax in row.taxes:

            if tax.charge_type is ChargeType.ON_NET_TOTAL and not tax.rate:

                account = db.get(Account, tax.account_head_id)

                if account is not None and account.tax_rate is not None:

                    tax.rate = Decimal(str(account.tax_rate))



    def _validate_rows(

        self, db: Session, business_id: uuid.UUID, row: SalesTaxesAndChargesTemplate

    ) -> None:

        for tax in row.taxes:

            validate_taxes_and_charges(tax.idx, tax.charge_type, tax.row_id)

            validate_account_head(

                db, business_id, tax.idx, tax.account_head_id, CONTEXT

            )

            validate_cost_center(db, business_id, tax.idx, tax.cost_center_id)

            validate_inclusive_tax(

                idx=tax.idx,

                charge_type=tax.charge_type,

                included_in_print_rate=bool(tax.included_in_print_rate),

                row_id=tax.row_id,

                category=None,          # sales rows have no valuation category

                taxes=row.taxes,

            )



    def _clear_other_defaults(

        self, db: Session, business_id: uuid.UUID, row: SalesTaxesAndChargesTemplate

    ) -> None:

        if not row.is_default:

            return

        self.repository.clear_default(db, business_id, except_id=row.id)



    def _validate(self, db: Session, business_id: uuid.UUID, row: SalesTaxesAndChargesTemplate) -> None:

        # Upstream order inside valdiate_taxes_and_charges_template.

        self._clear_other_defaults(db, business_id, row)

        self._validate_disabled(row)

        self._validate_for_tax_category(db, business_id, row)

        self._validate_rows(db, business_id, row)

        self._set_missing_rates(db, business_id, row)



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, template_id: uuid.UUID

    ) -> SalesTaxesAndChargesTemplate:

        return self._get_or_404(db, business_id, template_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[SalesTaxesAndChargesTemplate]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SalesTaxesAndChargesTemplate].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_taxes(

        self,

        business_id: uuid.UUID,

        row: SalesTaxesAndChargesTemplate,

        taxes: list[dict],

    ) -> None:

        row.taxes.clear()

        for idx, item in enumerate(taxes, start=1):

            row.taxes.append(

                SalesTaxesAndCharges(

                    business_id=business_id,

                    idx=idx,

                    charge_type=item["charge_type"],

                    row_id=item.get("row_id"),

                    account_head_id=item["account_head_id"],

                    cost_center_id=item.get("cost_center_id"),

                    description=item["description"],

                    included_in_print_rate=bool(item.get("included_in_print_rate")),

                    rate=item.get("rate"),

                    tax_amount=item.get("tax_amount"),

                    total=item.get("total"),

                    tax_amount_after_discount_amount=item.get(

                        "tax_amount_after_discount_amount"

                    ),

                    base_tax_amount=item.get("base_tax_amount"),

                    base_total=item.get("base_total"),

                    base_tax_amount_after_discount_amount=item.get(

                        "base_tax_amount_after_discount_amount"

                    ),

                    project=item.get("project"),

                    included_in_paid_amount=bool(item.get("included_in_paid_amount")),

                    dont_recompute_tax=bool(item.get("dont_recompute_tax")),

                    account_currency=item.get("account_currency"),

                    net_amount=item.get("net_amount"),

                    base_net_amount=item.get("base_net_amount"),

                    set_by_item_tax_template=bool(item.get("set_by_item_tax_template")),

                    is_tax_withholding_account=bool(

                        item.get("is_tax_withholding_account")

                    ),

                )

            )



    def create(

        self,

        db: Session,

        business_id: uuid.UUID,

        payload: SalesTaxesAndChargesTemplateCreate,

    ) -> SalesTaxesAndChargesTemplate:

        name = payload.title.strip()

        if not name:

            raise DomainValidationError(

                "Title is mandatory", code="sales_tax_template_title_mandatory"

            )

        if self.repository.get_by_name(db, business_id, name) is not None:

            raise ConflictError(

                f"Sales Taxes and Charges Template '{name}' already exists",

                code="sales_tax_template_duplicate",

            )



        row = SalesTaxesAndChargesTemplate(

            business_id=business_id,

            name=name,

            title=name,

            is_default=bool(payload.is_default),

            disabled=bool(payload.disabled),

            tax_category_id=payload.tax_category_id,

        )

        self._replace_taxes(business_id, row, [t.model_dump() for t in payload.taxes])



        try:

            db.flush()          # children need ids before the row validators

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

        payload: SalesTaxesAndChargesTemplateUpdate,

    ) -> SalesTaxesAndChargesTemplate:

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
