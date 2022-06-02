from typing import Dict, List, Union

from sqlalchemy.orm import Query

from db import db

ItemJSON = Dict[str, Union[int, str, float]]


class Item(db.Model):
    query: db.Query  # type: Query
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    store = db.relationship("Store", back_populates="items")

    def __init__(self, name: str, price: float, store_id: int):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self) -> ItemJSON:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "store_id": self.store_id,
        }

    @classmethod
    def find_by_name(cls, name: str) -> "Item":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["Item"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
