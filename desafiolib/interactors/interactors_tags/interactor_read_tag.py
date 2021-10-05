from domain.database.settings import UserAlchemyAdapter
from domain.models.tag_models import Tag


class ReadTagRequestModel:
    def __init__(self, tag_id):
        self.tag_id = tag_id


class ReadTagResponseModel:
    def __init__(self, tag: Tag):
        self.tag = tag

    def __call__(self):
        return self.tag.to_json()


class ReadTagInteractor:
    def __init__(self, request: ReadTagRequestModel,
                 adapter: UserAlchemyAdapter()):
        self.request = request
        self.adapter = adapter

    def _get_read_tag(self):
        return self.adapter.tag_models(Tag). \
            filter(Tag.id == self.request.tag_id).first()

    def run(self):
        tag = self._get_read_tag()
        response = ReadTagResponseModel(tag)
        return response
