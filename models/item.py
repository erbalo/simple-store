from typing import List

from sqlalchemy.orm import Query

from db import db


class Item(db.Model):
    query: db.Query  # type: Query
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    price = db.Column(db.Float(precision=2), nullable=False)

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
    store = db.relationship("Store", back_populates="items")

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
