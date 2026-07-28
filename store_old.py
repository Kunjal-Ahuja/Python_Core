# ==========================================
# File: ticket_api/store.py
# ==========================================
"""
Simple in-memory data store for the MVP (FR18).
"""
import json
import os
import logging

logger = logging.getLogger(__name__)

# In-memory dictionary acting as our "database"
# Key: ticket_id, Value: ticket dict
db = {}

def load_data(filepath: str):
    """FR18: Load data from the JSON report produced by Module 1."""
    global db
    if not os.path.exists(filepath):
        logger.warning(f"Data file not found at {filepath}. Starting with empty in-memory store.")
        return

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            tickets_list = data.get("tickets", [])
            for t in tickets_list:
                db[t["ticket_id"]] = t
        logger.info(f"Successfully loaded {len(db)} tickets into memory.")
    except Exception as e:
        logger.error(f"Error loading JSON data: {e}")

def get_all_tickets() -> list:
    return list(db.values())

def get_ticket(ticket_id: str) -> dict:
    return db.get(ticket_id)

def add_ticket(ticket: dict):
    db[ticket["ticket_id"]] = ticket

def delete_ticket(ticket_id: str) -> bool:
    if ticket_id in db:
        del db[ticket_id]
        return True
    return False
