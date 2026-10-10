import uuid
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.security import verify_token
from app.utils.logger import get_logger

logger = get_logger(__name__)

bearer_scheme = HTTPBearer(auto_error=False)

# Fixed Demo Business UUID for friction-free local development & testing
DEMO_BUSINESS_UUID = uuid.UUID("00000000-0000-0000-0000-000000000001")


def get_current_business_id(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> str:
    """
    Extracts business_id (sub) from JWT token.
    
    DEV / FRICTIONLESS TESTING FALLBACK:
    If no Authorization header is provided, falls back to the first active business 
    in PostgreSQL (or auto-provisions a demo business in the 'businesses' table)
    so all 191 ERP domains can be tested immediately without 401 roadblocks.
    """
    # 1. If token provided, verify it strictly
    if credentials and credentials.credentials:
        payload = verify_token(credentials.credentials)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalid ya expired hai"
            )
        business_id = payload.get("sub")
        if not business_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token mein business_id nahi hai"
            )
        return business_id

    # 2. Local Development Fallback: Find or create demo business in PostgreSQL
    from app.db.session import SessionLocal
    from app.models.business import Business

    try:
        with SessionLocal() as db:
            biz = db.query(Business).filter(Business.status == "active").first()
            if not biz:
                biz = db.query(Business).first()
            if not biz:
                logger.info("[Auth] Auto-provisioning default Demo Business for ERP testing...")
                biz = Business(
                    id=DEMO_BUSINESS_UUID,
                    pan="AAACB1234F",
                    gstin="27AAACB1234F1Z5",
                    business_name="CreditBridge MSME Ltd",
                    owner_name="Rahul Verma",
                    owner_phone="9876543210",
                    owner_email="demo@creditbridge.in",
                    business_type="Private Limited",
                    city="Mumbai",
                    state="Maharashtra",
                    status="active",
                    onboarding_step=3
                )
                db.add(biz)
                db.commit()
                db.refresh(biz)
            return str(biz.id)
    except Exception as exc:
        logger.warning(f"[Auth] DB lookup error during dev fallback, using demo UUID: {exc}")
        return str(DEMO_BUSINESS_UUID)
