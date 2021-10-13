from domain.database.settings import UserAlchemyAdapter
from domain.models.tag_models import Tag
from fastapi import HTTPException


class DeleteTagRequestModel:
    def __init__(self, tag_id):
        self.tag_id = tag_id


class DeleteTagResponseModel:
    def __init__(self, tag: Tag):
        self.tag = tag

    def __call__(self):
        return self.tag


class DeleteTagInteractor:
    def __init__(self, request: DeleteTagRequestModel,
                 adapter: UserAlchemyAdapter):
        self.request = request
        self.adapter = adapter

    def _get_tag(self):
        return self.adapter.query(Tag). \
            filter(Tag.id == self.request.tag_id).first()

    def _check_tag_delete(self):
        tag = self._get_tag()
        if tag is None:
            raise HTTPException(status_code=400,
                                detail="Tag not exist")
        else:
            return tag

    def _delete_tag(self, tag: Tag):
        self.adapter.query(Tag). \
            filter(Tag.id == tag.id).delete()
        self.adapter.commit()

        return {
            "status": 200,
            "message": "Tag was deleted",
            "tag": tag
        }

    def run(self):
        tag_validate = self._check_tag_delete()
        tag = self._delete_tag(tag_validate)
        response = DeleteTagResponseModel(tag)
        return response
