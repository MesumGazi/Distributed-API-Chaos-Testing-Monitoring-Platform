from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class HealthCheck(Base):
    __tablename__ = "health_checks"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(500), nullable=False, index=True)
    status_code = Column(Integer, nullable=True)
    response_time = Column(Float, nullable=True)
    is_healthy = Column(Boolean, default=False)
    status_message = Column(String(100), nullable=True)
    error_message = Column(String(1000), nullable=True)
    checked_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<HealthCheck {self.url} - {self.status_code}>"