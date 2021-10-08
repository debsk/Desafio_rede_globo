from domain.database.settings import UserAlchemyAdapter
from domain.models.card_models import Card
from fastapi import HTTPException


class DeleteCardRequestModel:
    def __init__(self, card_id):
        self.card_id = card_id


class DeleteCardResponseModel:
    def __init__(self, card: Card):
        self.card = card

    def __call__(self):
        return self.card


class DeleteCardInteractor:
    def __init__(self, request: DeleteCardRequestModel,
                 adapter: UserAlchemyAdapter):
        self.request = request
        self.adapter = adapter

    def _get_card(self):
        return self.adapter.query(Card). \
            filter(Card.id == self.request.card_id).first()

    def _check_card_delete(self):
        card = self._get_card()
        if card is None:
            raise HTTPException(status_code=400,
                                detail="Card not exist")
        else:
            return card

    def _delete_card(self, card: Card):
        self.adapter.query(Card). \
            filter(Card.id == card.id).delete()
        self.adapter.commit()

        return {
            "status": 200,
            "message": "Card was deleted",
            "card": card
        }

    def run(self):
        card_validate = self._check_card_delete()
        card = self._delete_card(card_validate)
        response = DeleteCardResponseModel(card)
        return response
