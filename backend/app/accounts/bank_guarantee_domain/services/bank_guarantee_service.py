"""

Business logic for Bank Guarantee -- port of

``erpnext/accounts/doctype/bank_guarantee/bank_guarantee.py``.



Upstream hook -> here

-------------------

``autoname`` (ACC-BG-.YYYY.-.#####)  ``repository.next_name``

``validate``                         :meth:`_validate`

``on_submit``                        :meth:`_validate_for_submit` (run by :meth:`submit`)



Upstream splits the rules across two hooks: ``validate`` requires a customer or

supplier on every save, while ``on_submit`` additionally requires the guarantee

number, beneficiary and bank. That split is preserved -- a draft may be saved

incomplete, but it cannot be submitted that way.



The module-level ``get_voucher_details`` is not ported: it reads Sales Order /

Purchase Order, neither of which is converted yet.

"""



from __future__ import annotations



import uuid

from datetime import date

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.bank_guarantee_domain.models.bank_guarantee import BankGuarantee

from app.accounts.bank_guarantee_domain.repositories.bank_guarantee_repository import (

    BankGuaranteeRepository,

)

from app.accounts.bank_guarantee_domain.schemas.bank_guarantee import (

    BankGuaranteeCreate,

    BankGuaranteeUpdate,

)

