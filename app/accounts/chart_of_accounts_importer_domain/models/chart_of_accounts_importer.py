"""

Chart Of Accounts Importer -- converted from ``erpnext/accounts/doctype/chart_of_accounts_importer``.





"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["ChartOfAccountsImporter"]







class ChartOfAccountsImporter(TenantModel):

    __tablename__ = "chart_of_accounts_importers"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_chart_of_accounts_importers_business_name"),

    )



    #: Upstream declares no ``autoname``; Frappe mints a hash.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    import_file: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ChartOfAccountsImporter id={self.id}>"
