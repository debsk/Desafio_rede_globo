from fastapi import APIRouter, Request, Depends
from interactors.interactor_create_card import \
    CreateCardResquestModel, CreateCardInteractor
from domain.database.settings import UserAlchemyAdapter
from sqlalchemy.orm import Session

card = APIRouter()


@card.post("/card")
async def create_card(json_body: Request,
                      adapter: Session = Depends(UserAlchemyAdapter)):
    body = await json_body.json()
    request = CreateCardResquestModel(body)
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




