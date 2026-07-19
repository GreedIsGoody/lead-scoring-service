from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select
from typing import List

from src.database import get_db, engine, Base
from src.models import Customer, CustomerActivityLog
from src.schemas import CustomerCreate, CustomerResponse, ActivityCreate, ActivityResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        
        await conn.run_sync(Base.metadata.create_all)
        
    yield
    
    
    pass



app = FastAPI(
    title="Customer Analytics & Lead Scoring Service",
    description="API for customer scoring and prediction using ML",
    lifespan=lifespan,
    version="1.0.0"
)


@app.get("/", tags=["General"])
async def root():
    return {"message": "Lead Scoring Service is running"}


# Endpoints for working with clients
@app.post("/api/v1/customers", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED, tags=["Customers"])
async def create_customer(customer_data: CustomerCreate, db: AsyncSession = Depends(get_db)):
    
    query = select(Customer).where(Customer.email == customer_data.email)
    result = await db.execute(query)
    existing_customer = result.scalar_one_or_none()
    
    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer with this email already registered"
        )
        
    new_customer = Customer(
        email=customer_data.email,
        company_name=customer_data.company_name,
        tariff_plan=customer_data.tariff_plan
    )
    
    db.add(new_customer)
    await db.commit()
    await db.refresh(new_customer)
    return new_customer

@app.get("/api/v1/customers", response_model=List[CustomerResponse], tags=["Customers"])
async def get_customers(db:AsyncSession = Depends(get_db)):
    query = select(Customer).order_by(Customer.id)
    result = await db.execute(query)
    customers =  result.scalars().all()
    
    return customers


@app.post("/api/v1/activity", response_model=ActivityResponse, status_code=status.HTTP_201_CREATED, tags=["Activities"])
async def log_customer_activity(activity_data: ActivityCreate, db:AsyncSession = Depends(get_db)):
    
    customer_query = select(Customer).where(Customer.id == activity_data.customer_id)
    customer_result = await db.execute(customer_query)
    customer = customer_result.scalar_one_or_none()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with id {activity_data.customer_id} is not found"
        )
        
    new_log = CustomerActivityLog(
        customer_id = activity_data.customer_id,
        activity_type = activity_data.activity_type,
        value = activity_data.value
    )
    
    db.add(new_log)
    await db.commit()
    await db.refresh(new_log)
    return new_log
