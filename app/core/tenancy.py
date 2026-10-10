"""
Tenancy + auth dependencies shared by every converted ERPNext domain.

This is the "core: db, auth, multi-tenancy" layer. It deliberately does not
reimplement authentication: it wraps the CreditBridge JWT dependency that
already exists (``app.utils.auth_dependency.get_current_business_id``) so there
is exactly one place that decodes a token.

The rule enforced across all converted domains, matching the frozen Lead spec
already in this repo:

    ``business_id`` is derived from the token. It is never accepted from a
    request body, query string or path segment.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Optional

from fastapi import Depends

from app.db.session import get_db
from app.utils.auth_dependency import get_current_business_id

__all__ = [
    "get_db",
    "get_current_business_uuid",
    "get_current_actor_id",
    "CurrentContext",
    "get_current_context",
]


def get_current_business_uuid(business_id: str = Depends(get_current_business_id)) -> uuid.UUID:
    """Resolve the authenticated tenant as a ``UUID`` for use in queries."""
    try:
        return uuid.UUID(business_id)
    except (ValueError, AttributeError, TypeError) as exc:  # pragma: no cover - bad token
        from fastapi import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token contains a malformed business id",
        ) from exc


def get_current_actor_id() -> Optional[uuid.UUID]:
    """
    The acting user, for ``modified_by``-style attribution.

    CreditBridge has business-account JWTs only -- no staff-level identity yet
    (same TODO the Lead domain records). Returns ``None`` until that lands;
    services treat it as nullable so nothing breaks when it does.
    """
    return None


@dataclass(frozen=True)
class CurrentContext:
    """
    The two facts every service call needs, bundled so a router injects one
    dependency instead of two and a service signature stays readable.
    """

    business_id: uuid.UUID
    actor_id: Optional[uuid.UUID] = None


def get_current_context(
    business_id: uuid.UUID = Depends(get_current_business_uuid),
    actor_id: Optional[uuid.UUID] = Depends(get_current_actor_id),
) -> CurrentContext:
    return CurrentContext(business_id=business_id, actor_id=actor_id)