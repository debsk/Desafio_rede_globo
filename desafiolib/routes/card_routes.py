from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from domain.models.card_models import Card
from domain.models import card_models
from domain.database.settings import UserAlchemyAdapter, engine

from desafiolib.interactors.interactors_cards.interactor_create_card import \
    CreateCardRequestModel, CreateCardInteractor
from desafiolib.interactors.interactors_cards.interactor_read_card import \
    ReadCardRequestModel, ReadCardInteractor

card_models.Base.metadata.create_all(bind=engine)

card = APIRouter()


@card.post("/card")
def post_create_card(json_body: Card.Schema,
                adapter: Session = Depends(UserAlchemyAdapter)):
    request = CreateCardRequestModel(json_body)
    interactor = CreateCardInteractor(request, adapter)

    result = interactor.run()

    return result()


@card.get("/card/{card_id}")
def get_read_card(card_id,
                  adapter: Session = Depends(UserAlchemyAdapter)):
    request = ReadCardRequestModel(card_id)

    interactor = ReadCardInteractor(request, adapter)

    result = interactor.run()

    return result()


@card.delete("/card")
def delete_card():
    return {}


@card.put("/card")
def put_update_card():
    return {}


@card.get("/card_all")
def get_all_cards():
    return {}
