# ==========================================
# File: ticket_processor/config.py
# ==========================================
"""
Constants and configuration to prevent hardcoding (NFR3)[span_2](start_span)[span_2](end_span).
"""

# FR5: Assign a priority score mapping[span_3](start_span)[span_3](end_span)
PRIORITY_MAPPING = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4
}

# FR7: Abort threshold if invalid-row ratio exceeds 10%[span_4](start_span)[span_4](end_span)
MAX_INVALID_RATIO = 0.10

# Expected date format based on sample data[span_5](start_span)[span_5](end_span)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"