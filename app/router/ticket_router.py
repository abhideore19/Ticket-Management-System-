from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Ticket, Comment
from app.schemas import (
    TicketCreate,
    TicketUpdate,
    CommentCreate
)

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


@router.post("/")
def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    new_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        created_by=current_user.id
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket


@router.get("/my")
def my_tickets(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    tickets = db.query(Ticket).filter(
        Ticket.created_by == current_user.id
    ).all()

    return tickets


@router.put("/{ticket_id}")
def update_ticket(
    ticket_id: int,
    ticket: TicketUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    db_ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not db_ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    if db_ticket.created_by != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not allowed"
        )

    db_ticket.title = ticket.title
    db_ticket.description = ticket.description

    db.commit()

    return {"message": "Ticket Updated"}


@router.post("/{ticket_id}/comments")
def add_comment(
    ticket_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    new_comment = Comment(
        comment=comment.comment,
        ticket_id=ticket_id,
        user_id=current_user.id
    )

    db.add(new_comment)
    db.commit()

    return {"message": "Comment Added"}


@router.get("/{ticket_id}/comments")
def get_comments(
    ticket_id: int,
    db: Session = Depends(get_db)
):

    comments = db.query(Comment).filter(
        Comment.ticket_id == ticket_id
    ).all()

    return comments


@router.get("/search/")
def search_tickets(
    status: str,
    db: Session = Depends(get_db)
):

    tickets = db.query(Ticket).filter(
        Ticket.status == status
    ).all()

    return tickets