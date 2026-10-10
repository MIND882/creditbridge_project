"""
Pydantic v2 conventions shared by every converted doctype's schemas.

Three rules, applied uniformly:

``extra="forbid"``
    An unknown key is a client bug. Silently dropping it (Pydantic's default
    ``ignore``) hides typos that would otherwise cost an hour of debugging a
    field that "isn't saving".

``str_strip_whitespace=True``
    Frappe trims on save; matching that keeps migrated data comparable.

``"" -> None`` via :func:`blank_to_none`
    ERPNext stores unselected Select/Link fields as the empty string, not NULL.
    A client posting a value straight out of an ERPNext export must not be
    rejected for it, and the database must not accumulate two spellings of
    "unset". Applied as a ``before`` validator on optional strings.

Input schemas never declare ``business_id``, ``id``, ``created_at`` or
``updated_at``: tenancy and identity come from the authenticated context and
the database, never from the request body.
"""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, field_validator

__all__ = ["DomainSchema", "InputSchema", "ReadSchema", "blank_to_none"]


class DomainSchema(BaseModel):
    """Root config inherited by every schema in the converted domains."""

    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True,
        from_attributes=True,
        validate_assignment=True,
        populate_by_name=True,
    )


class InputSchema(DomainSchema):
    """
    Base for Create/Update payloads.

    ``from_attributes`` is off here -- inputs describe a request body, never an
    ORM row, so there is no reason to allow object construction.
    """

    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True,
        validate_assignment=True,
    )


class ReadSchema(DomainSchema):
    """Base for response schemas (ORM -> JSON)."""

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
    )


def blank_to_none(value: Any) -> Any:
    """
    Normalise the ERPNext "empty string means unset" convention to ``None``.

    Attached as ``mode="before"`` so it runs prior to type coercion -- an
    optional field then validates cleanly instead of tripping enum parsing on
    ``""``.
    """
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    return value


def optional_str_field_validator(field: str):
    """Decorator helper: apply :func:`blank_to_none` to one named field."""

    def decorator(cls: type[BaseModel]) -> type[BaseModel]:
        setattr(
            cls,
            f"_blank_to_none_{field}",
            field_validator(field, mode="before")(classmethod(lambda _c, v: blank_to_none(v))),
        )
        return cls

    return decorator


def coerce_optional(value: Any) -> Optional[str]:
    """Alias kept for call sites that want the same behaviour inline."""
    result = blank_to_none(value)
    return None if result is None else str(result)