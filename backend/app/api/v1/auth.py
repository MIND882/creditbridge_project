from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.db.session import get_db
from app.models.business import Business
from app.services.kyc_service import verify_pan_comprehensive, verify_gstin
from app.utils.security import create_access_token, create_refresh_token
import uuid

router = APIRouter()

# --- Schemas ---
class RegisterRequest(BaseModel):
    pan: str
    gstin: Optional[str] = None
    business_name: str
    owner_name: str
    owner_phone: str
    owner_email: Optional[str] = None
    business_type: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None

class LoginRequest(BaseModel):
    owner_phone: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    business_id: str

# --- Endpoints ---

@router.post("/register", response_model=TokenResponse)
async def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    """
    Production registration flow:

      1. Reject if PAN is already registered (cheap DB check, no
         external call wasted on a request that's going to fail anyway).
      2. Verify PAN via Surepass (existing kyc_service -- not reimplemented).
      3. If GSTIN was supplied, verify it via Surepass too.
      4. Only after both verifications pass: normalize PAN/GSTIN and
         create the Business row.
      5. Commit once; issue tokens.

    Nothing is written to PostgreSQL if either verification fails.
    """

    # ── Step 1: duplicate PAN check (pre-verification, cheap) ──────────────
    existing = db.query(Business).filter(Business.pan == payload.pan.upper().strip()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Business with this PAN already registered"
        )

    # ── Step 2: verify PAN via existing Surepass integration ───────────────
    pan_result = await verify_pan_comprehensive(payload.pan)
    if not pan_result.get("verified"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=pan_result.get("error") or "PAN verification failed"
        )

    # ── Step 3: verify GSTIN via existing Surepass integration (conditional) ─
    gstin_result = None
    if payload.gstin:
        gstin_result = await verify_gstin(payload.gstin)
        if not gstin_result.get("verified"):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=gstin_result.get("error") or "GSTIN verification failed"
            )

    # ── Step 4: normalize verified values ───────────────────────────────────
    normalized_pan = payload.pan.upper().strip()
    normalized_gstin = payload.gstin.upper().strip() if payload.gstin else None

    # ── Step 5: create Business -- only reachable after both checks pass ────
    business = Business(
        pan=normalized_pan,
        gstin=normalized_gstin,
        business_name=payload.business_name,
        owner_name=payload.owner_name,
        owner_phone=payload.owner_phone,
        owner_email=payload.owner_email,
        business_type=payload.business_type,
        city=payload.city,
        state=payload.state,
        status="active",
        onboarding_step=1
    )
    db.add(business)

    try:
        db.commit()
    except IntegrityError:
        # Covers races (e.g. duplicate GSTIN inserted concurrently between
        # our pre-check and this commit) via the existing unique constraints
        # on Business.pan / Business.gstin -- surfaced as a clean 409
        # instead of a raw DB traceback.
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A business with this PAN or GSTIN already exists"
        )

    db.refresh(business)

    # ── Step 6: issue tokens ────────────────────────────────────────────────
    token_data = {"sub": str(business.id), "phone": business.owner_phone}
    return TokenResponse(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data),
        business_id=str(business.id)
    )


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    business = db.query(Business).filter(
        Business.owner_phone == payload.owner_phone
    ).first()

    if not business:
        # Auto-provision demo business for development so login immediately succeeds
        business = Business(
            pan="AAACB1234F",
            gstin="27AAACB1234F1Z5",
            business_name="CreditBridge MSME Ltd",
            owner_name="Rahul Verma",
            owner_phone=payload.owner_phone,
            owner_email="demo@creditbridge.in",
            business_type="Private Limited",
            city="Mumbai",
            state="Maharashtra",
            status="active",
            onboarding_step=3
        )
        db.add(business)
        db.commit()
        db.refresh(business)

    token_data = {"sub": str(business.id), "phone": business.owner_phone}
    return TokenResponse(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data),
        business_id=str(business.id)
    )


@router.get("/me")
def get_me(db: Session = Depends(get_db)):
    # Placeholder — will add JWT auth dependency next
    return {"message": "authenticated endpoint - coming next"}