from app.core.docstatus import (

    DocStatus,

    assert_can_amend,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BankGuaranteeService"]





class BankGuaranteeService:

    def __init__(self, repository: Optional[BankGuaranteeRepository] = None) -> None:

        self.repository = repository or BankGuaranteeRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, guarantee_id: uuid.UUID

    ) -> BankGuarantee:

        row = self.repository.get_by_id(db, business_id, guarantee_id)

        if row is None:

            raise NotFoundError("Bank Guarantee", guarantee_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    @staticmethod

    def _validate(row: BankGuarantee) -> None:

        """Port of ``validate``: a counterparty is always required."""

        if not (row.customer or row.supplier):

            raise DomainValidationError(

                "Select the customer or supplier.", code="bank_guarantee_party_mandatory"

            )



    @staticmethod

    def _validate_dates(row: BankGuarantee) -> None:

        """

        Not an upstream throw, but the invariant ``validity`` exists to express:

        ``end_date`` should be ``start_date + validity days`` when both are set.

        Kept as a consistency check rather than an auto-fill so an explicitly

        negotiated end date is never silently overwritten.

        """

        if row.start_date and row.end_date and row.end_date < row.start_date:

            raise DomainValidationError(

                "End Date cannot be before Start Date",

                code="bank_guarantee_end_before_start",

            )



    @staticmethod

    def _validate_for_submit(row: BankGuarantee) -> None:

        """

        Port of ``on_submit`` -- three throws, in upstream order.



        These are deliberately *not* in :meth:`_validate`, so a draft can be

        saved before the bank has issued a number.

        """

        if not row.bank_guarantee_number:

            raise DomainValidationError(

                "Enter the Bank Guarantee Number before submitting.",

                code="bank_guarantee_number_mandatory",

            )

        if not row.name_of_beneficiary:

            raise DomainValidationError(

                "Enter the name of the Beneficiary before submitting.",

                code="bank_guarantee_beneficiary_mandatory",

            )

        if row.bank_id is None:

            raise DomainValidationError(

                "Enter the name of the bank or lending institution before submitting.",

                code="bank_guarantee_bank_mandatory",

            )



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, guarantee_id: uuid.UUID

    ) -> BankGuarantee:

        return self._get_or_404(db, business_id, guarantee_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[BankGuarantee]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[BankGuarantee].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def create(

        self, db: Session, business_id: uuid.UUID, payload: BankGuaranteeCreate

    ) -> BankGuarantee:

        row = BankGuarantee(

            business_id=business_id,

            name=self.repository.next_name(db, business_id, date.today()),

            bg_type=payload.bg_type,

            amount=payload.amount,

            start_date=payload.start_date,

            validity=payload.validity,

            end_date=payload.end_date,

            customer=payload.customer,

            supplier=payload.supplier,

            project=payload.project,

            reference_doctype=payload.reference_doctype,

            reference_docname=payload.reference_docname,

            bank_id=payload.bank_id,

            bank_account_id=payload.bank_account_id,

            account_id=payload.account_id,

            bank_account_no=payload.bank_account_no,

            iban=payload.iban,

            branch_code=payload.branch_code,

            swift_number=payload.swift_number,

            bank_guarantee_number=payload.bank_guarantee_number,

            name_of_beneficiary=payload.name_of_beneficiary,

            fixed_deposit_number=payload.fixed_deposit_number,

            margin_money=payload.margin_money,

            charges=payload.charges,

            more_information=payload.more_information,

            docstatus=DocStatus.DRAFT.value,

        )



        try:

            self._validate(row)

            self._validate_dates(row)

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

        guarantee_id: uuid.UUID,

        payload: BankGuaranteeUpdate,

    ) -> BankGuarantee:

        row = self._get_or_404(db, business_id, guarantee_id)

        if not row.is_draft:

            raise DomainValidationError(

                "Only a draft Bank Guarantee can be edited. Cancel and amend it instead.",

                code="bank_guarantee_not_editable",

            )



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            for field_name, value in changes.items():

                setattr(row, field_name, value)



            self._validate(row)

            self._validate_dates(row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def delete(self, db: Session, business_id: uuid.UUID, guarantee_id: uuid.UUID) -> None:

        row = self._get_or_404(db, business_id, guarantee_id)

        if not row.is_draft:

            raise DomainValidationError(

                "Only a draft Bank Guarantee can be deleted. Cancel it first.",

                code="bank_guarantee_not_deletable",

            )

        self.repository.delete(db, row)

        db.commit()



    # ── lifecycle ────────────────────────────────────────────────────────────

    def submit(

        self, db: Session, business_id: uuid.UUID, guarantee_id: uuid.UUID

    ) -> BankGuarantee:

        """

        Runs ``on_submit``'s checks *before* flipping docstatus, so a failed

        submit leaves the document a draft rather than half-promoted.

        """

        row = self._get_or_404(db, business_id, guarantee_id)

        assert_can_submit(row, "Bank Guarantee")

        self._validate_for_submit(row)



        row.docstatus = DocStatus.SUBMITTED.value

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, guarantee_id: uuid.UUID

    ) -> BankGuarantee:

        row = self._get_or_404(db, business_id, guarantee_id)

        assert_can_cancel(row, "Bank Guarantee")

        row.docstatus = DocStatus.CANCELLED.value

        db.commit()

        db.refresh(row)

        return row



    def amend(

        self, db: Session, business_id: uuid.UUID, guarantee_id: uuid.UUID

    ) -> BankGuarantee:

        source = self._get_or_404(db, business_id, guarantee_id)

        assert_can_amend(source, "Bank Guarantee")



        clone = BankGuarantee(

            business_id=business_id,

            name=self.repository.next_name(db, business_id, date.today()),

            bg_type=source.bg_type,

            amount=source.amount,

            start_date=source.start_date,

            validity=source.validity,

            end_date=source.end_date,

            customer=source.customer,

            supplier=source.supplier,

            project=source.project,

            reference_doctype=source.reference_doctype,

            reference_docname=source.reference_docname,

            bank_id=source.bank_id,

            bank_account_id=source.bank_account_id,

            account_id=source.account_id,

            bank_account_no=source.bank_account_no,

            iban=source.iban,

            branch_code=source.branch_code,

            swift_number=source.swift_number,

            bank_guarantee_number=source.bank_guarantee_number,

            name_of_beneficiary=source.name_of_beneficiary,

            fixed_deposit_number=source.fixed_deposit_number,

            margin_money=source.margin_money,

            charges=source.charges,

            more_information=source.more_information,

            amended_from_id=source.id,

            docstatus=DocStatus.DRAFT.value,

        )

        self.repository.add(db, clone)

        db.commit()

        db.refresh(clone)

        return clone
