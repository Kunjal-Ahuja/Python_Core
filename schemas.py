from pydantic import BaseModel
from typing import Optional

class TicketBase(BaseModel):
    ticket_id: str
    customer_name: str
    category: str
    priority_raw: str
    created_at: str
    sla_hours: float
    status: str

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    priority_raw: Optional[str] = None

class TicketResponse(TicketBase):
    priority_score: int
    sla_breached: bool

    class Config:
        from_attributes = True