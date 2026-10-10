"""

Business logic for Accounting Dimension -- port of

``erpnext/accounts/doctype/accounting_dimension/accounting_dimension.py``.



Upstream hook -> here

-------------------

``autoname: field:label``       label uniqueness in :meth:`_assert_label_free`

fieldname derivation            :func:`make_fieldname`

``create_custom_fields``        :meth:`sync_custom_fields` (TODO stub)

``delete_custom_fields``        :meth:`sync_custom_fields` (TODO stub)



Upstream's real teeth are in the custom-field machinery: saving a dimension

physically adds a field to every transaction doctype, and deleting it removes

it. There is no runtime schema here, so that is stubbed with a named method

rather than silently dropped -- the call sites exist in :meth:`create` and

:meth:`delete` so the wiring survives.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.accounting_dimension_detail_domain.models.accounting_dimension_detail import (

    AccountingDimensionDetail,

)

from app.accounts.accounting_dimension_domain.models.accounting_dimension import (

    AccountingDimension,

    make_fieldname,

)

from app.accounts.accounting_dimension_domain.repositories.accounting_dimension_repository import (

    AccountingDimensionRepository,

)

from app.accounts.accounting_dimension_domain.schemas.accounting_dimension import (

    AccountingDimensionCreate,

    AccountingDimensionUpdate,

)

from app.core.errors import ConflictError, DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["AccountingDimensionService"]





class AccountingDimensionService:

    def __init__(self, repository: Optional[AccountingDimensionRepository] = None) -> None:

        self.repository = repository or AccountingDimensionRepository()



    # ── helpers ──────────────────────────────────────────────────────────────

    def _get_or_404(

        self, db: Session, business_id: uuid.UUID, dimension_id: uuid.UUID

    ) -> AccountingDimension:

        row = self.repository.get_by_id(db, business_id, dimension_id)

        if row is None:

            raise NotFoundError("Accounting Dimension", dimension_id)

        return row



    def _assert_label_free(

        self,

        db: Session,

        business_id: uuid.UUID,

        label: str,

        *,

        exclude_id: Optional[uuid.UUID] = None,

    ) -> None:

        existing = self.repository.get_by_name(db, business_id, label)

        if existing is not None and existing.id != exclude_id:

            raise ConflictError(

                f"Accounting Dimension '{label}' already exists",

                code="accounting_dimension_duplicate",

            )



    def _assert_fieldname_free(

        self,

        db: Session,

        business_id: uuid.UUID,

        fieldname: str,

        *,

        exclude_id: Optional[uuid.UUID] = None,

    ) -> None:

        """

        Stricter than the label check, and for a concrete reason: the fieldname

        is what would become a column on transaction doctypes, so two

        dimensions sharing one would write to the same place.

        """

        clash = self.repository.get_by_fieldname(

            db, business_id, fieldname, exclude_id=exclude_id

        )

        if clash is not None:

            raise ConflictError(

                f"Fieldname '{fieldname}' is already used by Accounting Dimension "

                f"'{clash.label}'. Use another label.",

                code="accounting_dimension_fieldname_duplicate",

            )



    def sync_custom_fields(

        self,

        db: Session,

        business_id: uuid.UUID,

        dimension: AccountingDimension,

        *,

        removing: bool = False,

    ) -> None:

        """

        Port of ``create_custom_fields`` / ``delete_custom_fields`` -- STUB.



        TODO(accounts-conversion): upstream adds (or removes) a real field named

        ``dimension.fieldname`` on every transaction doctype, and mirrors the

        per-company ``dimension_defaults`` as the field's default. That is

        runtime schema mutation, which has no equivalent until the transaction

        doctypes are converted. Kept as a named no-op called from

        :meth:`create` / :meth:`delete` so the call sites survive and the

        omission is explicit rather than silent.

        """

        return None



    # ── public API ───────────────────────────────────────────────────────────

    def get(

        self, db: Session, business_id: uuid.UUID, dimension_id: uuid.UUID

    ) -> AccountingDimension:

        return self._get_or_404(db, business_id, dimension_id)



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[AccountingDimension]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[AccountingDimension].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )



    def list_enabled(self, db: Session, business_id: uuid.UUID) -> list[AccountingDimension]:

        """The active dimensions a transaction form would render."""

        return self.repository.list_enabled(db, business_id)



    def create(

        self, db: Session, business_id: uuid.UUID, payload: AccountingDimensionCreate

    ) -> AccountingDimension:

        label = payload.label.strip()

        if not label:

            raise DomainValidationError(

                "Label is mandatory", code="accounting_dimension_label_mandatory"

            )



        fieldname = (payload.fieldname or "").strip() or make_fieldname(label)

        if not fieldname:

            raise DomainValidationError(

                "Could not derive a fieldname from this label",

                code="accounting_dimension_fieldname_invalid",

            )



        self._assert_label_free(db, business_id, label)

        self._assert_fieldname_free(db, business_id, fieldname)



        row = AccountingDimension(

            business_id=business_id,

            name=label,

            label=label,

            fieldname=fieldname,

            document_type=payload.document_type,

            disabled=payload.disabled,

        )

        for idx, detail in enumerate(payload.dimension_defaults, start=1):

            row.dimension_defaults.append(

                AccountingDimensionDetail(

                    business_id=business_id,

                    idx=idx,

                    company=detail.company,

                    reference_document=detail.reference_document,

                    default_dimension=detail.default_dimension,

                    mandatory_for_bs=detail.mandatory_for_bs,

                    mandatory_for_pl=detail.mandatory_for_pl,

                    automatically_post_balancing_accounting_entry=(

                        detail.automatically_post_balancing_accounting_entry

                    ),

                    offsetting_account_id=detail.offsetting_account_id,

                )

            )



        try:

            self.repository.add(db, row)

            self.sync_custom_fields(db, business_id, row)

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

        dimension_id: uuid.UUID,

        payload: AccountingDimensionUpdate,

    ) -> AccountingDimension:

        row = self._get_or_404(db, business_id, dimension_id)

        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        try:

            if "label" in changes:

                new_label = (changes["label"] or "").strip()

                if not new_label:

                    raise DomainValidationError(

                        "Label is mandatory", code="accounting_dimension_label_mandatory"

                    )

                self._assert_label_free(db, business_id, new_label, exclude_id=row.id)

                row.label = new_label

                row.name = new_label

                # The fieldname is deliberately NOT rederived here. Upstream's

                # controller never touches it on rename -- the JS re-scrubs the

                # label client-side, and the stored fieldname is whatever the

                # user last set. There is no "was this derived or pinned" flag

                # on the model, so rederiving would silently overwrite a

                # hand-chosen fieldname. Send `fieldname` in the same PATCH to

                # change it.



            if "fieldname" in changes:

                new_fieldname = (changes["fieldname"] or "").strip() or make_fieldname(row.label)

                row.fieldname = new_fieldname



            if "disabled" in changes:

                row.disabled = changes["disabled"]



            self._assert_fieldname_free(db, business_id, row.fieldname, exclude_id=row.id)



            if "dimension_defaults" in changes:

                row.dimension_defaults.clear()

                for idx, detail in enumerate(changes["dimension_defaults"] or [], start=1):

                    row.dimension_defaults.append(

                        AccountingDimensionDetail(

                            business_id=business_id,

                            idx=idx,

                            company=detail.get("company"),

                            reference_document=detail.get("reference_document"),

                            default_dimension=detail.get("default_dimension"),

                            mandatory_for_bs=bool(detail.get("mandatory_for_bs")),

                            mandatory_for_pl=bool(detail.get("mandatory_for_pl")),

                            automatically_post_balancing_accounting_entry=bool(

                                detail.get("automatically_post_balancing_accounting_entry")

                            ),

                            offsetting_account_id=detail.get("offsetting_account_id"),

                        )

                    )



            self.sync_custom_fields(db, business_id, row)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row



    def delete(

        self, db: Session, business_id: uuid.UUID, dimension_id: uuid.UUID

    ) -> None:

        row = self._get_or_404(db, business_id, dimension_id)



        try:

            self.sync_custom_fields(db, business_id, row, removing=True)

            self.repository.delete(db, row)

        except Exception:

            db.rollback()

            raise



        db.commit()
