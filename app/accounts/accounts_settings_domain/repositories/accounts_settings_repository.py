"""

Data access for AccountsSettings. Scoped by ``business_id`` throughout.



A Frappe Single has exactly one document, so the only lookup this repository

needs is "the row for this tenant" -- there is no list, and no lookup by id

independent of the tenant.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import select

from sqlalchemy.orm import Session



from app.accounts.accounts_settings_domain.models.accounts_settings import (

    AccountsSettings,

)



__all__ = ["AccountsSettingsRepository"]





class AccountsSettingsRepository:

    model = AccountsSettings



    def get_for_business(

        self, db: Session, business_id: uuid.UUID

    ) -> Optional[AccountsSettings]:

        return db.scalar(

            select(AccountsSettings).where(

                AccountsSettings.business_id == business_id

            )

        )



    def add(self, db: Session, row: AccountsSettings) -> AccountsSettings:

        db.add(row)

        db.flush()

        return row
