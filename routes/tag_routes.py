from fastapi import APIRouter

tag = APIRouter()


@tag.post("/create_tag")
def create_tag():
    return {}


@tag.get("/tag")
def read_tag():
    return {}


@tag.delete("/tag")
def delete_tag():
    return {}


@tag.put("/tag")
def update_tag():
    return {}
