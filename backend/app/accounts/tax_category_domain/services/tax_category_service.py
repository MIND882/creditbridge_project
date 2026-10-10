"""

Business logic for Tax Category -- port of

``erpnext/accounts/doctype/tax_category/tax_category.py``.



Upstream's controller body is empty: there is no ``validate`` to port. What is

enforced here is the structural contract -- ``autoname = field:title`` identity,

uniqueness per tenant, and no renaming in place.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import select

from sqlalchemy.orm import Session



from app.accounts.tax_category_domain.models.tax_category import TaxCategory

from app.accounts.tax_category_domain.repositories.tax_category_repository import (

    TaxCategoryRepository,

)

from app.accounts.tax_category_domain.schemas.tax_category import (

    TaxCategoryCreate,

    TaxCategoryUpdate,

)

from app.core.errors import ConflictError, DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["TaxCategoryService"]





class TaxCategoryService:

    def __init__(self, repository: Optional[TaxCategoryRepository] = None) -> None:

        self.repository = repository or TaxCategoryRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, category_id: uuid.UUID

    ) -> TaxCategory:

        row = self.repository.get_by_id(db, business_id, category_id)

        if row is None:

            raise NotFoundError("Tax Category", category_id)

        return row



    def get(self, db: Session, business_id: uuid.UUID, category_id: uuid.UUID) -> TaxCategory:

        return self._get_or_404(db, business_id, category_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[TaxCategory]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[TaxCategory].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def create(

        self, db: Session, business_id: uuid.UUID, payload: TaxCategoryCreate

    ) -> TaxCategory:

        name = payload.title.strip()

        if not name:

            raise DomainValidationError(

                "Title is mandatory", code="tax_category_title_mandatory"

            )

        if self.repository.get_by_name(db, business_id, name) is not None:

            raise ConflictError(

                f"Tax Category '{name}' already exists", code="tax_category_duplicate"

            )



        row = TaxCategory(

            business_id=business_id,

            name=name,

            title=name,

            disabled=bool(payload.disabled),

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

        self,

        db: Session,

        business_id: uuid.UUID,

        category_id: uuid.UUID,

        payload: TaxCategoryUpdate,

    ) -> TaxCategory:

        row = self._get_or_404(db, business_id, category_id)



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



    def delete(self, db: Session, business_id: uuid.UUID, category_id: uuid.UUID) -> None:

        """

        Refused while any tax template or rule points at this category.



        The FK is ``RESTRICT`` so the database would refuse anyway; this turns

        that into a readable 400 rather than an IntegrityError.

        """

        from app.accounts.sales_taxes_and_charges_template_domain.models.sales_taxes_and_charges_template import (  # noqa: E501

            SalesTaxesAndChargesTemplate,

        )

        from app.accounts.purchase_taxes_and_charges_template_domain.models.purchase_taxes_and_charges_template import (  # noqa: E501

            PurchaseTaxesAndChargesTemplate,

        )

        from app.accounts.tax_rule_domain.models.tax_rule import TaxRule



        row = self._get_or_404(db, business_id, category_id)



        for model, label in (

            (SalesTaxesAndChargesTemplate, "Sales Taxes and Charges Template"),

            (PurchaseTaxesAndChargesTemplate, "Purchase Taxes and Charges Template"),

            (TaxRule, "Tax Rule"),

        ):

            in_use = db.scalar(

                select(model.id).where(

                    model.business_id == business_id,

                    model.tax_category_id == category_id,

                )

            )

            if in_use is not None:

                raise DomainValidationError(

                    f"Tax Category {row.name} is used by a {label} and cannot be deleted",

                    code="tax_category_in_use",

                )



        self.repository.delete(db, row)

        db.commit()
