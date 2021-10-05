from domain.database.settings import UserAlchemyAdapter
from domain.models.card_models import Card


class ReadCardRequestModel:
    def __init__(self, card_id):
        self.card_id = card_id


class ReadCardResponseModel:
    def __init__(self, card: Card):
        self.card = card

    def __call__(self):
        return self.card.to_json()


class ReadCardInteractor:
    def __init__(self, request: ReadCardRequestModel,
                 adapter: UserAlchemyAdapter):
        self.request = request
        self.adapter = adapter

    def _get_read_card(self):
        return self.adapter.card_models(Card). \
            filter(Card.id == self.request.card_id).first()

    def run(self):
        card = self._get_read_card()
        response = ReadCardResponseModel(card)
        return response
