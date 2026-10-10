# HAND-WRITTEN

"""

Business logic for Share Transfer -- port of

``erpnext/accounts/doctype/share_transfer/share_transfer.py``.



Submittable, so ``submit``/``cancel`` guard the docstatus transitions.



Upstream hooks:

    on_submit

    on_cancel

    validate

    basic_validations

    share_exists

    folio_no_validation

    autoname_folio

    remove_shares

    return_share_balance_entry

    get_shareholder_doc

    get_company_shareholder



**Upstream has 13 `frappe.throw` site(s). They are NOT yet ported -- see `_validate` below.**

"""



from __future__ import annotations



import uuid

from decimal import Decimal

from typing import Optional



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.share_transfer_domain.models.share_transfer import ShareTransfer

from app.accounts.share_transfer_domain.repositories.share_transfer_repository import (

    ShareTransferRepository,

)

from app.accounts.share_transfer_domain.schemas.share_transfer import (

    ShareTransferCreate,

    ShareTransferUpdate,

)

from app.accounts.share_balance_domain.models.share_balance import ShareBalance

from app.accounts.shareholder_domain.models.shareholder import Shareholder

from app.core.docstatus import (

    DocStatus,

    assert_can_cancel,

    assert_can_submit,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ShareTransferService"]





def _dec(value) -> Decimal:

    """Coerce a possibly-None Numeric column to Decimal."""

    return Decimal(str(value if value is not None else 0))





def _transfer_type(value) -> str:

    """Unwrap the enum, tolerating a raw string."""

    return getattr(value, "value", value)





class ShareTransferService:

    def __init__(self, repository: Optional[ShareTransferRepository] = None) -> None:

        self.repository = repository or ShareTransferRepository()



    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ShareTransfer:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Share Transfer", row_id)

        return row



    # ── ported validators ────────────────────────────────────────────────────

    # ══════════════════════════════════════════════════════════════════════

    # ported validators

    # ══════════════════════════════════════════════════════════════════════

    def _validate(

        self, db: Session, business_id: uuid.UUID, row: ShareTransfer

    ) -> None:

        """

        Port of upstream ``validate``:



            self.get_company_shareholder()   -> _company_shareholder (ensures one)

            self.basic_validations()         -> _basic_validations

            self.folio_no_validation()       -> _folio_no_validation

            self.share_exists(...)           -> _share_exists



        Order matters: ``_basic_validations`` blanks the shareholder that does

        not apply to the transfer type *before* the seller==buyer check, and

        ``_folio_no_validation`` may write folio numbers that later reads rely on.

        """

        self._company_shareholder(db, business_id)

        self._basic_validations(db, business_id, row)

        self._folio_no_validation(db, business_id, row)

        self._validate_share_exists(db, business_id, row)



    # ── basic_validations ─────────────────────────────────────────────────

    def _basic_validations(

        self, db: Session, business_id: uuid.UUID, row: ShareTransfer

    ) -> None:

        ttype = _transfer_type(row.transfer_type)



        if ttype == "Purchase":

            # Upstream clears to_shareholder first, so a stray value cannot

            # later trip the seller==buyer check.

            row.to_shareholder_id = None

            if not row.from_shareholder_id:

                raise DomainValidationError(

                    "The field From Shareholder cannot be blank",

                    code="share_transfer_from_shareholder_required",

                )

            if not row.from_folio_no:

                # Upstream calls autoname_folio(self.to_shareholder) here, which

                # it has just blanked -- that raises upstream. The only party in

                # a Purchase is the seller, so name against that instead.

                row.to_folio_no = self._autoname_folio(db, business_id, row.from_shareholder_id)

            if not row.asset_account_id:

                raise DomainValidationError(

                    "The field Asset Account cannot be blank",

                    code="share_transfer_asset_account_required",

                )



        elif ttype == "Issue":

            row.from_shareholder_id = None

            if not row.to_shareholder_id:

                raise DomainValidationError(

                    "The field To Shareholder cannot be blank",

                    code="share_transfer_to_shareholder_required",

                )

            if not row.to_folio_no:

                row.to_folio_no = self._autoname_folio(db, business_id, row.to_shareholder_id)

            if not row.asset_account_id:

                raise DomainValidationError(

                    "The field Asset Account cannot be blank",

                    code="share_transfer_asset_account_required",

                )



        else:  # "Transfer"

            if not row.from_shareholder_id or not row.to_shareholder_id:

                raise DomainValidationError(

                    "The fields From Shareholder and To Shareholder cannot be blank",

                    code="share_transfer_both_shareholders_required",

                )

            if not row.to_folio_no:

                row.to_folio_no = self._autoname_folio(db, business_id, row.to_shareholder_id)



        if not row.equity_or_liability_account_id:

            raise DomainValidationError(

                "The field Equity/Liability Account cannot be blank",

                code="share_transfer_equity_account_required",

            )



        if row.from_shareholder_id and row.from_shareholder_id == row.to_shareholder_id:

            raise DomainValidationError(

                "The seller and the buyer cannot be the same",

                code="share_transfer_same_seller_and_buyer",

                details={"shareholder_id": str(row.from_shareholder_id)},

            )



        # Share numbers are an inclusive range, hence the +1.

        if row.no_of_shares != row.to_no - row.from_no + 1:

            raise DomainValidationError(

                "The number of shares and the share numbers are inconsistent",

                code="share_transfer_share_count_mismatch",

                details={

                    "no_of_shares": row.no_of_shares,

                    "expected": row.to_no - row.from_no + 1,

                },

            )



        if not row.amount:

            row.amount = _dec(row.rate) * row.no_of_shares

        if _dec(row.amount) != _dec(row.rate) * row.no_of_shares:

            raise DomainValidationError(

                "There are inconsistencies between the rate, no of shares and "

                "the amount calculated",

                code="share_transfer_amount_mismatch",

                details={

                    "amount": str(row.amount),

                    "expected": str(_dec(row.rate) * row.no_of_shares),

                },

            )



    # ── folio_no_validation ───────────────────────────────────────────────

    def _folio_no_validation(

        self, db: Session, business_id: uuid.UUID, row: ShareTransfer

    ) -> None:

        for field, folio in (

            ("from", (row.from_shareholder_id, row.from_folio_no)),

            ("to", (row.to_shareholder_id, row.to_folio_no)),

        ):

            shareholder_id, expected_folio = folio

            if not shareholder_id:

                continue

            sh = self._shareholder_or_fail(db, business_id, shareholder_id, field)



            if not sh.folio_no:

                sh.folio_no = expected_folio

                db.flush()

            elif expected_folio and sh.folio_no != expected_folio:

                raise DomainValidationError(

                    "The folio numbers are not matching",

                    code="share_transfer_folio_mismatch",

                    details={

                        "shareholder": sh.title,

                        "folio_no": sh.folio_no,

                        "expected": expected_folio,

                    },

                )



    # ── share_exists ──────────────────────────────────────────────────────

    def _validate_share_exists(

        self, db: Session, business_id: uuid.UUID, row: ShareTransfer

    ) -> None:

        ttype = _transfer_type(row.transfer_type)

        if ttype == "Issue":

            company = self._company_shareholder(db, business_id)

            state = self._share_exists(db, business_id, company.id, row)

            if state in ("Complete", "Partial"):

                raise DomainValidationError(

                    "The shares already exist",

                    code="share_transfer_shares_already_exist",

                    details={"coverage": state},

                )

        else:

            state = self._share_exists(db, business_id, row.from_shareholder_id, row)

            if state in ("Outside", "Partial"):

                raise DomainValidationError(

                    f"The shares don\'t exist with the {row.from_shareholder_id}",

                    code="share_transfer_shares_dont_exist",

                    details={"coverage": state},

                )



    def _share_exists(

        self, db: Session, business_id: uuid.UUID, shareholder_id, row: ShareTransfer

    ) -> str:

        """

        Classify how ``[from_no, to_no]`` sits against a shareholder's holdings:

        ``Complete`` (one holding covers it), ``Partial`` (it straddles a

        boundary) or ``Outside`` (no holding overlaps at all).



        Entries of a different share type are skipped -- a Preference holding

        does not back an Equity transfer.

        """

        if not shareholder_id:

            return "Outside"

        for entry in self._balances(db, business_id, shareholder_id):

            if (

                entry.share_type_id != row.share_type_id

                or entry.from_no > row.to_no

                or entry.to_no < row.from_no

            ):

                continue

            if entry.from_no <= row.from_no and entry.to_no >= row.to_no:

                return "Complete"

            if entry.from_no <= row.from_no <= entry.to_no:

                return "Partial"

            if entry.from_no <= row.to_no <= entry.to_no:

                return "Partial"

        return "Outside"



    # ══════════════════════════════════════════════════════════════════════

    # on_submit / on_cancel -- Share Balance register movement

    # ══════════════════════════════════════════════════════════════════════

    def _on_submit(

        self, db: Session, business_id: uuid.UUID, row: ShareTransfer

    ) -> None:

        """Port of ``on_submit``."""

        ttype = _transfer_type(row.transfer_type)

        company = self._company_shareholder(db, business_id)



        if ttype == "Issue":

            self._append_balance(db, business_id, company.id, row, is_company=True,

                                 current_state="Issued")

            self._append_balance(db, business_id, row.to_shareholder_id, row)



        elif ttype == "Purchase":

            self._remove_shares(db, business_id, row.from_shareholder_id, row)

            self._remove_shares(db, business_id, company.id, row)



        else:  # "Transfer"

            self._remove_shares(db, business_id, row.from_shareholder_id, row)

            self._append_balance(db, business_id, row.to_shareholder_id, row)



    def _on_cancel(

        self, db: Session, business_id: uuid.UUID, row: ShareTransfer

    ) -> None:

        """Port of ``on_cancel`` -- the exact inverse of ``_on_submit``."""

        ttype = _transfer_type(row.transfer_type)

        company = self._company_shareholder(db, business_id)



        if ttype == "Issue":

            self._remove_shares(db, business_id, company.id, row)

            self._remove_shares(db, business_id, row.to_shareholder_id, row)



        elif ttype == "Purchase":

            self._append_balance(db, business_id, row.from_shareholder_id, row)

            self._append_balance(db, business_id, company.id, row)



        else:  # "Transfer"

            self._remove_shares(db, business_id, row.to_shareholder_id, row)

            self._append_balance(db, business_id, row.from_shareholder_id, row)



    def _append_balance(

        self, db: Session, business_id: uuid.UUID, shareholder_id, row: ShareTransfer,

        *, is_company: bool = False, current_state: Optional[str] = None,

    ) -> None:

        if not shareholder_id:

            return

        existing = self._balances(db, business_id, shareholder_id)

        db.add(

            ShareBalance(

                business_id=business_id,

                parent_id=shareholder_id,

                idx=len(existing) + 1,

                share_type_id=row.share_type_id,

                from_no=row.from_no,

                to_no=row.to_no,

                rate=_dec(row.rate),

                no_of_shares=row.no_of_shares,

                amount=_dec(row.amount or 0),

                is_company=is_company,

                current_state=current_state,

            )

        )

        db.flush()



    def _remove_shares(

        self, db: Session, business_id: uuid.UUID, shareholder_id, row: ShareTransfer

    ) -> None:

        """

        Port of ``remove_shares``: subtract ``[from_no, to_no]`` from the

        shareholder's holdings, splitting a holding that only partly overlaps.



        One deliberate deviation: upstream builds each remnant with

        ``amount = self.rate * count`` while passing the *entry's* rate, so a

        remnant keeps its old rate but is valued at the transfer's. That is

        inconsistent, and ShareBalance.amount is NOT NULL, so both are taken

        from the entry here.

        """

        if not shareholder_id:

            return

        entries = self._balances(db, business_id, shareholder_id)

        keep: list[tuple[int, int, Decimal]] = []



        for e in entries:

            if (

                e.share_type_id != row.share_type_id

                or e.from_no > row.to_no

                or e.to_no < row.from_no

            ):

                keep.append((e.from_no, e.to_no, _dec(e.rate)))

            elif e.from_no <= row.from_no and e.to_no >= row.to_no:

                # The transfer sits wholly inside this holding -> split.

                if e.from_no == row.from_no:

                    if e.to_no != row.to_no:

                        keep.append((row.to_no + 1, e.to_no, _dec(e.rate)))

                elif e.to_no == row.to_no:

                    keep.append((e.from_no, row.from_no - 1, _dec(e.rate)))

                else:

                    keep.append((e.from_no, row.from_no - 1, _dec(e.rate)))

                    keep.append((row.to_no + 1, e.to_no, _dec(e.rate)))

            elif e.from_no >= row.from_no and e.to_no <= row.to_no:

                pass  # wholly consumed

            elif row.from_no <= e.from_no <= row.to_no and e.to_no >= row.to_no:

                keep.append((row.to_no + 1, e.to_no, _dec(e.rate)))

            elif row.from_no <= e.to_no <= row.to_no and e.from_no <= row.from_no:

                keep.append((e.from_no, row.from_no - 1, _dec(e.rate)))

            else:

                keep.append((e.from_no, e.to_no, _dec(e.rate)))



        for e in entries:

            db.delete(e)

        db.flush()



        for idx, (from_no, to_no, rate) in enumerate(keep, start=1):

            db.add(

                ShareBalance(

                    business_id=business_id,

                    parent_id=shareholder_id,

                    idx=idx,

                    share_type_id=row.share_type_id,

                    from_no=from_no,

                    to_no=to_no,

                    rate=rate,

                    no_of_shares=to_no - from_no + 1,

                    amount=rate * (to_no - from_no + 1),

                )

            )

        db.flush()



    # ══════════════════════════════════════════════════════════════════════

    # lookups

    # ══════════════════════════════════════════════════════════════════════

    def _balances(self, db: Session, business_id: uuid.UUID, shareholder_id):

        return list(

            db.scalars(

                select(ShareBalance)

                .where(

                    ShareBalance.business_id == business_id,

                    ShareBalance.parent_id == shareholder_id,

                )

                .order_by(ShareBalance.idx)

            ).all()

        )



    def _shareholder_or_fail(

        self, db: Session, business_id: uuid.UUID, shareholder_id, field: str

    ) -> Shareholder:

        """

        Upstream compares ``doc.company != self.company`` and throws "The

        shareholder does not belong to this company". Company is the tenant

        here, so a shareholder owned elsewhere simply does not resolve.

        """

        sh = db.scalar(

            select(Shareholder).where(

                Shareholder.id == shareholder_id,

                Shareholder.business_id == business_id,

            )

        )

        if sh is None:

            raise DomainValidationError(

                "The shareholder does not belong to this company",

                code="share_transfer_shareholder_other_company",

                details={"field": field, "shareholder_id": str(shareholder_id)},

            )

        return sh



    def _company_shareholder(

        self, db: Session, business_id: uuid.UUID

    ) -> Shareholder:

        """

        Port of ``get_company_shareholder``: the tenant's own register, created

        on first use. Upstream keys it on ``company``; the tenant is the key here.

        """

        sh = db.scalar(

            select(Shareholder).where(

                Shareholder.business_id == business_id,

                Shareholder.is_company.is_(True),

            )

        )

        if sh is not None:

            return sh

        sh = Shareholder(

            business_id=business_id,

            name=f"SH-COMPANY-{business_id.hex[:8].upper()}",

            naming_series="SH-COMPANY-",

            title="Company",

            is_company=True,

        )

        db.add(sh)

        db.flush()

        return sh



    def _autoname_folio(

        self, db: Session, business_id: uuid.UUID, shareholder_id

    ) -> Optional[str]:

        """``autoname_folio``: mint ``FN.#####`` and store it on the shareholder."""

        if not shareholder_id:

            return None

        sh = db.scalar(

            select(Shareholder).where(

                Shareholder.id == shareholder_id,

                Shareholder.business_id == business_id,

            )

        )

        if sh is None:

            return None

        if sh.folio_no:

            return sh.folio_no

        count = int(

            db.scalar(

                select(func.count())

                .select_from(Shareholder)

                .where(

                    Shareholder.business_id == business_id,

                    Shareholder.folio_no.is_not(None),

                )

            )

            or 0

        )

        sh.folio_no = f"FN-{count + 1:05d}"

        db.flush()

        return sh.folio_no





    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ShareTransfer:

        return self._get_or_404(db, business_id, row_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ShareTransfer]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ShareTransfer].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def next_name(self, db: Session, business_id: uuid.UUID) -> str:

        """A per-tenant sequential name; upstream mints one from ``autoname``."""

        count = int(

            db.scalar(

                select(func.count()).select_from(ShareTransfer).where(

                    ShareTransfer.business_id == business_id

                )

            )

            or 0

        )

        return f"SHA-{count + 1:05d}"



    def create(

        self, db: Session, business_id: uuid.UUID, payload: ShareTransferCreate

    ) -> ShareTransfer:

        row = ShareTransfer(

            business_id=business_id,

            name=self.next_name(db, business_id),

            transfer_type=payload.transfer_type,

            date=payload.date,

            from_shareholder_id=payload.from_shareholder_id,

            from_folio_no=payload.from_folio_no,

            equity_or_liability_account_id=payload.equity_or_liability_account_id,

            asset_account_id=payload.asset_account_id,

            to_shareholder_id=payload.to_shareholder_id,

            to_folio_no=payload.to_folio_no,

            share_type_id=payload.share_type_id,

            from_no=payload.from_no,

            rate=payload.rate,

            no_of_shares=payload.no_of_shares,

            to_no=payload.to_no,

            amount=payload.amount,

            remarks=payload.remarks,

            amended_from=payload.amended_from,

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

        payload: ShareTransferUpdate,

    ) -> ShareTransfer:

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



    def submit(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ShareTransfer:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_submit(row, "Share Transfer")

        try:

            self._on_submit(db, business_id, row)

            row.docstatus = DocStatus.SUBMITTED.value

        except Exception:

            db.rollback()

            raise

        db.commit()

        db.refresh(row)

        return row



    def cancel(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ShareTransfer:

        row = self._get_or_404(db, business_id, row_id)

        assert_can_cancel(row, "Share Transfer")

        try:

            self._on_cancel(db, business_id, row)

            row.docstatus = DocStatus.CANCELLED.value

        except Exception:

            db.rollback()

            raise

        db.commit()

        db.refresh(row)

        return row
