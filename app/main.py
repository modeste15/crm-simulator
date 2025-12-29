from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from .db import Base, engine, get_db
from .seed import seed

app = FastAPI(title="CRM Data Simulator")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok"}

@app.post("/seed")
def seed_data(
    n_personnes: int = 20,
    n_entreprises: int = 50,
    n_interlocuteurs: int = 120,
    n_actions: int = 400,
    n_ventes: int = 120,
    db: Session = Depends(get_db),
):
    return seed(
        db,
        n_personnes=n_personnes,
        n_entreprises=n_entreprises,
        n_interlocuteurs=n_interlocuteurs,
        n_actions=n_actions,
        n_ventes=n_ventes
    )

@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    users = db.execute(text("SELECT * FROM personnes")).fetchall()
    return {"users": [dict(user) for user in users]}
