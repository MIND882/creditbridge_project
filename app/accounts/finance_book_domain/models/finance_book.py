"""

Finance Book -- converted from ``erpnext/accounts/doctype/finance_book``.



A single-field lookup doctype. ``autoname`` is ``field:finance_book_name``, so the label

*is* the identity upstream; here it is a unique column and ``id`` is the key.

"""



from __future__ import annotations



from sqlalchemy import String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["FinanceBook"]





class FinanceBook(TenantModel):

    """One row of the Finance Book lookup."""



    __tablename__ = "finance_books"

    __table_args__ = (

        UniqueConstraint("business_id", "finance_book_name", name="uq_finance_books_business_id_finance_book_name"),

    )



    #: ``autoname: field:finance_book_name`` upstream -- the label is the document name.

    name: Mapped[str] = mapped_column(String(140), nullable=False)

    finance_book_name: Mapped[str] = mapped_column(String(140), nullable=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<FinanceBook id={self.id} {self.finance_book_name!r}>"
