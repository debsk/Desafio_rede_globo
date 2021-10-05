from fastapi import APIRouter, Depends

from desafiolib.interactors.interactors_tags.interactor_create_tag import \
    CreateTagRequestModel, CreateTagInteractor
from desafiolib.interactors.interactors_tags.interactor_read_tag import \
    ReadTagRequestModel, ReadTagInteractor
from domain.database.settings import UserAlchemyAdapter, engine
from domain.models import tag_models
from sqlalchemy.orm import Session

tag_models.Base.metadata.create_all(bind=engine)

tag = APIRouter()


@tag.post("/tag")
def post_create_tag(json_body: tag_models.Tag.Schema,
               adapter: Session = Depends(UserAlchemyAdapter)):
    request = CreateTagRequestModel(json_body)
    interactor = CreateTagInteractor(request, adapter)

    result = interactor.run()

    return result()


@tag.get("/tag/{tag_id}")
def get_read_tag(tag_id,
             adapter: Session = Depends(UserAlchemyAdapter)):
    request = ReadTagRequestModel(tag_id)

    interactor = ReadTagInteractor(request, adapter)

    result = interactor.run()

    return result()


@tag.delete("/tag")
def delete_tag():
    return {}


@tag.put("/tag")
def put_update_tag():
    return {}
