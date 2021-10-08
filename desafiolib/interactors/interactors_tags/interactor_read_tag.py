from domain.database.settings import UserAlchemyAdapter
from domain.models.tag_models import Tag
from fastapi import HTTPException


class ReadTagRequestModel:
    def __init__(self, tag_id):
        self.tag_id = tag_id


class ReadTagResponseModel:
    def __init__(self, tag: Tag):
        self.tag = tag

    def __call__(self):
        return self.tag


class ReadTagInteractor:
    def __init__(self, request: ReadTagRequestModel,
                 adapter: UserAlchemyAdapter()):
        self.request = request
        self.adapter = adapter

    def _get_read_tag(self):
        return self.adapter.query(Tag). \
            filter(Tag.id == self.request.tag_id).first()

    def _check_exist_read_card(self):
        tag = self._get_read_tag()
        if tag is None:
            raise HTTPException(status_code=400,
                                detail="Tag not exist")

    def run(self):
        tag = self._get_read_tag()
        self._check_exist_read_card(tag)
        response = ReadTagResponseModel(tag)
        return response
