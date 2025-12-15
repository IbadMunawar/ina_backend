from pydantic import BaseModel, EmailStr

class TenantCreate(BaseModel):
    email: EmailStr
    password: str
    client_policy_api_endpoint: str | None = None

class TenantOut(BaseModel):
    id: int
    email: EmailStr
    client_policy_api_endpoint: str | None

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class AuthResponse(Token):
    tenant_id: int
    api_key: str | None = None


class TenantConfigIn(BaseModel):
    client_policy_api_endpoint: str

class TenantConfigOut(BaseModel):
    client_policy_api_endpoint: str | None
    client_api_key: str | None


class TenantRuleInput(BaseModel):
    mam: float
    asking_price: float



class SessionInitRequest(BaseModel):
    api_key: str           # The Tenant's authentication key (from Week 2)
    context_id: str        # The Tenant's internal ID for this user/chat
    mam: float             # Minimum Acceptable Margin
    asking_price: float    # The starting price

class SessionInitResponse(BaseModel):
    session_id: str        # We return our generated Session ID
    status: str