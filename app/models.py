from sqlalchemy import String, Integer, ForeignKey, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base

class Personne(Base):
    __tablename__ = "personnes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(180), unique=True, nullable=False)

    actions: Mapped[list["Action"]] = relationship(back_populates="personne")
    ventes: Mapped[list["Vente"]] = relationship(back_populates="personne")

class Entreprise(Base):
    __tablename__ = "entreprises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    siren: Mapped[str] = mapped_column(String(9), unique=True, nullable=False)
    nom: Mapped[str] = mapped_column(String(180), nullable=False)
    code_postal: Mapped[str] = mapped_column(String(5), nullable=False)

    interlocuteurs: Mapped[list["Interlocuteur"]] = relationship(back_populates="entreprise")
    ventes: Mapped[list["Vente"]] = relationship(back_populates="entreprise")

class Interlocuteur(Base):
    __tablename__ = "interlocuteurs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom: Mapped[str] = mapped_column(String(120), nullable=False)
    entreprise_id: Mapped[int] = mapped_column(ForeignKey("entreprises.id"), nullable=False)

    entreprise: Mapped["Entreprise"] = relationship(back_populates="interlocuteurs")
    actions: Mapped[list["Action"]] = relationship(back_populates="interlocuteur")

class Action(Base):
    __tablename__ = "actions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(40), nullable=False)  # ex: call, email, meeting
    interlocuteur_id: Mapped[int] = mapped_column(ForeignKey("interlocuteurs.id"), nullable=False)
    personne_id: Mapped[int] = mapped_column(ForeignKey("personnes.id"), nullable=False)

    interlocuteur: Mapped["Interlocuteur"] = relationship(back_populates="actions")
    personne: Mapped["Personne"] = relationship(back_populates="actions")

class Vente(Base):
    __tablename__ = "ventes"
    __table_args__ = (
        CheckConstraint("ca >= 0", name="ca_positive"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ca: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    entreprise_id: Mapped[int] = mapped_column(ForeignKey("entreprises.id"), nullable=False)
    personne_id: Mapped[int] = mapped_column(ForeignKey("personnes.id"), nullable=False)

    entreprise: Mapped["Entreprise"] = relationship(back_populates="ventes")
    personne: Mapped["Personne"] = relationship(back_populates="ventes")