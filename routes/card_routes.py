from fastapi import APIRouter, Depends

from domain.models import card_models
from domain.database.settings import UserAlchemyAdapter, engine
from interactors.interactors_cards.interactor_create_card import \
    CreateCardResquestModel, CreateCardInteractor
from sqlalchemy.orm import Session

card_models.Base.metadata.create_all(bind=engine)

card = APIRouter()


@card.post("/card")
def create_card(json_body: card_models.Card.Schema,
                      adapter: Session = Depends(UserAlchemyAdapter)):
    request = CreateCardResquestModel(json_body)
    interactor = CreateCardInteractor(request, adapter)

    result = interactor.run()

    return result()


@card.get("/card")
def read_card():
    return {}


@card.delete("/card")
def delete_card():
    return {}


@card.put("/card")
def update_card():
    return {}


@card.get("/card_all")
def all_cards():
    return {}




