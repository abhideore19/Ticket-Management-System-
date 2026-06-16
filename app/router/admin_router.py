from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models import Ticket
from app.schemas import AssignTicket, StatusUpdate
from app.dependencies import get_current_user

router = APIRouter()


# Admin Dashboard
@router.get("/dashboard")
def admin_dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    total_tickets = db.query(Ticket).count()

    open_tickets = db.query(Ticket).filter(
        Ticket.status == "Open"
    ).count()

    return {
        "total_tickets": total_tickets,
        "open_tickets": open_tickets
    }


# Assign Ticket
@router.put("/assign/{ticket_id}")
def assign_ticket(
    ticket_id: int,
    data: AssignTicket,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    ticket.assigned_to = data.assigned_to

    db.commit()
    db.refresh(ticket)

    return {
        "message": "Ticket assigned successfully",
        "ticket_id": ticket.id
    }


# Change Status
@router.put("/status/{ticket_id}")
def change_status(
    ticket_id: int,
    data: StatusUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    ticket.status = data.status

    db.commit()
    db.refresh(ticket)

    return {
        "message": "Status updated successfully",
        "status": ticket.status
    }


# Search Tickets
@router.get("/search")
def search_tickets(
    keyword: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    tickets = db.query(Ticket).filter(
        or_(
            Ticket.title.ilike(f"%{keyword}%"),
            Ticket.description.ilike(f"%{keyword}%")
        )
    ).all()

    return tickets