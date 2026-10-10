"""Business logic for Supplier -- port of

``erpnext/buying/doctype/supplier/supplier.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.buying.supplier_domain.models.supplier import Supplier

from app.buying.supplier_domain.repositories.supplier_repository import (

    SupplierRepository,

)

from app.buying.supplier_domain.schemas.supplier import (

    SupplierCreate,

    SupplierUpdate,

)

from app.buying.customer_number_at_supplier_domain.models.customer_number_at_supplier import CustomerNumberAtSupplier

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SupplierService"]





class SupplierService:

    def __init__(self, repository: Optional[SupplierRepository] = None) -> None:

        self.repository = repository or SupplierRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Supplier:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Supplier", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: Supplier

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Supplier:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[Supplier]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[Supplier].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID, series: Optional[str] = None) -> str:

        """A per-tenant sequential name; upstream mints one from ``naming_series``."""

        # ``naming_series`` is optional on input (Frappe fills it from a

        # default), so fall back to the doctype prefix when it is absent.

        series = series or ""

        prefix = series.split(".")[0].split("#")[0]

        if prefix and not prefix.endswith("-"):

            prefix += "-"

        count = int(

            db.scalar(

                select(func.count()).select_from(Supplier).where(

                    Supplier.business_id == business_id

                )

            )

            or 0

        )

        return f"{prefix}{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: SupplierCreate

    ) -> Supplier:

        row = Supplier(

            business_id=business_id,

            name=self.next_name(db, business_id, payload.naming_series),

            naming_series=payload.naming_series,

            supplier_name=payload.supplier_name,

            country=payload.country,

            default_bank_account_id=payload.default_bank_account_id,

            tax_id=payload.tax_id,

            tax_category_id=payload.tax_category_id,

            tax_withholding_category_id=payload.tax_withholding_category_id,

            is_transporter=payload.is_transporter,

            is_internal_supplier=payload.is_internal_supplier,

            represents_company=payload.represents_company,

            image=payload.image,

            supplier_group=payload.supplier_group,

            supplier_type=payload.supplier_type,

            language=payload.language,

            disabled=payload.disabled,

            warn_rfqs=payload.warn_rfqs,

            warn_pos=payload.warn_pos,

            prevent_rfqs=payload.prevent_rfqs,

            prevent_pos=payload.prevent_pos,

            default_currency=payload.default_currency,

            default_price_list_id=payload.default_price_list_id,

            payment_terms_id=payload.payment_terms_id,

            on_hold=payload.on_hold,

            hold_type=payload.hold_type,

            release_date=payload.release_date,

            website=payload.website,

            supplier_details=payload.supplier_details,

            is_frozen=payload.is_frozen,

            allow_purchase_invoice_creation_without_purchase_order=payload.allow_purchase_invoice_creation_without_purchase_order,

            allow_purchase_invoice_creation_without_purchase_receipt=payload.allow_purchase_invoice_creation_without_purchase_receipt,

            supplier_primary_contact=payload.supplier_primary_contact,

            mobile_no=payload.mobile_no,

            email_id=payload.email_id,

            primary_address=payload.primary_address,

            supplier_primary_address=payload.supplier_primary_address,

            restrict_to_companies=payload.restrict_to_companies,

            tax_withholding_group_id=payload.tax_withholding_group_id,

            gender=payload.gender,

            alias=payload.alias,

        )

        self._replace_customer_numbers(business_id, row, [x.model_dump() for x in payload.customer_numbers])



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

        payload: SupplierUpdate,

    ) -> Supplier:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "customer_numbers":

                    self._replace_customer_numbers(business_id, row, value or [])

                    continue

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



    def _replace_customer_numbers(

        self, business_id: uuid.UUID, row: Supplier, customer_numbers: list[dict]

    ) -> None:

        row.customer_numbers.clear()

        for idx, entry in enumerate(customer_numbers, start=1):

            row.customer_numbers.append(

                CustomerNumberAtSupplier(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Supplier",

                    parentfield="customer_numbers",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )
