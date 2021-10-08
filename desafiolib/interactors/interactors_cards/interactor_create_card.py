from fastapi import HTTPException

from domain.database.settings import UserAlchemyAdapter
from domain.models.card_models import Card
import json


class CreateCardRequestModel:
    def __init__(self, body):
        self.text = body.text
        self.tags = body.tags


class CreateCardResponseModel:
    def __init__(self, card: Card):
        self.card = card

    def __call__(self):
        return self.card.to_json()


class CreateCardInteractor:
    def __init__(self, request: CreateCardRequestModel,
                 adapter: UserAlchemyAdapter):
        self.request = request
        self.adapter = adapter

    def _get_card(self):
        return self.adapter.query(Card). \
            filter(Card.text == self.request.text).first()

    def _check_exist_card(self):
        card = self._get_card()
        if card is not None:
            raise HTTPException(status_code=400,
                                detail="Card already create")

    def _create_card(self):
        card = Card(text=self.request.text,
                    tags=json.dumps(self.request.tags))

        self.adapter.add(card)
        self.adapter.commit()
        self.adapter.refresh(card)

        return card

    def run(self):
        self._check_exist_card()
        card = self._create_card()
        response = CreateCardResponseModel(card)
        return response
