from domain.database.settings import UserAlchemyAdapter
from domain.models.card_models import Card
from fastapi import HTTPException


class ReadCardRequestModel:
    def __init__(self, card_id):
        self.card_id = card_id


class ReadCardResponseModel:
    def __init__(self, card: Card):
        self.card = card

    def __call__(self):
        return self.card


class ReadCardInteractor:
    def __init__(self, request: ReadCardRequestModel,
                 adapter: UserAlchemyAdapter):
        self.request = request
        self.adapter = adapter

    def _get_read_card(self):
        return self.adapter.query(Card). \
            filter(Card.id == self.request.card_id).first()

    def _check_exist_read_card(self):
        card = self._get_read_card()
        if card is None:
            raise HTTPException(status_code=400,
                                detail="Card not exist")

    def run(self):
        card = self._get_read_card()
        self._check_exist_read_card(card)
        response = ReadCardResponseModel(card)
        return response
