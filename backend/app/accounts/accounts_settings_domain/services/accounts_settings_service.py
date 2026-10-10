"""

Business logic for Accounts Settings -- port of

``erpnext/accounts/doctype/accounts_settings/accounts_settings.py``.



**A Frappe Single.** Upstream there is exactly one ``Accounts Settings`` document

per site; here there is exactly one row per ``business_id``, materialised with

upstream's defaults the first time it is read. That is why this service has

``get_or_create`` and ``update`` and nothing else -- no list, no delete, no

create-from-payload.



Ported from ``validate()``

--------------------------

``validate_auto_tax_settings``              -> the two "automatically add taxes"

                                               switches are mutually exclusive

``validate_stale_days``                     -> stale days must start at 1

``validate_and_sync_auto_reconcile_config`` -> cron interval 1..59, queue size

                                               5..100



Upstream gates the two reconcile-config checks behind ``has_value_changed``, so

an out-of-range value already in the database is not re-litigated when you edit

something else. That is preserved: :meth:`_validate_reconcile_config` compares

against the stored row and only checks fields that actually moved.



Not ported

----------

Everything in ``validate()`` that writes Frappe *desk metadata* rather than

application state: ``enable_payment_schedule_in_print``,

``toggle_accounting_dimension_sections``, ``toggle_sales_discount_section``,

``toggle_loyalty_point_program_section``, ``toggle_subscription_sections``,

``toggle_overdue_billing_threshold_field``,

``set_allow_on_submit_for_dimension_fields``,

``update_property_for_accounting_dimension``, plus the

``frappe.db.set_default`` and ``frappe.clear_cache`` calls. These create

``Property Setter`` rows and flip Custom Field flags -- machinery this conversion

does not have. The switches themselves are stored and readable; only their

desk-side effects are absent.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import inspect as sa_inspect

from sqlalchemy.orm import Session



from app.accounts.accounts_settings_domain.models.accounts_settings import (

    AccountsSettings,

)

from app.accounts.accounts_settings_domain.repositories.accounts_settings_repository import (

    AccountsSettingsRepository,

)

from app.accounts.accounts_settings_domain.schemas.accounts_settings import (

    AccountsSettingsUpdate,

)

from app.core.errors import DomainValidationError



__all__ = ["AccountsSettingsService"]



#: Bounds from ``validate_and_sync_auto_reconcile_config``. Upstream accepts

#: ``> 0 and < 60`` for the interval, i.e. 1..59 minutes.

AUTO_RECONCILE_TRIGGER_MIN = 1

AUTO_RECONCILE_TRIGGER_MAX = 59

RECONCILIATION_QUEUE_MIN = 5

RECONCILIATION_QUEUE_MAX = 100





class AccountsSettingsService:

    def __init__(

        self, repository: Optional[AccountsSettingsRepository] = None

    ) -> None:

        self.repository = repository or AccountsSettingsRepository()



    # ── ported validators ────────────────────────────────────────────────────

    @staticmethod

    def _validate_auto_tax_settings(row: AccountsSettings) -> None:

        """

        Port of ``validate_auto_tax_settings``.



        Taxes may be derived from the Item Tax Template *or* from the Taxes and

        Charges Template, never both -- otherwise the same tax is added twice.

        """

        if row.add_taxes_from_item_tax_template and row.add_taxes_from_taxes_and_charges_template:

            raise DomainValidationError(

                "You cannot enable both the settings 'Automatically add Taxes and "

                "Charges from Item Tax Template' and 'Automatically add taxes from "

                "Taxes and Charges Template'.",

                code="accounts_settings_auto_tax_conflict",

            )



    @staticmethod

    def _validate_stale_days(row: AccountsSettings) -> None:

        """

        Port of ``validate_stale_days``.



        Upstream raises via ``frappe.msgprint(..., raise_exception=1)``, which is

        an exception despite the ``msgprint`` name -- so it maps to a 400 like

        the rest.



        Only checked when stale rates are disallowed: with ``allow_stale`` on,

        the day count is unused.

        """

        if not row.allow_stale and (row.stale_days or 0) <= 0:

            raise DomainValidationError(

                "Stale Days should start from 1.",

                code="accounts_settings_stale_days",

            )



    @staticmethod

    def _validate_reconcile_config(

        row: AccountsSettings, previous: Optional[dict[str, object]]

    ) -> None:

        """

        Port of ``validate_and_sync_auto_reconcile_config``.



        Upstream only validates a field when it has actually changed, so a bad

        value that is already stored is not re-raised while you edit something

        else. ``previous`` is a snapshot of every column value before this write;

        on first materialisation there is none, so every field counts as changed.



        The snapshot has to be *complete*. An earlier version copied only the

        fields present in the patch, which left the untouched ones holding the

        fresh-object defaults -- so patching ``stale_days`` made an unrelated,

        unchanged ``reconciliation_queue_size`` look like it had moved, and the

        range check fired on a field nobody had touched.



        The ``sync_auto_reconcile_config`` call upstream makes (which rewrites a

        scheduler event) is not ported -- this conversion has no scheduler.

        """

        def changed(field: str) -> bool:

            return previous is None or previous.get(field) != getattr(row, field)



        if changed("auto_reconciliation_job_trigger"):

            trigger = row.auto_reconciliation_job_trigger or 0

            if not AUTO_RECONCILE_TRIGGER_MIN <= trigger <= AUTO_RECONCILE_TRIGGER_MAX:

                raise DomainValidationError(

                    "Cron Interval should be between 1 and 59 Min",

                    code="accounts_settings_cron_interval",

                )



        if changed("reconciliation_queue_size"):

            size = row.reconciliation_queue_size or 0

            if not RECONCILIATION_QUEUE_MIN <= size <= RECONCILIATION_QUEUE_MAX:

                raise DomainValidationError(

                    "Queue Size should be between 5 and 100",

                    code="accounts_settings_queue_size",

                )



    def _validate(

        self, row: AccountsSettings, previous: Optional[dict[str, object]]

    ) -> None:

        # Upstream order preserved.

        self._validate_auto_tax_settings(row)

        self._validate_stale_days(row)

        self._validate_reconcile_config(row, previous)



    @staticmethod

    def _snapshot(row: AccountsSettings) -> dict[str, object]:

        """

        Every current column value, keyed by name.



        Taken *before* the patch is applied, because SQLAlchemy mutates the row

        in place and the ``has_value_changed`` semantics need the old values.

        """

        return {

            attr.key: getattr(row, attr.key)

            for attr in sa_inspect(AccountsSettings).mapper.column_attrs

        }



    # ── public API ───────────────────────────────────────────────────────────

    def get_or_create(

        self, db: Session, business_id: uuid.UUID

    ) -> AccountsSettings:

        """

        The tenant's settings row, created with upstream defaults on first read.



        Materialising on read mirrors ``frappe.get_single``, which always returns

        a document. The defaults come from the column definitions, which were

        taken from the upstream doctype JSON.

        """

        row = self.repository.get_for_business(db, business_id)

        if row is not None:

            return row



        row = AccountsSettings(business_id=business_id)

        try:

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

        payload: AccountsSettingsUpdate,

    ) -> AccountsSettings:

        """

        Apply a partial update to the tenant's single settings row.



        ``previous`` is a detached snapshot of the values before this write, so

        the ``has_value_changed`` semantics survive the fact that SQLAlchemy

        mutates the row in place.

        """

        row = self.get_or_create(db, business_id)



        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row



        previous = self._snapshot(row)



        try:

            for field_name, value in changes.items():

                setattr(row, field_name, value)

            db.flush()

            self._validate(row, previous)

        except Exception:

            db.rollback()

            raise



        db.commit()

        db.refresh(row)

        return row
