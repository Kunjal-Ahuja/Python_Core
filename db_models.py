from sqlalchemy import Column, String, Float, Integer, Boolean
from .database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    ticket_id = Column(String, primary_key=True, index=True)
    customer_name = Column(String)
    category = Column(String)

    priority_raw = Column(String)
    priority_score = Column(Integer)

    created_at = Column(String)
    sla_hours = Column(Float)

    status = Column(String)
    sla_breached = Column(Boolean)