from domain.database.settings import UserAlchemyAdapter
from domain.models.card_models import Card
import json


class CreateCardResquestModel:
    def __init__(self, body):
        self.text = body.text
        self.tags = body.tags


class CreateCardResponseModel:
    def __init__(self, card: Card):
        self.card = card

    def __call__(self):
        return self.card.to_json()


class CreateCardInteractor:
    def __init__(self, request: CreateCardResquestModel,
                 adapter: UserAlchemyAdapter):
        self.request = request
        self.adapter = adapter

    def _create_card(self):
        card = Card(text=self.request.text,
                    tags=json.dumps(self.request.tags))

        return card

    def _save_card(self, card):
        self.adapter.add(card)
        self.adapter.commit()
        self.adapter.refresh(card)

    def run(self):
        card = self._create_card()
        self._save_card(card)
        response = CreateCardResponseModel(card)
        return response
