"""
Shared infrastructure for the ERPNext-derived domains.

Submodules:

``base_model``   -- declarative base with id / business_id / timestamps
``database``     -- re-export of the session Base and the ``get_db`` dependency
``errors``       -- ``frappe.throw`` -> ``DomainValidationError`` -> HTTP
``pagination``   -- the shared list envelope
``tenancy``      -- business_id / actor dependencies
``tree``         -- adjacency-list replacement for Frappe's NestedSet lft/rgt
"""

from app.core.base_model import Base, TenantModel, new_uuid, tenant_index
from app.core.errors import ConflictError, DomainValidationError, NotFoundError
from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE, Page, ResultPage
from app.core.tenancy import CurrentContext, get_current_business_uuid, get_current_context
from app.core.tree import TreeHelper, TreeNode

__all__ = [
    "Base",
    "TenantModel",
    "new_uuid",
    "tenant_index",
    "DomainValidationError",
    "ConflictError",
    "NotFoundError",
    "Page",
    "ResultPage",
    "DEFAULT_PAGE_SIZE",
    "MAX_PAGE_SIZE",
    "CurrentContext",
    "get_current_business_uuid",
    "get_current_context",
    "TreeHelper",
    "TreeNode",
]