from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


#Customer activity schema
class ActivityCreate(BaseModel):
    customer_id: int
    activity_type: str
    value: float = 0.0
    
class ActivityResponse(ActivityCreate):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True
        
class CustomerCreate(BaseModel):
    email: EmailStr
    company_name: Optional[str] = None
    tariff_plan: str = "free"
    
    
class CustomerResponse(BaseModel):
    id: int
    email: EmailStr
    company_name: Optional[str]
    tariff_plan: str
    created_at: datetime    
    
    class Config:
        from_attributes = True
        
        
class ScoringResponse(BaseModel):
    customer_id: int
    churn_probability: float
    risk_level: str