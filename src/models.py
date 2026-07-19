import datetime
from sqlalchemy import String, ForeignKey, DateTime, Float, Integer 
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

def get_utc_now():
    return datetime.datetime.now(datetime.timezone.utc)

class Customer(Base):
    __tablename__ = "customers"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False )
    company_name: Mapped[str] = mapped_column(String(255), nullable=True)
    tariff_plan: Mapped[str] = mapped_column(String(50), default="free")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now)
    activities: Mapped[list["CustomerActivityLog"]] = relationship(
        "CustomerActivityLog", back_populates="customer", cascade="all, delete-orphan"
    )
    
    
class CustomerActivityLog(Base):
    __tablename__ = "customer_activity_log"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    
    #type of activity such as "login", "page_view","support_ticker", "payment_success", "payment_failed"
    activity_type: Mapped[str] = mapped_column(String(100), nullable=False)
    value: Mapped[float] = mapped_column(Float, default=0.0)
    
    timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=get_utc_now, index=True
    )
    customer: Mapped["Customer"] = relationship("Customer", back_populates="activities")
    
    