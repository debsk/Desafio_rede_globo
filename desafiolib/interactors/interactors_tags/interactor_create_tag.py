from domain.database.settings import UserAlchemyAdapter
from domain.models.tag_models import Tag
from fastapi import HTTPException


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

    def _get_tag(self):
        return self.adapter.query(Tag). \
            filter(Tag.name == self.request.name).first()

    def _check_exist_tag(self):
        tag = self._get_tag()
        if tag is not None:
            raise HTTPException(status_code=400,
                                detail="Tag already create")

    def _create_tag(self):
        tag = Tag(name=self.request.name)

        self.adapter.add(tag)
        self.adapter.commit()
        self.adapter.refresh(tag)

        return tag

    def run(self):
        self._check_exist_tag()
        tag = self._create_tag()
        response = CreateTagResponseModel(tag)
        return response
