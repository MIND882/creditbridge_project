"""

DunningLetterText -- converted from

``erpnext/accounts/doctype/dunning_letter_text``.



One row of ``DunningType.dunning_letter_text``: the letter body for a single

language, plus the flag marking which language is the fallback.



Rows only ever exist inside a dunning type, so the API is read-only.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import Boolean, ForeignKey, String, Text

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["DunningLetterText"]





class DunningLetterText(ChildTableModel, TenantModel):

    """One row of ``DunningType.dunning_letter_text``."""



    __tablename__ = "dunning_letter_texts"



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("dunning_types.id", ondelete="CASCADE"), nullable=True, index=True

    )



    #: Language is its own doctype and is not converted.

    language: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    #: Upstream rejects more than one row carrying this flag.

    is_default_language: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    #: ERPNext ``Text Editor`` -- Jinja-templated HTML upstream.

    body_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    closing_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<DunningLetterText id={self.id} language={self.language!r}>"
