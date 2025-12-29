import random
from faker import Faker
from sqlalchemy.orm import Session
from sqlalchemy import select

from .models import Personne, Entreprise, Interlocuteur, Action, Vente

fake = Faker("fr_FR")

ACTION_TYPES = ["call", "email", "meeting", "demo", "followup"]

def _unique_siren() -> str:
    # 9 chiffres
    return "".join(str(random.randint(0, 9)) for _ in range(9))

def seed(db: Session, n_personnes=20, n_entreprises=50, n_interlocuteurs=120, n_actions=400, n_ventes=120):
    # PERSONNES
    personnes = []
    for _ in range(n_personnes):
        nom = fake.name()
        email = fake.unique.email()
        personnes.append(Personne(nom=nom, email=email))
    db.add_all(personnes)
    db.commit()

    # ENTREPRISES
    entreprises = []
    for _ in range(n_entreprises):
        entreprises.append(
            Entreprise(
                siren=_unique_siren(),
                nom=fake.company(),
                code_postal=fake.postcode()
            )
        )
    db.add_all(entreprises)
    db.commit()

    personnes = db.scalars(select(Personne)).all()
    entreprises = db.scalars(select(Entreprise)).all()

    # INTERLOCUTEURS
    interlocuteurs = []
    for _ in range(n_interlocuteurs):
        ent = random.choice(entreprises)
        interlocuteurs.append(Interlocuteur(nom=fake.name(), entreprise_id=ent.id))
    db.add_all(interlocuteurs)
    db.commit()

    interlocuteurs = db.scalars(select(Interlocuteur)).all()

    # ACTIONS
    actions = []
    for _ in range(n_actions):
        actions.append(
            Action(
                type=random.choice(ACTION_TYPES),
                interlocuteur_id=random.choice(interlocuteurs).id,
                personne_id=random.choice(personnes).id
            )
        )
    db.add_all(actions)
    db.commit()

    # VENTES
    ventes = []
    for _ in range(n_ventes):
        ventes.append(
            Vente(
                ca=round(random.uniform(500, 25000), 2),
                entreprise_id=random.choice(entreprises).id,
                personne_id=random.choice(personnes).id
            )
        )
    db.add_all(ventes)
    db.commit()

    return {
        "personnes": n_personnes,
        "entreprises": n_entreprises,
        "interlocuteurs": n_interlocuteurs,
        "actions": n_actions,
        "ventes": n_ventes,
    }