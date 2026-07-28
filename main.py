# ==========================================
# File: ticket_processor/main.py
# ==========================================
"""
Entry point for the command-line processing script[span_23](start_span)[span_23](end_span).
"""
import argparse
import logging
import sys
from .processor import process_tickets

def setup_logging():
    """FR10: Configure logging for meaningful steps[span_24](start_span)[span_24](end_span)."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )

def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting ticket processing script...")

    # FR9: Script runnable from CLI with --input and --output arguments[span_25](start_span)[span_25](end_span)
    parser = argparse.ArgumentParser(description="Process raw ticket CSV into a structured JSON report[span_26](start_span)[span_26](end_span).")
    parser.add_argument("--input", required=True, help="Path to the raw tickets CSV[span_27](start_span)[span_27](end_span)")
    parser.add_argument("--output", required=True, help="Path to save the JSON report[span_28](start_span)[span_28](end_span)")
    args = parser.parse_args()

    # Process tickets
    process_tickets(args.input, args.output)
    logger.info("Processing complete.")

if __name__ == "__main__":
    main()