"""Business logic for Customer -- port of

``erpnext/selling/doctype/customer/customer.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.selling.customer_domain.models.customer import Customer

from app.selling.customer_domain.repositories.customer_repository import (

    CustomerRepository,

)

from app.selling.customer_domain.schemas.customer import (

    CustomerCreate,

    CustomerUpdate,

)

from app.selling.customer_credit_limit_domain.models.customer_credit_limit import CustomerCreditLimit

from app.selling.sales_team_domain.models.sales_team import SalesTeam

from app.selling.supplier_number_at_customer_domain.models.supplier_number_at_customer import SupplierNumberAtCustomer

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["CustomerService"]





class CustomerService:

    def __init__(self, repository: Optional[CustomerRepository] = None) -> None:

        self.repository = repository or CustomerRepository()





    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Customer:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Customer", row_id)

        return row





    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: Customer

    ) -> None:

        """

        Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

        """

        return None





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Customer:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[Customer]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[Customer].build(

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

                select(func.count()).select_from(Customer).where(

                    Customer.business_id == business_id

                )

            )

            or 0

        )

        return f"{prefix}{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: CustomerCreate

    ) -> Customer:

        row = Customer(

            business_id=business_id,

            name=self.next_name(db, business_id, payload.naming_series),

            naming_series=payload.naming_series,

            customer_name=payload.customer_name,

            alias=payload.alias,

            customer_type=payload.customer_type,

            gender=payload.gender,

            customer_group=payload.customer_group,

            territory=payload.territory,

            image=payload.image,

            default_currency=payload.default_currency,

            default_bank_account_id=payload.default_bank_account_id,

            default_price_list_id=payload.default_price_list_id,

            payment_terms_id=payload.payment_terms_id,

            loyalty_program_id=payload.loyalty_program_id,

            loyalty_program_tier=payload.loyalty_program_tier,

            customer_primary_address=payload.customer_primary_address,

            primary_address=payload.primary_address,

            customer_primary_contact=payload.customer_primary_contact,

            mobile_no=payload.mobile_no,

            email_id=payload.email_id,

            first_name=payload.first_name,

            last_name=payload.last_name,

            is_internal_customer=payload.is_internal_customer,

            represents_company=payload.represents_company,

            tax_id=payload.tax_id,

            tax_category_id=payload.tax_category_id,

            tax_withholding_group_id=payload.tax_withholding_group_id,

            tax_withholding_category_id=payload.tax_withholding_category_id,

            restrict_to_companies=payload.restrict_to_companies,

            so_required=payload.so_required,

            dn_required=payload.dn_required,

            disabled=payload.disabled,

            is_frozen=payload.is_frozen,

            account_manager=payload.account_manager,

            default_sales_partner=payload.default_sales_partner,

            default_commission_rate=payload.default_commission_rate,

            lead_name=payload.lead_name,

            opportunity_name=payload.opportunity_name,

            prospect_name=payload.prospect_name,

            market_segment=payload.market_segment,

            industry_id=payload.industry_id,

            website=payload.website,

            language=payload.language,

            customer_pos_id=payload.customer_pos_id,

            customer_details=payload.customer_details,

        )

        self._replace_credit_limits(business_id, row, [x.model_dump() for x in payload.credit_limits])

        self._replace_sales_team(business_id, row, [x.model_dump() for x in payload.sales_team])

        self._replace_supplier_numbers(business_id, row, [x.model_dump() for x in payload.supplier_numbers])



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

        payload: CustomerUpdate,

    ) -> Customer:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "credit_limits":

                    self._replace_credit_limits(business_id, row, value or [])

                    continue

                if field_name == "sales_team":

                    self._replace_sales_team(business_id, row, value or [])

                    continue

                if field_name == "supplier_numbers":

                    self._replace_supplier_numbers(business_id, row, value or [])

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



    def _replace_credit_limits(

        self, business_id: uuid.UUID, row: Customer, credit_limits: list[dict]

    ) -> None:

        row.credit_limits.clear()

        for idx, entry in enumerate(credit_limits, start=1):

            row.credit_limits.append(

                CustomerCreditLimit(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Customer",

                    parentfield="credit_limits",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_sales_team(

        self, business_id: uuid.UUID, row: Customer, sales_team: list[dict]

    ) -> None:

        row.sales_team.clear()

        for idx, entry in enumerate(sales_team, start=1):

            row.sales_team.append(

                SalesTeam(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Customer",

                    parentfield="sales_team",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )



    def _replace_supplier_numbers(

        self, business_id: uuid.UUID, row: Customer, supplier_numbers: list[dict]

    ) -> None:

        row.supplier_numbers.clear()

        for idx, entry in enumerate(supplier_numbers, start=1):

            row.supplier_numbers.append(

                SupplierNumberAtCustomer(

                    business_id=business_id,

                    idx=idx,

                    parenttype="Customer",

                    parentfield="supplier_numbers",

                    **{k: v for k, v in entry.items() if v is not None},

                )

            )
