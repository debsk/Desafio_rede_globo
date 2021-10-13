from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from domain.database.settings import Base


class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    def to_json(self):
        return vars(self)

    class Schema(BaseModel):
        id: Optional[int]
        name: str
