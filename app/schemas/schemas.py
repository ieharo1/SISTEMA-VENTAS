from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SellerBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    region: Optional[str] = None


class SellerCreate(SellerBase):
    pass


class SellerUpdate(SellerBase):
    pass


class Seller(SellerBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SaleBase(BaseModel):
    seller_id: str
    amount: float
    description: Optional[str] = None
    sale_date: datetime


class SaleCreate(SaleBase):
    pass


class Sale(SaleBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


class GoalBase(BaseModel):
    seller_id: str
    month: int
    year: int
    target_amount: float


class GoalCreate(GoalBase):
    pass


class Goal(GoalBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


class GoalWithProgress(Goal):
    achieved_amount: float = 0.0
    percentage: float = 0.0

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class DashboardMetrics(BaseModel):
    total_sales: float
    total_sellers: int
    total_goals: int
    goals_achieved: int
    average_sale: float
    top_sellers: list
