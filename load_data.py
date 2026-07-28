import json

from sqlalchemy.orm import Session
from . import db_models


def load_json(db: Session, filepath):

    with open(filepath) as f:
        data = json.load(f)

    for t in data["tickets"]:

        exists = (
            db.query(db_models.Ticket)
            .filter_by(ticket_id=t["ticket_id"])
            .first()
        )

        if exists:
            continue

        db.add(db_models.Ticket(**t))

    db.commit()