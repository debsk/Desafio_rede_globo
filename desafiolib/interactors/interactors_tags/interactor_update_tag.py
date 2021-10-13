from domain.database.settings import UserAlchemyAdapter
from domain.models.tag_models import Tag


class UpdateTagRequestModel:
    def __init__(self, body):
        self.id = body.id
        self.name = body.name


class UpdateTagResponseModel:
    def __init__(self, tag: Tag):
        self.tag = tag

    def __call__(self):
        return self.tag.to_json()


class UpdateTagInteractor:
    def __init__(self, request: UpdateTagRequestModel,
                 adapter: UserAlchemyAdapter):
        self.request = request
        self.adapter = adapter

    def _get_tag(self):
        return self.adapter.query(Tag). \
            filter(Tag.id == self.request.id).first()

    def _update_tag(self, tag: Tag):
        tag.name = self.request.name
        self.adapter.commit()
        return tag

    def run(self):
        tag = self._get_tag()
        self._update_tag(tag)
        response = UpdateTagResponseModel(tag)
        return response
