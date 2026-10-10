# HAND-WRITTEN

"""

Business logic for Coupon Code -- port of

``erpnext/accounts/doctype/coupon_code/coupon_code.py``.







Upstream hooks:

    autoname

    validate



**Upstream has 1 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.coupon_code_domain.models.coupon_code import CouponCode

from app.accounts.coupon_code_domain.repositories.coupon_code_repository import (

    CouponCodeRepository,

)

from app.accounts.coupon_code_domain.schemas.coupon_code import (

    CouponCodeCreate,

    CouponCodeUpdate,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["CouponCodeService"]





class CouponCodeService:

    def __init__(self, repository: Optional[CouponCodeRepository] = None) -> None:

        self.repository = repository or CouponCodeRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> CouponCode:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Coupon Code", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: CouponCode

    ) -> None:

        """

        TODO(PORT-VALIDATION): upstream validation is NOT ported.



        This controller has **1 ``frappe.throw`` site(s)** upstream.

        None are enforced here, so writes upstream would reject

        currently succeed. It fails open deliberately rather than

        blocking the CRUD surface, but must not be read as complete.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> CouponCode:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[CouponCode]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[CouponCode].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(CouponCode).where(

                    CouponCode.business_id == business_id

                )

            )

            or 0

        )

        return f"COU-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: CouponCodeCreate

    ) -> CouponCode:

        row = CouponCode(

            business_id=business_id,

            name=self.next_name(db, business_id),

            coupon_name=payload.coupon_name,

            coupon_type=payload.coupon_type,

            customer=payload.customer,

            coupon_code=payload.coupon_code,

            pricing_rule=payload.pricing_rule,

            valid_from=payload.valid_from,

            valid_upto=payload.valid_upto,

            maximum_use=payload.maximum_use,

            used=payload.used,

            description=payload.description,

            amended_from=payload.amended_from,

            from_external_ecomm_platform=payload.from_external_ecomm_platform,

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

        payload: CouponCodeUpdate,

    ) -> CouponCode:

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
