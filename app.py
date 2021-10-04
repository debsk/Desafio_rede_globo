from desafiolib.routes import tag_routes, card_routes
from fastapi import FastAPI

app = FastAPI(app_name='desafio')

app.include_router(card_routes.card)
app.include_router(tag_routes.tag)
