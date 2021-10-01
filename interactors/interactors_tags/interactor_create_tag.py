from domain.database.settings import UserAlchemyAdapter
from domain.models.tag_models import Tag


class CreateTagResquestModel:
    def __init__(self, body):
        self.name = body.name


class CreateTagResponseModel:
    def __init__(self, tag: Tag):
        self.tag = tag

    def __call__(self):
        return self.tag.to_json()


class CreateTagInteractor:
    def __init__(self, request: CreateTagResquestModel,
                 adapter: UserAlchemyAdapter):
        self.request = request
        self.adapter = adapter

    def _create_tag(self):
        tag = Tag(name=self.request.name)
        return tag

    def _save_tag(self, tag):
        self.adapter.add(tag)
        self.adapter.commit()
        self.adapter.refresh(tag)

    def run(self):
        tag = self._create_tag()
        self._save_tag(tag)
        response = CreateTagResponseModel(tag)
        return response
