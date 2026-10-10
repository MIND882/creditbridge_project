# RE-EXPORT

"""

Closed Document -- converted from ``erpnext/accounts/doctype/closed_document``.



A Frappe child table (``istable: 1``) recording which document types are locked

inside an Accounting Period.



**This module re-exports a model defined elsewhere, and that is deliberate.**

``ClosedDocument`` was written inline in

``app.accounts.accounting_period_domain.models.accounting_period`` in an earlier

batch, complete with its parent foreign key and ``idx``. Declaring a second

class with the same ``__tablename__`` here raises

``InvalidRequestError: Table 'closed_documents' is already defined for this

MetaData instance`` -- there can only be one mapping per table.



Re-exporting keeps a single table definition while still giving this doctype its

own domain package and read-only API, consistent with every other child table.

The ``# RE-EXPORT`` marker on line 1 stops the generator from overwriting this

file with a second mapping.

"""



from __future__ import annotations



from app.accounts.accounting_period_domain.models.accounting_period import (

    ClosedDocument,

)



__all__ = ["ClosedDocument"]
