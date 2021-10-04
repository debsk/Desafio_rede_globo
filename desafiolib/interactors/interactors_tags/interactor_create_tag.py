from domain.database.settings import UserAlchemyAdapter
from domain.models.tag_models import Tag


class CreateTagRequestModel:
    def __init__(self, body):
        self.name = body.name


class CreateTagResponseModel:
    def __init__(self, tag: Tag):
        self.tag = tag

    def __call__(self):
        return self.tag.to_json()


class CreateTagInteractor:
    def __init__(self, request: CreateTagRequestModel,
                 adapter: UserAlchemyAdapter):
        self.request = request
        self.adapter = adapter

    def _create_tag(self):
        tag = Tag(name=self.request.name)

        self.adapter.add(tag)
        self.adapter.commit()
        self.adapter.refresh(tag)

        return tag

    def run(self):
        tag = self._create_tag()
        response = CreateTagResponseModel(tag)
        return response
