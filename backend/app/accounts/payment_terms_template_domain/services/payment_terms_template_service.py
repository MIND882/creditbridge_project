"""

Business logic for Payment Terms Template -- port of

``erpnext/accounts/doctype/payment_terms_template/payment_terms_template.py``.



Upstream hook -> here

-------------------

``autoname`` (field:template_name)   :meth:`create`

``validate``                          :meth:`_validate`

  ``validate_invoice_portion``        :meth:`_validate_invoice_portion`

  ``validate_terms``                  :meth:`_validate_terms`



Both upstream guards raise via ``frappe.msgprint(..., raise_exception=1)``,

which surfaces as a validation error just like ``frappe.throw`` -- so both

become ``HTTPException(400)`` here.

"""



from __future__ import annotations



import uuid

from decimal import Decimal, ROUND_HALF_UP

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.payment_terms_template_detail_domain.models.payment_terms_template_detail import (

    PaymentTermsTemplateDetail,

)

from app.accounts.payment_terms_template_domain.models.payment_terms_template import (

    PaymentTermsTemplate,

)

from app.accounts.payment_terms_template_domain.repositories.payment_terms_template_repository import (  # noqa: E501

    PaymentTermsTemplateRepository,

)

from app.accounts.payment_terms_template_domain.schemas.payment_terms_template import (

    PaymentTermsTemplateCreate,

    PaymentTermsTemplateUpdate,

)

from app.core.errors import ConflictError, DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PaymentTermsTemplateService"]



HUNDRED = Decimal("100")





def _dec(value: object) -> Decimal:

    if value is None or value == "":

        return Decimal("0")

    return Decimal(str(value))





class PaymentTermsTemplateService:

    def __init__(

        self, repository: Optional[PaymentTermsTemplateRepository] = None

    ) -> None:

        self.repository = repository or PaymentTermsTemplateRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, template_id: uuid.UUID

    ) -> PaymentTermsTemplate:

        row = self.repository.get_by_id(db, business_id, template_id)

        if row is None:

            raise NotFoundError("Payment Terms Template", template_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    @staticmethod

    def _validate_invoice_portion(row: PaymentTermsTemplate) -> None:

        """

        Port of ``validate_invoice_portion``.



        Upstream compares ``flt(total_portion, 2) != 100.00`` -- i.e. rounded to

        two decimals, so 99.999 is accepted and 99.99 is not. Decimal rounding

        reproduces that exactly, where a float comparison would not.

        """

        total = sum((_dec(t.invoice_portion) for t in row.terms), Decimal("0"))

        if total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) != HUNDRED.quantize(

            Decimal("0.01")

        ):

            raise DomainValidationError(

                "Combined invoice portion must equal 100%",

                code="payment_terms_template_portion_not_100",

                details={"total_portion": str(total)},

            )



    @staticmethod

    def _validate_terms(row: PaymentTermsTemplate) -> None:

        """Port of ``validate_terms``."""

        seen: list[tuple] = []

        for term in row.terms:

            # Only bites when the template allocates payments per term.

            if row.allocate_payment_based_on_payment_terms and not term.payment_term_id:

                raise DomainValidationError(

                    f"Row {term.idx}: Payment Term is mandatory",

                    code="payment_terms_template_term_mandatory",

                )



            key = (

                term.payment_term_id,

                term.credit_days,

                term.credit_months,

                term.due_date_based_on,

            )

            if key in seen:

                raise DomainValidationError(

                    f"The Payment Term at row {term.idx} is possibly a duplicate.",

                    code="payment_terms_template_duplicate_term",

                )

            seen.append(key)



    def _validate(self, row: PaymentTermsTemplate) -> None:

        # Upstream order: portion first, then the per-row rules.

        self._validate_invoice_portion(row)

        self._validate_terms(row)



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, template_id: uuid.UUID

    ) -> PaymentTermsTemplate:

        return self._get_or_404(db, business_id, template_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PaymentTermsTemplate]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PaymentTermsTemplate].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_terms(

        self,

        business_id: uuid.UUID,

        row: PaymentTermsTemplate,

        terms: list[dict],

    ) -> None:

        row.terms.clear()

        for idx, item in enumerate(terms, start=1):

            row.terms.append(

                PaymentTermsTemplateDetail(

                    business_id=business_id,

                    idx=idx,

                    payment_term_id=item.get("payment_term_id"),

                    description=item.get("description"),

                    invoice_portion=item["invoice_portion"],

                    due_date_based_on=item["due_date_based_on"],

                    credit_days=item.get("credit_days"),

                    credit_months=item.get("credit_months"),

                    mode_of_payment=item.get("mode_of_payment"),

                    discount_type=item.get("discount_type"),

                    discount=item.get("discount"),

                    discount_validity_based_on=item.get("discount_validity_based_on"),

                    discount_validity=item.get("discount_validity"),

                )

            )



    def create(

        self,

        db: Session,

        business_id: uuid.UUID,

        payload: PaymentTermsTemplateCreate,

    ) -> PaymentTermsTemplate:

        name = payload.template_name.strip()

        if not name:

            raise DomainValidationError(

                "Template Name is mandatory", code="payment_terms_template_name_mandatory"

            )

        if self.repository.get_by_name(db, business_id, name) is not None:

            raise ConflictError(

                f"Payment Terms Template '{name}' already exists",

                code="payment_terms_template_duplicate",

            )



        row = PaymentTermsTemplate(

            business_id=business_id,

            name=name,

            template_name=name,

            allocate_payment_based_on_payment_terms=bool(

                payload.allocate_payment_based_on_payment_terms

            ),

        )

        self._replace_terms(

            business_id, row, [t.model_dump() for t in payload.terms]

        )



        try:

            db.flush()          # children need ids before the duplicate check

            self._validate(row)

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

        payload: PaymentTermsTemplateUpdate,

    ) -> PaymentTermsTemplate:

        row = self._get_or_404(db, business_id, template_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "terms":

                    self._replace_terms(business_id, row, value)

                else:

                    setattr(row, field_name, value)

            db.flush()

            self._validate(row)

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
