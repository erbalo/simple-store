from ma import ma
from models.item import Item
from models.store import Store


class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        load_only = ("store",)
        dump_only = ("id",)
        include_fk = True
