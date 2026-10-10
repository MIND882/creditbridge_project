# HAND-WRITTEN

"""

Business logic for POS Profile -- port of

``erpnext/accounts/doctype/pos_profile/pos_profile.py``.







Upstream hooks:

    validate

    validate_accounting_dimensions

    validate_disabled

    validate_default_profile

    validate_all_link_fields

    validate_duplicate_groups

    validate_payment_methods

    on_update

    on_trash

    set_defaults



**Upstream has 9 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.pos_profile_domain.models.pos_profile import POSProfile

from app.accounts.pos_profile_user_domain.models.pos_profile_user import POSProfileUser

from app.accounts.cashier_closing_payments_domain.models.cashier_closing_payments import CashierClosingPayments

from app.accounts.pos_item_group_domain.models.pos_item_group import POSItemGroup

from app.accounts.pos_customer_group_domain.models.pos_customer_group import POSCustomerGroup

from app.accounts.pos_profile_domain.repositories.pos_profile_repository import (

    POSProfileRepository,

)

from app.accounts.pos_profile_domain.schemas.pos_profile import (

    POSProfileCreate,

    POSProfileUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["POSProfileService"]





class POSProfileService:

    def __init__(self, repository: Optional[POSProfileRepository] = None) -> None:

        self.repository = repository or POSProfileRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> POSProfile:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("POS Profile", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: POSProfile

    ) -> None:

        """

        TODO(PORT-VALIDATION): upstream validation is NOT ported.



        This controller has **9 ``frappe.throw`` site(s)** upstream.

        None are enforced here, so writes upstream would reject

        currently succeed. It fails open deliberately rather than

        blocking the CRUD surface, but must not be read as complete.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> POSProfile:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[POSProfile]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[POSProfile].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def _replace_applicable_for_users(

        self, business_id: uuid.UUID, row: POSProfile, items: list[dict]

    ) -> None:

        row.applicable_for_users.clear()

        for idx, item in enumerate(items, start=1):

            row.applicable_for_users.append(

                POSProfileUser(

                    business_id=business_id,

                    idx=idx,

                    default=item.get('default'),

                    user=item.get('user'),

                )

            )



    def _replace_payments(

        self, business_id: uuid.UUID, row: POSProfile, items: list[dict]

    ) -> None:

        row.payments.clear()

        for idx, item in enumerate(items, start=1):

            row.payments.append(

                POSPaymentMethod(

                    business_id=business_id,

                    idx=idx,

                    default=item.get('default'),

                    mode_of_payment_id=item.get('mode_of_payment_id'),

                    allow_in_returns=item.get('allow_in_returns'),

                )

            )



    def _replace_item_groups(

        self, business_id: uuid.UUID, row: POSProfile, items: list[dict]

    ) -> None:

        row.item_groups.clear()

        for idx, item in enumerate(items, start=1):

            row.item_groups.append(

                POSItemGroup(

                    business_id=business_id,

                    idx=idx,

                    item_group=item.get('item_group'),

                )

            )



    def _replace_customer_groups(

        self, business_id: uuid.UUID, row: POSProfile, items: list[dict]

    ) -> None:

        row.customer_groups.clear()

        for idx, item in enumerate(items, start=1):

            row.customer_groups.append(

                POSCustomerGroup(

                    business_id=business_id,

                    idx=idx,

                    customer_group=item.get('customer_group'),

                )

            )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(POSProfile).where(

                    POSProfile.business_id == business_id

                )

            )

            or 0

        )

        return f"POS-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: POSProfileCreate

    ) -> POSProfile:

        row = POSProfile(

            business_id=business_id,

            name=self.next_name(db, business_id),

            disabled=payload.disabled,

            customer=payload.customer,

            country=payload.country,

            company_address=payload.company_address,

            letter_head=payload.letter_head,

            tc_name=payload.tc_name,

            select_print_heading=payload.select_print_heading,

            selling_price_list=payload.selling_price_list,

            currency=payload.currency,

            write_off_account_id=payload.write_off_account_id,

            write_off_cost_center_id=payload.write_off_cost_center_id,

            account_for_change_amount_id=payload.account_for_change_amount_id,

            income_account_id=payload.income_account_id,

            expense_account_id=payload.expense_account_id,

            cost_center_id=payload.cost_center_id,

            taxes_and_charges=payload.taxes_and_charges,

            apply_discount_on=payload.apply_discount_on,

            tax_category_id=payload.tax_category_id,

            print_format=payload.print_format,

            warehouse=payload.warehouse,

            ignore_pricing_rule=payload.ignore_pricing_rule,

            update_stock=payload.update_stock,

            hide_unavailable_items=payload.hide_unavailable_items,

            hide_images=payload.hide_images,

            auto_add_item_to_cart=payload.auto_add_item_to_cart,

            allow_rate_change=payload.allow_rate_change,

            allow_discount_change=payload.allow_discount_change,

            validate_stock_on_save=payload.validate_stock_on_save,

            write_off_limit=payload.write_off_limit,

            disable_rounded_total=payload.disable_rounded_total,

            utm_campaign=payload.utm_campaign,

            utm_source=payload.utm_source,

            utm_medium=payload.utm_medium,

            print_receipt_on_order_complete=payload.print_receipt_on_order_complete,

            project=payload.project,

            set_grand_total_to_default_mop=payload.set_grand_total_to_default_mop,

            action_on_new_invoice=payload.action_on_new_invoice,

            allow_partial_payment=payload.allow_partial_payment,

            allow_warehouse_change=payload.allow_warehouse_change,

        )

        self._replace_applicable_for_users(business_id, row, [x.model_dump() for x in payload.applicable_for_users])

        self._replace_payments(business_id, row, [x.model_dump() for x in payload.payments])

        self._replace_item_groups(business_id, row, [x.model_dump() for x in payload.item_groups])

        self._replace_customer_groups(business_id, row, [x.model_dump() for x in payload.customer_groups])



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

        payload: POSProfileUpdate,

    ) -> POSProfile:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                if field_name == "applicable_for_users":

                    self._replace_applicable_for_users(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "payments":

                    self._replace_payments(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "item_groups":

                    self._replace_item_groups(business_id, row, value or [])

                else:

                    setattr(row, field_name, value)

                if field_name == "customer_groups":

                    self._replace_customer_groups(business_id, row, value or [])

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
