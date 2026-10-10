# HAND-WRITTEN

"""

Business logic for Payment Gateway Account -- port of

``erpnext/accounts/doctype/payment_gateway_account/payment_gateway_account.py``.







Upstream hooks:

    autoname

    validate

    update_default_payment_gateway

    set_as_default_if_not_set



Upstream declares no validation, so `_validate` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.payment_gateway_account_domain.models.payment_gateway_account import PaymentGatewayAccount

from app.accounts.payment_gateway_account_domain.repositories.payment_gateway_account_repository import (

    PaymentGatewayAccountRepository,

)

from app.accounts.payment_gateway_account_domain.schemas.payment_gateway_account import (

    PaymentGatewayAccountCreate,

    PaymentGatewayAccountUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PaymentGatewayAccountService"]





class PaymentGatewayAccountService:

    def __init__(self, repository: Optional[PaymentGatewayAccountRepository] = None) -> None:

        self.repository = repository or PaymentGatewayAccountRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PaymentGatewayAccount:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Payment Gateway Account", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: PaymentGatewayAccount

    ) -> None:

        """

        Upstream's controller defines no ``frappe.throw``, so there is

        no rule to port. Empty by design, not by omission.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PaymentGatewayAccount:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PaymentGatewayAccount]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PaymentGatewayAccount].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(PaymentGatewayAccount).where(

                    PaymentGatewayAccount.business_id == business_id

                )

            )

            or 0

        )

        return f"PAY-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: PaymentGatewayAccountCreate

    ) -> PaymentGatewayAccount:

        row = PaymentGatewayAccount(

            business_id=business_id,

            name=self.next_name(db, business_id),

            payment_gateway=payload.payment_gateway,

            is_default=payload.is_default,

            payment_account_id=payload.payment_account_id,

            currency=payload.currency,

            message=payload.message,

            payment_channel=payload.payment_channel,

        )



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

        payload: PaymentGatewayAccountUpdate,

    ) -> PaymentGatewayAccount:

        row = self._get_or_404(db, business_id, row_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

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
