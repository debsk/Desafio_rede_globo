from sqlalchemy import Column, Integer, String, ARRAY
from domain.database.settings import Base


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    date_create = Column(String)
    date_update = Column(String)
    tags = Column(ARRAY(String))

    def to_json(self):
        return vars(self)


class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, index=True)
    tag_id = Column(Integer)
