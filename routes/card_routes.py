from fastapi import APIRouter

card = APIRouter()


@card.post("/card")
def create_card():
    return {}


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




