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


class TenantConfigIn(BaseModel):
    client_policy_api_endpoint: str

class TenantConfigOut(BaseModel):
    client_policy_api_endpoint: str | None
    client_api_key: str | None


class TenantRuleInput(BaseModel):
    mam: float
    asking_price: float