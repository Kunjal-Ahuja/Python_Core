# ==========================================
# File: ticket_processor/processor.py
# ==========================================
"""
Core classification and report building logic[span_14](start_span)[span_14](end_span).
"""
import csv
import json
import logging
import sys
from datetime import datetime, timedelta
from .config import PRIORITY_MAPPING, MAX_INVALID_RATIO, DATE_FORMAT
from .validators import validate_row
from .models import Ticket

logger = logging.getLogger(__name__)

def process_tickets(input_path: str, output_path: str):
    """
    Reads the CSV, validates, classifies, and writes the JSON report[span_15](start_span)[span_15](end_span).
    """
    valid_tickets = []
    invalid_rows = []
    category_counts = {}
    breached_count = 0
    total_rows = 0
    
    # FR1: Read the raw tickets CSV[span_16](start_span)[span_16](end_span)
    try:
        with open(input_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                total_rows += 1
                
                # FR2, FR3: Validate and collect invalid rows separately[span_17](start_span)[span_17](end_span)
                is_valid, reason = validate_row(row)
                if not is_valid:
                    invalid_rows.append({
                        "raw_row": ",".join(str(v) for v in row.values()), 
                        "reason": reason
                    })
                    continue
                
                # Parsing valid data
                created_at_dt = datetime.strptime(row["created_at"].strip(), DATE_FORMAT)
                sla_hours = float(row["sla_hours"])
                status = row["status"].strip().lower()
                
                # FR4: Compute SLA breach (created_at + sla_hours < now AND status != closed)[span_18](start_span)[span_18](end_span)
                deadline = created_at_dt + timedelta(hours=sla_hours)
                is_breached = (deadline < datetime.now()) and (status != "closed")
                if is_breached:
                    breached_count += 1
                
                # FR5: Assign priority score[span_19](start_span)[span_19](end_span)
                priority_raw = row["priority_raw"].strip().lower()
                priority_score = PRIORITY_MAPPING[priority_raw]
                
                category = row["category"].strip()
                category_counts[category] = category_counts.get(category, 0) + 1
                
                ticket = Ticket(
                    ticket_id=row["ticket_id"].strip(),
                    customer_name=row["customer_name"].strip(),
                    category=category,
                    priority_raw=priority_raw,
                    priority_score=priority_score,
                    created_at=created_at_dt.isoformat(),
                    sla_hours=sla_hours,
                    status=status,
                    sla_breached=is_breached
                )
                valid_tickets.append(ticket.to_dict())
                
    except FileNotFoundError:
        logger.error(f"Input file not found: {input_path}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error reading CSV: {e}")
        sys.exit(1)

    logger.info(f"Processed {total_rows} total rows. Valid: {len(valid_tickets)}, Invalid: {len(invalid_rows)}")

    # FR7: Abort entirely if invalid-row ratio exceeds 10%[span_20](start_span)[span_20](end_span)
    if total_rows > 0:
        invalid_ratio = len(invalid_rows) / total_rows
        if invalid_ratio > MAX_INVALID_RATIO:
            logger.error(f"Abort: Invalid row ratio ({invalid_ratio:.1%}) exceeds threshold ({MAX_INVALID_RATIO:.1%})[span_21](start_span)[span_21](end_span)")
            sys.exit(1)

    # FR6, FR8: Compute summary counts and write structured JSON report[span_22](start_span)[span_22](end_span)
    report = {
        "generated_at": datetime.now().isoformat(),
        "summary": {
            "total_rows": total_rows,
            "valid_tickets": len(valid_tickets),
            "invalid_rows": len(invalid_rows),
            "breached_count": breached_count,
            "by_category": category_counts
        },
        "tickets": valid_tickets,
        "invalid_rows": invalid_rows
    }

    try:
        with open(output_path, mode='w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        logger.info(f"Successfully wrote report to {output_path}")
    except Exception as e:
        logger.error(f"Failed to write output JSON: {e}")
        sys.exit(1)

