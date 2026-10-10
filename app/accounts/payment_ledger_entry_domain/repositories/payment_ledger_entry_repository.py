"""Data access for Payment Ledger Entry. Every query is scoped by business_id."""



from __future__ import annotations



import uuid

from datetime import date

from decimal import Decimal

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.payment_ledger_entry_domain.models.payment_ledger_entry import (

    PLEAccountType,

    PaymentLedgerEntry,

)

from app.core.docstatus import DocStatus



__all__ = ["PaymentLedgerEntryRepository"]



#: ERPNext's ``OUTSTANDING_DOCTYPES`` -- the vouchers whose outstanding amount a

#: payment ledger row moves. Kept as names rather than FKs because the doctypes

#: themselves are not converted.

OUTSTANDING_DOCTYPES = ("Sales Invoice", "Purchase Invoice", "Payment Entry", "Journal Entry")





class PaymentLedgerEntryRepository:

    def get_by_id(

        self, db: Session, business_id: uuid.UUID, entry_id: uuid.UUID

    ) -> Optional[PaymentLedgerEntry]:

        return db.scalar(

            select(PaymentLedgerEntry).where(

                PaymentLedgerEntry.business_id == business_id,

                PaymentLedgerEntry.id == entry_id,

            )

        )



    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[PaymentLedgerEntry]:

        return db.scalar(

            select(PaymentLedgerEntry).where(

                PaymentLedgerEntry.business_id == business_id,

                PaymentLedgerEntry.name == name,

            )

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """

        ``ACC-PLE-#####``.



        Upstream has no ``autoname`` and lets Frappe mint a hash. A hash is

        useless in a REST API, so this port keeps a per-tenant sequence instead.

        """

        count = int(

            db.scalar(

                select(func.count())

                .select_from(PaymentLedgerEntry)

                .where(PaymentLedgerEntry.business_id == business_id)

            )

            or 0

        )

        return f"ACC-PLE-{count + 1:05d}"



    # ── balances ─────────────────────────────────────────────────────────────

    def _outstanding_select(self, business_id: uuid.UUID):

        """

        Shared filter for every outstanding read.



        Cancelled rows and delinked rows are both out of the running balance:

        the first never happened, the second has been written off.

        """

        return select(func.coalesce(func.sum(PaymentLedgerEntry.amount), 0)).where(

            PaymentLedgerEntry.business_id == business_id,

            PaymentLedgerEntry.docstatus != DocStatus.CANCELLED.value,

            PaymentLedgerEntry.delinked.is_(False),

        )



    def invoice_outstanding(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        account_id: Optional[uuid.UUID] = None,

        party_type: Optional[str] = None,

        party: Optional[str] = None,

        against_voucher_no: Optional[str] = None,

    ) -> Decimal:

        """

        Port of ``get_invoice_outstanding_amounts``.



        Sums every open row for one invoice. A payment against it posts a

        negative row, so the sum is what is still owed.

        """

        stmt = self._outstanding_select(business_id)

        if account_id is not None:

            stmt = stmt.where(PaymentLedgerEntry.account_id == account_id)

        if party_type is not None:

            stmt = stmt.where(PaymentLedgerEntry.party_type == party_type)

        if party is not None:

            stmt = stmt.where(PaymentLedgerEntry.party == party)

        if against_voucher_no is not None:

            stmt = stmt.where(PaymentLedgerEntry.against_voucher_no == against_voucher_no)

        return Decimal(str(db.scalar(stmt) or 0))



    def party_outstanding(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        account_id: Optional[uuid.UUID] = None,

        party_type: Optional[str] = None,

        party: Optional[str] = None,

        as_on: Optional[date] = None,

    ) -> Decimal:

        """Everything still open for a party, ignoring which invoice it sits on."""

        stmt = self._outstanding_select(business_id)

        if account_id is not None:

            stmt = stmt.where(PaymentLedgerEntry.account_id == account_id)

        if party_type is not None:

            stmt = stmt.where(PaymentLedgerEntry.party_type == party_type)

        if party is not None:

            stmt = stmt.where(PaymentLedgerEntry.party == party)

        if as_on is not None:

            stmt = stmt.where(PaymentLedgerEntry.posting_date <= as_on)

        return Decimal(str(db.scalar(stmt) or 0))



    def open_rows_for_voucher(

        self, db: Session, business_id: uuid.UUID, voucher_type: str, voucher_no: str

    ) -> list[PaymentLedgerEntry]:

        return list(

            db.scalars(

                select(PaymentLedgerEntry).where(

                    PaymentLedgerEntry.business_id == business_id,

                    PaymentLedgerEntry.voucher_type == voucher_type,

                    PaymentLedgerEntry.voucher_no == voucher_no,

                    PaymentLedgerEntry.docstatus != DocStatus.CANCELLED.value,

                )

            )

        )



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        account_id: Optional[uuid.UUID] = None,

        account_type: Optional[str] = None,

        party_type: Optional[str] = None,

        party: Optional[str] = None,

        against_voucher_no: Optional[str] = None,

        from_date: Optional[date] = None,

        to_date: Optional[date] = None,

        delinked: Optional[bool] = None,

        docstatus: Optional[int] = None,

        include_cancelled: bool = False,

        search: Optional[str] = None,

    ) -> tuple[list[PaymentLedgerEntry], int]:

        conditions = [PaymentLedgerEntry.business_id == business_id]



        if not include_cancelled and docstatus is None:

            conditions.append(PaymentLedgerEntry.docstatus != DocStatus.CANCELLED.value)

        if docstatus is not None:

            conditions.append(PaymentLedgerEntry.docstatus == docstatus)

        if account_id is not None:

            conditions.append(PaymentLedgerEntry.account_id == account_id)

        if account_type is not None:

            conditions.append(PaymentLedgerEntry.account_type == PLEAccountType(account_type))

        if party_type is not None:

            conditions.append(PaymentLedgerEntry.party_type == party_type)

        if party is not None:

            conditions.append(PaymentLedgerEntry.party == party)

        if against_voucher_no is not None:

            conditions.append(PaymentLedgerEntry.against_voucher_no == against_voucher_no)

        if from_date is not None:

            conditions.append(PaymentLedgerEntry.posting_date >= from_date)

        if to_date is not None:

            conditions.append(PaymentLedgerEntry.posting_date <= to_date)

        if delinked is not None:

            conditions.append(PaymentLedgerEntry.delinked.is_(delinked))

        if search:

            like = f"%{search.strip()}%"

            conditions.append(

                PaymentLedgerEntry.name.ilike(like)

                | PaymentLedgerEntry.party.ilike(like)

                | PaymentLedgerEntry.against_voucher_no.ilike(like)

            )



        total = int(

            db.scalar(

                select(func.count())

                .select_from(PaymentLedgerEntry)

                .where(*conditions)

            )

            or 0

        )

        rows = list(

            db.scalars(

                select(PaymentLedgerEntry)

                .where(*conditions)

                .order_by(PaymentLedgerEntry.posting_date.desc(), PaymentLedgerEntry.name.desc())

                .offset(offset)

                .limit(limit)

            )

        )

        return rows, total



    def add(self, db: Session, entry: PaymentLedgerEntry) -> PaymentLedgerEntry:

        db.add(entry)

        db.flush()

        return entry



    def delete(self, db: Session, entry: PaymentLedgerEntry) -> None:

        db.delete(entry)

        db.flush()
