from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, models, auth
from ..database import get_db

router = APIRouter()

@router.post("/register", response_model=schemas.Token)
async def register(payload: schemas.TenantCreate, db: AsyncSession = Depends(get_db)):
    stmt = select(models.Tenant).where(models.Tenant.email == payload.email)
    result = await db.execute(stmt)
    existing = result.scalars().first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = auth.hash_password(payload.password)
    new_tenant = models.Tenant(
        email=payload.email,
        password_hash=hashed_pw,
        client_policy_api_endpoint=payload.client_policy_api_endpoint
    )

    db.add(new_tenant)
    await db.commit()
    await db.refresh(new_tenant)

    token = auth.create_access_token({"sub": str(new_tenant.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # OAuth2PasswordRequestForm provides 'username' and 'password'
    stmt = select(models.Tenant).where(models.Tenant.email == form_data.username)
    result = await db.execute(stmt)
    tenant = result.scalars().first()

    if not tenant or not auth.verify_password(form_data.password, tenant.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = auth.create_access_token({"sub": str(tenant.id)})
    return {"access_token": token, "token_type": "bearer"}
