"""
Repository for Customer data access.
"""

import uuid
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.customers.models.customer import Customer, CustomerStatus


class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, customer: Customer) -> Customer:
        self.db.add(customer)
        self.db.flush()
        return customer

    def get_by_id(
        self, customer_id: uuid.UUID, business_id: uuid.UUID
    ) -> Optional[Customer]:
        stmt = select(Customer).where(
            Customer.id == customer_id,
            Customer.business_id == business_id,
            Customer.is_deleted.is_(False),
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_lead_id(
        self, lead_id: uuid.UUID, business_id: uuid.UUID
    ) -> Optional[Customer]:
        stmt = select(Customer).where(
            Customer.converted_from_lead_id == lead_id,
            Customer.business_id == business_id,
            Customer.is_deleted.is_(False),
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def list_by_business(
        self,
        business_id: uuid.UUID,
        *,
        status: Optional[CustomerStatus] = None,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 25,
    ) -> tuple[list[Customer], int]:
        filters = [
            Customer.business_id == business_id,
            Customer.is_deleted.is_(False),
        ]
        if status is not None:
            filters.append(Customer.status == status)
        if search:
            filters.append(Customer.customer_name.ilike(f"%{search}%"))

        count_stmt = select(func.count()).select_from(Customer).where(*filters)
        total = self.db.execute(count_stmt).scalar_one()

        stmt = (
            select(Customer)
            .where(*filters)
            .order_by(Customer.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        items = list(self.db.execute(stmt).scalars().all())
        return items, total

    def update(self, customer: Customer) -> Customer:
        self.db.add(customer)
        self.db.flush()
        return customer

    def soft_delete(self, customer: Customer) -> Customer:
        customer.is_deleted = True
        customer.deleted_at = func.now()
        self.db.add(customer)
        self.db.flush()
        return customer

    def exists_with_gstin(
        self, gstin: str, business_id: uuid.UUID, exclude_id: Optional[uuid.UUID] = None
    ) -> bool:
        filters = [
            Customer.gstin == gstin,
            Customer.business_id == business_id,
            Customer.is_deleted.is_(False),
        ]
        if exclude_id is not None:
            filters.append(Customer.id != exclude_id)
        stmt = select(Customer.id).where(*filters)
        return self.db.execute(stmt).first() is not None
