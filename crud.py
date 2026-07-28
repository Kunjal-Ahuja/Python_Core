from sqlalchemy.orm import Session

from . import db_models


def get_all_tickets(db: Session):
    return db.query(db_models.Ticket).all()


def get_ticket(db: Session, ticket_id: str):
    return (
        db.query(db_models.Ticket)
        .filter(db_models.Ticket.ticket_id == ticket_id)
        .first()
    )


def create_ticket(db: Session, ticket):
    priority_map = {
        "low": 1,
        "medium": 2,
        "high": 3,
        "critical": 4
    }

    db_ticket = db_models.Ticket(
        **ticket.model_dump(),
        priority_score=priority_map[ticket.priority_raw.lower()],
        sla_breached=False
    )

    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)

    return db_ticket


def update_ticket(db: Session, ticket_id: str, ticket_update):
    ticket = get_ticket(db, ticket_id)

    if ticket is None:
        return None

    if ticket_update.status is not None:
        ticket.status = ticket_update.status

    if ticket_update.priority_raw is not None:
        ticket.priority_raw = ticket_update.priority_raw

        priority_map = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4
        }

        ticket.priority_score = priority_map.get(
            ticket_update.priority_raw.lower(),
            ticket.priority_score
        )

    db.commit()
    db.refresh(ticket)

    return ticket


def delete_ticket(db: Session, ticket_id: str):
    ticket = get_ticket(db, ticket_id)

    if ticket is None:
        return None

    db.delete(ticket)
    db.commit()

    return ticket