"""

Business logic for Payment Term -- port of

``erpnext/accounts/doctype/payment_term/payment_term.py``.



Upstream's controller body is literally ``pass``: there is no ``validate``,

``before_save`` or ``on_submit`` to port. Everything here is therefore the

structural contract rather than ported rules -- the ``autoname =

field:payment_term_name`` identity, uniqueness per tenant, and the refusal to

rename in place.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.payment_term_domain.models.payment_term import PaymentTerm

from app.accounts.payment_term_domain.repositories.payment_term_repository import (

    PaymentTermRepository,

)

from app.accounts.payment_term_domain.schemas.payment_term import (

    PaymentTermCreate,

    PaymentTermUpdate,

)

from app.core.errors import ConflictError, DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PaymentTermService"]





class PaymentTermService:

    def __init__(self, repository: Optional[PaymentTermRepository] = None) -> None:

        self.repository = repository or PaymentTermRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, term_id: uuid.UUID

    ) -> PaymentTerm:

        row = self.repository.get_by_id(db, business_id, term_id)

        if row is None:

            raise NotFoundError("Payment Term", term_id)

        return row



    def get(self, db: Session, business_id: uuid.UUID, term_id: uuid.UUID) -> PaymentTerm:

        return self._get_or_404(db, business_id, term_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PaymentTerm]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PaymentTerm].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def create(self, db: Session, business_id: uuid.UUID, payload: PaymentTermCreate) -> PaymentTerm:

        """

        ``name`` is ``payment_term_name`` verbatim, per ``autoname =

        field:payment_term_name``, and must be unique within the tenant.

        """

        name = payload.payment_term_name.strip()

        if not name:

            raise DomainValidationError(

                "Payment Term Name is mandatory", code="payment_term_name_mandatory"

            )

        if self.repository.get_by_name(db, business_id, name) is not None:

            raise ConflictError(

                f"Payment Term '{name}' already exists", code="payment_term_duplicate"

            )



        row = PaymentTerm(

            business_id=business_id,

            name=name,

            payment_term_name=name,

            invoice_portion=payload.invoice_portion,

            mode_of_payment=payload.mode_of_payment,

            due_date_based_on=payload.due_date_based_on,

            credit_days=payload.credit_days,

            credit_months=payload.credit_months,

            description=payload.description,

            discount_type=payload.discount_type,

            discount=payload.discount,

            discount_validity_based_on=payload.discount_validity_based_on,

            discount_validity=payload.discount_validity,

        )



        try:

            self.repository.add(db, row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def update(

        self, db: Session, business_id: uuid.UUID, term_id: uuid.UUID, payload: PaymentTermUpdate

    ) -> PaymentTerm:

        row = self._get_or_404(db, business_id, term_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                setattr(row, field_name, value)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def delete(self, db: Session, business_id: uuid.UUID, term_id: uuid.UUID) -> None:

        """

        Refused while any template row points at this term.



        Upstream relies on Frappe's link check; here the FK is ``RESTRICT`` so

        the database would refuse anyway, and turning that into a readable 400

        beats surfacing an IntegrityError.

        """

        from app.accounts.payment_terms_template_detail_domain.models.payment_terms_template_detail import (  # noqa: E501

            PaymentTermsTemplateDetail,

        )

        from sqlalchemy import select



        row = self._get_or_404(db, business_id, term_id)



        in_use = db.scalar(

            select(PaymentTermsTemplateDetail.id).where(

                PaymentTermsTemplateDetail.business_id == business_id,

                PaymentTermsTemplateDetail.payment_term_id == term_id,

            )

        )

        if in_use is not None:

            raise DomainValidationError(

                f"Payment Term {row.name} is used by a Payment Terms Template and "

                f"cannot be deleted",

                code="payment_term_in_use",

            )



        self.repository.delete(db, row)

        db.commit()
