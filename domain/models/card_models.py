from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime
from domain.database.settings import Base
import datetime


class Card(Base):
    __tablename__ = "card"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    date_create = Column(DateTime, default=datetime.datetime.utcnow)
    date_update = Column(DateTime, default=datetime.datetime.utcnow)
    tags = Column(String)

    def to_json(self):
        return vars(self)

    class Schema(BaseModel):
        text: str
        tags: list


