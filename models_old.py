# ==========================================
# File: ticket_api/models.py
# ==========================================

"""
Pydantic models for API request validation.
"""
from pydantic import BaseModel
from typing import Optional

class TicketCreate(BaseModel):
    """Schema for creating a new ticket (FR15)."""
    ticket_id: str
    customer_name: str
    category: str
    priority_raw: str
    created_at: str
    sla_hours: float
    status: str = "open"

class TicketUpdate(BaseModel):
    """Schema for updating an existing ticket (FR16)."""
    status: Optional[str] = None
    priority_raw: Optional[str] = None