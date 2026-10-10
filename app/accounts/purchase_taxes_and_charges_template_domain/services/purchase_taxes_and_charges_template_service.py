"""

Business logic for Purchase Taxes and Charges Template -- port of

``erpnext/accounts/doctype/purchase_taxes_and_charges_template``.



Upstream's ``validate`` is a one-liner delegating to the same

``valdiate_taxes_and_charges_template`` the sales template uses, so the two

share :mod:`app.accounts.tax_validators`. Two differences are kept:



* the purchase row passes its own ``category`` to ``validate_inclusive_tax``,

  because "Valuation" charges cannot be marked inclusive;

* there is no ``set_missing_values`` -- that rate-backfill exists only on the

  sales controller.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.purchase_taxes_and_charges_domain.models.purchase_taxes_and_charges import (

    PurchaseTaxesAndCharges,

)

from app.accounts.purchase_taxes_and_charges_template_domain.models.purchase_taxes_and_charges_template import (  # noqa: E501

    PurchaseTaxesAndChargesTemplate,

)

from app.accounts.purchase_taxes_and_charges_template_domain.repositories.purchase_taxes_and_charges_template_repository import (  # noqa: E501

    PurchaseTaxesAndChargesTemplateRepository,

)

from app.accounts.purchase_taxes_and_charges_template_domain.schemas.purchase_taxes_and_charges_template import (  # noqa: E501

    PurchaseTaxesAndChargesTemplateCreate,

    PurchaseTaxesAndChargesTemplateUpdate,

)

from app.accounts.tax_validators import (

    validate_account_head,

    validate_cost_center,

    validate_inclusive_tax,

    validate_taxes_and_charges,

)

from app.core.errors import ConflictError, DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PurchaseTaxesAndChargesTemplateService"]



CONTEXT = "Taxes and Charges"





class PurchaseTaxesAndChargesTemplateService:

    def __init__(

        self, repository: Optional[PurchaseTaxesAndChargesTemplateRepository] = None

    ) -> None:

        self.repository = repository or PurchaseTaxesAndChargesTemplateRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, template_id: uuid.UUID

    ) -> PurchaseTaxesAndChargesTemplate:

        row = self.repository.get_by_id(db, business_id, template_id)

        if row is None:

            raise NotFoundError("Purchase Taxes and Charges Template", template_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    @staticmethod

    def _validate_disabled(row: PurchaseTaxesAndChargesTemplate) -> None:

        """Port of ``validate_disabled``."""

        if row.is_default and row.disabled:

            raise DomainValidationError(

                "Disabled template must not be default template",

                code="purchase_tax_template_disabled_default",

            )



    def _validate_for_tax_category(

        self, db: Session, business_id: uuid.UUID, row: PurchaseTaxesAndChargesTemplate

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

                code="purchase_tax_template_category_taken",

            )



    def _validate_rows(

        self, db: Session, business_id: uuid.UUID, row: PurchaseTaxesAndChargesTemplate

    ) -> None:

        for tax in row.taxes:

            validate_taxes_and_charges(tax.idx, tax.charge_type, tax.row_id)

            validate_account_head(db, business_id, tax.idx, tax.account_head_id, CONTEXT)

            validate_cost_center(db, business_id, tax.idx, tax.cost_center_id)

            validate_inclusive_tax(

                idx=tax.idx,

                charge_type=tax.charge_type,

                included_in_print_rate=bool(tax.included_in_print_rate),

                row_id=tax.row_id,

                # Purchase-only: a Valuation charge cannot be marked inclusive.

                category=tax.category.value if tax.category else None,

                taxes=row.taxes,

            )



    def _clear_other_defaults(

        self, db: Session, business_id: uuid.UUID, row: PurchaseTaxesAndChargesTemplate

    ) -> None:

        if not row.is_default:

            return

        self.repository.clear_default(db, business_id, except_id=row.id)



    def _validate(

        self, db: Session, business_id: uuid.UUID, row: PurchaseTaxesAndChargesTemplate

    ) -> None:

        self._clear_other_defaults(db, business_id, row)

        self._validate_disabled(row)

        self._validate_for_tax_category(db, business_id, row)

        self._validate_rows(db, business_id, row)



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, template_id: uuid.UUID

    ) -> PurchaseTaxesAndChargesTemplate:

        return self._get_or_404(db, business_id, template_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PurchaseTaxesAndChargesTemplate]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PurchaseTaxesAndChargesTemplate].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_taxes(

        self,

        business_id: uuid.UUID,

        row: PurchaseTaxesAndChargesTemplate,

        taxes: list[dict],

    ) -> None:

        row.taxes.clear()

        for idx, item in enumerate(taxes, start=1):

            row.taxes.append(

                PurchaseTaxesAndCharges(

                    business_id=business_id,

                    idx=idx,

                    category=item.get("category"),

                    add_deduct_tax=item.get("add_deduct_tax"),

                    charge_type=item.get("charge_type"),

                    row_id=item.get("row_id"),

                    allocate_full_amount_to_stock_items=bool(

                        item.get("allocate_full_amount_to_stock_items")

                    ),

                    included_in_print_rate=bool(item.get("included_in_print_rate")),

                    account_head_id=item["account_head_id"],

                    cost_center_id=item.get("cost_center_id"),

                    description=item["description"],

                    rate=item.get("rate"),

                    tax_amount=item.get("tax_amount"),

                    tax_amount_after_discount_amount=item.get(

                        "tax_amount_after_discount_amount"

                    ),

                    total=item.get("total"),

                    base_tax_amount=item.get("base_tax_amount"),

                    base_total=item.get("base_total"),

                    base_tax_amount_after_discount_amount=item.get(

                        "base_tax_amount_after_discount_amount"

                    ),

                    project=item.get("project"),

                    included_in_paid_amount=bool(item.get("included_in_paid_amount")),

                    account_currency=item.get("account_currency"),

                    net_amount=item.get("net_amount"),

                    base_net_amount=item.get("base_net_amount"),

                    is_tax_withholding_account=bool(

                        item.get("is_tax_withholding_account")

                    ),

                    set_by_item_tax_template=bool(item.get("set_by_item_tax_template")),

                    dont_recompute_tax=bool(item.get("dont_recompute_tax")),

                )

            )



    def create(

        self,

        db: Session,

        business_id: uuid.UUID,

        payload: PurchaseTaxesAndChargesTemplateCreate,

    ) -> PurchaseTaxesAndChargesTemplate:

        name = payload.title.strip()

        if not name:

            raise DomainValidationError(

                "Title is mandatory", code="purchase_tax_template_title_mandatory"

            )

        if self.repository.get_by_name(db, business_id, name) is not None:

            raise ConflictError(

                f"Purchase Taxes and Charges Template '{name}' already exists",

                code="purchase_tax_template_duplicate",

            )



        row = PurchaseTaxesAndChargesTemplate(

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

        payload: PurchaseTaxesAndChargesTemplateUpdate,

    ) -> PurchaseTaxesAndChargesTemplate:

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
