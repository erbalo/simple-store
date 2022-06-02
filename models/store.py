from typing import Dict, List, Union

from sqlalchemy.orm import Query

from db import db
from models.item import ItemJSON

StoreJSON = Dict[str, Union[int, str, List[ItemJSON]]]


class Store(db.Model):
    query: db.Query  # type: Query
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship("Item", lazy="dynamic")

    def __init__(self, name: str):
        self.name = name

    def json(self) -> StoreJSON:
        return {
            "id": self.id,
            "name": self.name,
            "items": [item.json() for item in self.items.all()],
        }

    @classmethod
    def find_by_name(cls, name: str) -> "Store":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["Store"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
