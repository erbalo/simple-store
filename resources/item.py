from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from models.item import Item
from schemas.item import ItemSchema

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)


class ItemResource(Resource):

    @classmethod
    def get(cls, name: str):
        item = Item.find_by_name(name)
        if item:
            return item_schema.dump(item), 200
        return {"message": "Item not found"}, 404

    @classmethod
    @jwt_required(fresh=True)
    def post(cls, name: str):
        if Item.find_by_name(name):
            return {
                       "message": "an item with name '{}' already exists".format(name)
                   }, 400

        item_json = request.get_json()
        item_json["name"] = name

        try:
            item = item_schema.load(item_json)
        except ValidationError as err:
            return err.messages, 400

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred while inserting the item"}, 500

        return item.json(), 201

    @classmethod
    @jwt_required()
    def delete(cls, name: str):
        item = Item.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "item deleted"}, 200
        return {"message": "item not found"}, 404

    @classmethod
    def put(cls, name: str):
        item_json = request.get_json()
        item = Item.find_by_name(name)

        if item:
            item.price = item_json["price"]
        else:
            item_json["name"] = name

            try:
                item = item_schema.load(item_json)
            except ValidationError as err:
                return err.messages, 400

        item.save_to_db()

        return item_schema.dump(item), 200


class ItemResourceList(Resource):
    @classmethod
    def get(cls):
        items = item_list_schema.dump(Item.find_all())
        return {"items": items}, 200
