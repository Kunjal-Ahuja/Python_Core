# ==========================================
# File: ticket_processor/models.py
# ==========================================
"""
Data structures for the ticket processing (NFR2)[span_6](start_span)[span_6](end_span).
"""
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class Ticket:
    """Represents a valid, processed ticket[span_7](start_span)[span_7](end_span)."""
    ticket_id: str
    customer_name: str
    category: str
    priority_raw: str
    priority_score: int
    created_at: str 
    sla_hours: float
    status: str
    sla_breached: bool

    def to_dict(self):
        return asdict(self)
