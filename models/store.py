from typing import List

from sqlalchemy.orm import Query

from db import db


class Store(db.Model):
    query: db.Query  # type: Query
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    items = db.relationship("Item", lazy="dynamic")

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
