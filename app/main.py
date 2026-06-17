from fastapi import FastAPI

from database import Base, engine

from router.auth_router import router as auth_router
from router.ticket_router import router as ticket_router
from router.admin_router import router as admin_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ticket Management System")

app.include_router(auth_router)
app.include_router(ticket_router, prefix="/tickets", tags=["Tickets"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])


@app.get("/")
def home():
    return {"message": "Ticket Management API Running"}
