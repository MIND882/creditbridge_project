# app/crm/quotation_domain/repositories/quotation_repository.py

"""
Repository for Quotation data access, including its three child tables
(QuotationItem, QuotationTax, QuotationPaymentScheduleEntry).

ASSUMPTION: synchronous SQLAlchemy `Session` — matching the convention
used elsewhere in this codebase. Verify against the actual
`app/db/session.py` / `app/customers/repositories/customer_repository.py`
before use.
"""

import uuid
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.crm.quotation_domain.models.quotation import (
    Quotation,
    QuotationItem,
    QuotationPaymentScheduleEntry,
    QuotationStatus,
    QuotationTax,
)


class QuotationRepository:
    def __init__(self, db: Session):
        self.db = db

    def _base_query(self):
        return select(Quotation).options(
            selectinload(Quotation.items),
            selectinload(Quotation.taxes),
            selectinload(Quotation.payment_schedule_entries),
        )

    def create(self, quotation: Quotation) -> Quotation:
        self.db.add(quotation)
        self.db.flush()
        return quotation

    def get_by_id(
        self, quotation_id: uuid.UUID, business_id: uuid.UUID
    ) -> Optional[Quotation]:
        stmt = self._base_query().where(
            Quotation.id == quotation_id,
            Quotation.business_id == business_id,
            Quotation.is_deleted.is_(False),
        )
        return self.db.execute(stmt).unique().scalar_one_or_none()

    def list_by_opportunity(
        self, opportunity_id: uuid.UUID, business_id: uuid.UUID
    ) -> list[Quotation]:
        stmt = self._base_query().where(
            Quotation.opportunity_id == opportunity_id,
            Quotation.business_id == business_id,
            Quotation.is_deleted.is_(False),
        )
        return list(self.db.execute(stmt).unique().scalars().all())

    def list_by_business(
        self,
        business_id: uuid.UUID,
        *,
        status: Optional[QuotationStatus] = None,
        page: int = 1,
        page_size: int = 25,
    ) -> tuple[list[Quotation], int]:
        filters = [
            Quotation.business_id == business_id,
            Quotation.is_deleted.is_(False),
        ]
        if status is not None:
            filters.append(Quotation.status == status)

        count_stmt = select(func.count()).select_from(Quotation).where(*filters)
        total = self.db.execute(count_stmt).scalar_one()

        stmt = (
            self._base_query()
            .where(*filters)
            .order_by(Quotation.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        items = list(self.db.execute(stmt).unique().scalars().all())
        return items, total

    def list_sent_expiring_before(
        self, business_id: uuid.UUID, cutoff_date
    ) -> list[Quotation]:
        """Used by the auto-expire scheduled job — mirrors ERPNext's
        set_expired_status()."""
        stmt = select(Quotation).where(
            Quotation.business_id == business_id,
            Quotation.status == QuotationStatus.SENT,
            Quotation.valid_till < cutoff_date,
            Quotation.is_deleted.is_(False),
        )
        return list(self.db.execute(stmt).scalars().all())

    def replace_items(self, quotation: Quotation, items: list[QuotationItem]) -> None:
        quotation.items.clear()
        self.db.flush()
        for idx, item in enumerate(items):
            item.idx = idx
            quotation.items.append(item)

    def replace_taxes(self, quotation: Quotation, taxes: list[QuotationTax]) -> None:
        quotation.taxes.clear()
        self.db.flush()
        for idx, tax in enumerate(taxes):
            tax.idx = idx
            quotation.taxes.append(tax)

    def replace_payment_schedule(
        self, quotation: Quotation, entries: list[QuotationPaymentScheduleEntry]
    ) -> None:
        quotation.payment_schedule_entries.clear()
        self.db.flush()
        for idx, entry in enumerate(entries):
            entry.idx = idx
            quotation.payment_schedule_entries.append(entry)

    def update(self, quotation: Quotation) -> Quotation:
        self.db.add(quotation)
        self.db.flush()
        return quotation

    def soft_delete(self, quotation: Quotation) -> Quotation:
        quotation.is_deleted = True
        quotation.deleted_at = func.now()
        self.db.add(quotation)
        self.db.flush()
        return quotation