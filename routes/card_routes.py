from fastapi import APIRouter, Request
from interactors.interactor_create_card import CreateCardResquestModel

card = APIRouter()


@card.post("/card")
async def create_card(json_body: Request):
    body = await json_body.json()
    request = CreateCardResquestModel(body)
    
    return {} #objeto_vazio


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




