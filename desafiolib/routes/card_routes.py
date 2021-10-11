from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from domain.models.card_models import Card
from domain.models import card_models
from domain.database.settings import UserAlchemyAdapter, engine

from desafiolib.interactors.interactors_cards.interactor_create_card import \
    CreateCardRequestModel, CreateCardInteractor
from desafiolib.interactors.interactors_cards.interactor_read_card import \
    ReadCardRequestModel, ReadCardInteractor
from desafiolib.interactors.interactors_cards.interactor_remove_card import \
    DeleteCardRequestModel, DeleteCardInteractor
from desafiolib.interactors.interactors_cards.interactor_card_all import \
    AllCardRequestModel, AllCardInteractor
from desafiolib.interactors.interactors_cards.interactor_update_card import \
    UpdateCardRequestModel, UpdateCardInteractor

card_models.Base.metadata.create_all(bind=engine)

card = APIRouter()


@card.post("/card")
def post_create_card(json_body: Card.Schema,
                     adapter: Session = Depends(UserAlchemyAdapter)):
    request = CreateCardRequestModel(json_body)
    interactor = CreateCardInteractor(request, adapter)

    result = interactor.run()

    return result()


@card.get("/card/read/{card_id}")
def get_read_card(card_id,
                  adapter: Session = Depends(UserAlchemyAdapter)):
    request = ReadCardRequestModel(card_id)

    interactor = ReadCardInteractor(request, adapter)

    result = interactor.run()

    return result()


@card.delete("/card/delete/{card_id}")
def delete_card(card_id,
                adapter: Session = Depends(UserAlchemyAdapter)):
    request = DeleteCardRequestModel(card_id)

    interactor = DeleteCardInteractor(request, adapter)

    result = interactor.run()

    return result()


@card.put("/card/update/")
def put_update_card(json_body: Card.Schema,
                    adapter: Session = Depends(UserAlchemyAdapter)):
    request = UpdateCardRequestModel(json_body)

    interactor = UpdateCardInteractor(request, adapter)

    result = interactor.run()

    return result()


@card.get("/card_all/{tag_id}")
def get_all_cards(tag_id,
                  adapter: Session = Depends(UserAlchemyAdapter)):
    request = AllCardRequestModel(tag_id)

    interactor = AllCardInteractor(request, adapter)

    result = interactor.run()

    return result()
