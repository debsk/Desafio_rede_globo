from domain.database.settings import UserAlchemyAdapter
from domain.models.card_models import Card


class CreateCardResquestModel:
    def __init__(self, body):
        self.id = body["id"]
        self.text = body["text"]
        self.date_create = body["date_create"]
        self.date_update = body["date_update"]
        self.tags = body["tags"]


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
        card = Card(id=self.request.id,
                    text=self.request.text,
                    date_create=self.request.date_create,
                    date_update=self.request.date_update,
                    tags=self.request.tags)

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
