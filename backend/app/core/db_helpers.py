from __future__ import annotations
from typing import Optional
from sqlalchemy.exc import  IdentifierError
from sqlalchemy.orm import Session
from app.core.errors import ConflictError

def commit_or_conflict(
        db: Session, *, message: str, code: str ="conflict", details: Optional[dict] = None
) -> None:
    """ commit karo, agar duplicate-name error aaye to clean 409 do, raw crah nahi."""
    try: 
        db.commit()
    except IdentifierError as exc :
        db.rollback()
        raise ConflictError(message, code=code, details=details or {}) from exc
    
