"""
Error translation layer -- the FastAPI equivalent of `frappe.throw`.

Throughout the ERPNext source the guard idiom is::

    frappe.throw(_("Account with existing transaction cannot be converted to ledger"))

Frappe turns that into a 417 with the message rendered in the UI. Here the
services raise :class:`DomainValidationError` (a plain Python exception with no
web-framework import, so services stay transport-agnostic and unit-testable)
and the API layer converts it once, centrally, into ``HTTPException(400)``.

Keeping the two halves separate means a service can be exercised by pytest
without a TestClient, and the HTTP mapping lives in exactly one place.
"""

from __future__ import annotations

from typing import Any, Optional

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse


class DomainValidationError(ValueError):
    """
    Raised by service-layer validation. Direct port of ``frappe.throw(...)``.

    ``code`` is a stable machine-readable slug (``account_has_children``) so a
    client can branch on the failure without string-matching the human message.
    """

    def __init__(
        self,
        message: str,
        *,
        code: str = "validation_error",
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}


class NotFoundError(LookupError):
    """Raised when a tenancy-scoped lookup finds nothing -- maps to 404."""

    def __init__(self, resource: str, identifier: Any) -> None:
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} '{identifier}' not found")


class ConflictError(DomainValidationError):
    """
    A uniqueness/integrity clash rather than bad input -- maps to 409.

    Subclasses DomainValidationError so existing handlers catch it, but carries
    its own status code.
    """

    def __init__(self, message: str, *, code: str = "conflict", details: Optional[dict] = None) -> None:
        super().__init__(
            message,
            code=code,
            status_code=status.HTTP_409_CONFLICT,
            details=details,
        )


async def domain_error_handler(request: Request, exc: DomainValidationError) -> JSONResponse:
    """App-level handler wiring DomainValidationError -> JSON HTTP response."""
    return JSONResponse(status_code=exc.status_code, content=_body(exc))


def to_http_exception(exc: DomainValidationError) -> HTTPException:
    """
    Inline conversion for routers that prefer raising over relying on the
    app-level handler (e.g. when the exception crosses a boundary that would
    otherwise swallow it).

    ``detail`` is a dict rather than a bare string so the stable ``code``
    survives the round trip -- clients branch on the code, and a string-only
    detail would force them to match on human-readable message text.
    """
    return HTTPException(status_code=exc.status_code, detail=_body(exc))


def _body(exc: DomainValidationError) -> dict[str, Any]:
    """Single definition of the error payload, shared by both paths above."""
    body: dict[str, Any] = {"message": exc.message, "code": exc.code}
    if exc.details:
        body["details"] = exc.details
    return body