from ma import ma
from models.store import Store
from models.item import Item
from schemas.item import ItemSchema


class StoreSchema(ma.SQLAlchemyAutoSchema):
    items = ma.Nested(ItemSchema, many=True)

    class Meta:
        model = Store
        dump_only = ("id",)
        include_fk = True
