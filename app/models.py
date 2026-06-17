from sqlalchemy import Column, Integer, String, ForeignKey, Text
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    description = Column(Text, nullable=False)

    status = Column(String, default="Open")

    created_by = Column(
        Integer,
        ForeignKey("users.id")
    )

    assigned_to = Column(
    Integer,
    nullable=True
    )


    engineer_name = Column(
    String,
    nullable=True
    )


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)

    comment = Column(Text, nullable=False)

    ticket_id = Column(
        Integer,
        ForeignKey("tickets.id")
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )
