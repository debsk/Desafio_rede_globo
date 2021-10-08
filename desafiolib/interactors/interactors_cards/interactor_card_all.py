from typing import List
import json
from domain.database.settings import UserAlchemyAdapter
from domain.models.card_models import Card
from domain.models.tag_models import Tag

from fastapi import HTTPException


class AllCardRequestModel:
    def __init__(self, tag_id):
        self.tag_id = tag_id


class AllCardResponseModel:
    def __init__(self, cards: List[Card]):
        self.cards = cards

    def __call__(self):
        return self.cards


class AllCardInteractor:
    def __init__(self, request: AllCardRequestModel,
                 adapter: UserAlchemyAdapter):
        self.request = request
        self.adapter = adapter

    def _get_all_card(self):
        cards = []
        all_cards = self.adapter.query(Card).all()
        for card in all_cards:
            if not card.tags:
                continue

            for tag_name in json.loads(card.tags):
                if self.request.tag_id != tag_name:
                    continue
                cards.append(card)

        return cards

    def run(self):
        cards = self._get_all_card()
        response = AllCardResponseModel(cards)
        return response



