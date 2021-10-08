import json

from domain.database.settings import UserAlchemyAdapter
from domain.models.card_models import Card


class UpdateCardRequestModel:
    def __init__(self, body):
        self.id = body.id
        self.text = body.text
        self.tags = body.tags


class UpdateCardResponseModel:
    def __init__(self, card: Card):
        self.card = card

    def __call__(self):
        return self.card.to_json()


class UpdateCardInteractor:
    def __init__(self, request: UpdateCardRequestModel,
                 adapter: UserAlchemyAdapter):
        self.request = request
        self.adapter = adapter

    def _get_card(self):
        return self.adapter.query(Card). \
            filter(Card.id == self.request.id).first()

    def _update_card(self, card: Card):
        card.text = self.request.text
        card.tags = json.dumps(self.request.tags)

        self.adapter.commit()

        return card

    def run(self):
        card = self._get_card()
        self._update_card(card)
        response = UpdateCardResponseModel(card)
        return response


