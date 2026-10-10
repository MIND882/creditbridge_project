"""

Currency Exchange Settings -- converted from ``erpnext/accounts/doctype/currency_exchange_settings``.





"""



from __future__ import annotations



import enum

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.currency_exchange_settings_details_domain.models.currency_exchange_settings_details import CurrencyExchangeSettingsDetails

from app.accounts.currency_exchange_settings_result_domain.models.currency_exchange_settings_result import CurrencyExchangeSettingsResult



from app.core.base_model import TenantModel



__all__ = ["CurrencyExchangeSettings", "CurrencyExchangeSettingsServiceProvider"]







class CurrencyExchangeSettingsServiceProvider(str, enum.Enum):

    FRANKFURTER_DEV = "frankfurter.dev"

    EXCHANGERATE_HOST = "exchangerate.host"

    FRANKFURTER_DEV_V2 = "frankfurter.dev - v2"

    CUSTOM = "Custom"









class CurrencyExchangeSettings(TenantModel):

    __tablename__ = "currency_exchange_settings"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_currency_exchange_settings_business_name"),

    )



    #: Upstream declares no ``autoname``; Frappe mints a hash.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    api_endpoint: Mapped[str] = mapped_column(String(140), nullable=False)

    url: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    service_provider: Mapped[CurrencyExchangeSettingsServiceProvider] = mapped_column(

        SAEnum(CurrencyExchangeSettingsServiceProvider, native_enum=False, length=20, validate_strings=True),

        nullable=False,

    )

    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    access_key: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    use_http: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)



    req_params = relationship(

        CurrencyExchangeSettingsDetails,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=CurrencyExchangeSettingsDetails.idx,

        passive_deletes=True,

    )

    result_key = relationship(

        CurrencyExchangeSettingsResult,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=CurrencyExchangeSettingsResult.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<CurrencyExchangeSettings id={self.id}>"
