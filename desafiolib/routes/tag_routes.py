from fastapi import APIRouter, Depends
from desafiolib.interactors.interactors_tags.interactor_create_tag import \
    CreateTagRequestModel, CreateTagInteractor
from domain.database.settings import UserAlchemyAdapter, engine
from domain.models import tag_models
from sqlalchemy.orm import Session

tag_models.Base.metadata.create_all(bind=engine)

tag = APIRouter()


@tag.post("/tag")
def create_tag(json_body: tag_models.Tag.Schema,
               adapter: Session = Depends(UserAlchemyAdapter)):
    request = CreateTagRequestModel(json_body)
    interactor = CreateTagInteractor(request, adapter)

    result = interactor.run()

    return result()


@tag.get("/tag")
def read_tag():
    return {}


@tag.delete("/tag")
def delete_tag():
    return {}


@tag.put("/tag")
def update_tag():
    return {}
