# ==========================================
# File: ticket_processor/validators.py
# ==========================================
"""
Row validation logic (FR2)[span_8](start_span)[span_8](end_span).
"""
from datetime import datetime
from .config import PRIORITY_MAPPING, DATE_FORMAT

def validate_row(row: dict) -> tuple[bool, str]:
    """
    FR2: Validate every row. Returns (is_valid, error_reason)[span_9](start_span)[span_9](end_span).
    Invalid if:
    - ticket_id is missing[span_10](start_span)[span_10](end_span)
    - sla_hours is not a positive number[span_11](start_span)[span_11](end_span)
    - created_at is not a parseable date[span_12](start_span)[span_12](end_span)
    - priority_raw is not low / medium / high / critical[span_13](start_span)[span_13](end_span)
    """
    if not row.get("ticket_id") or not str(row.get("ticket_id")).strip():
        return False, "missing ticket_id"
    
    try:
        sla_hours = float(row.get("sla_hours", 0))
        if sla_hours <= 0:
            return False, "sla_hours must be a positive number"
    except ValueError:
        return False, "sla_hours is not a number"
        
    try:
        datetime.strptime(row.get("created_at", "").strip(), DATE_FORMAT)
    except ValueError:
        return False, "created_at is not a parseable date"
        
    if row.get("priority_raw") not in PRIORITY_MAPPING:
        return False, "invalid priority_raw"
        
    return True, ""