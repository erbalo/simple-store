from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from models.item import Item


class ItemResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="This field cannot be left blank"
    )
    parser.add_argument(
        "store_id", type=int, required=True, help="Every item needs a store_id"
    )

    def get(self, name: str):
        item = Item.find_by_name(name)

        if item:
            return item.json(), 200
        return {"message": "Item not found"}, 404

    @jwt_required(fresh=True)
    def post(self, name: str):
        if Item.find_by_name(name):
            return {
                "message": "an item with name '{}' already exists".format(name)
            }, 400

        data = ItemResource.parser.parse_args()
        item = Item(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred while inserting the item"}, 500

        return item.json(), 201

    @jwt_required()
    def delete(self, name: str):
        item = Item.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "item deleted"}, 200
        return {"message": "item not found"}, 404

    def put(self, name: str):
        data = ItemResource.parser.parse_args()
        item = Item.find_by_name(name)

        if item:
            item.price = data["price"]
        else:
            item = Item(name, **data)

        item.save_to_db()

        return item.json(), 200


class ItemResourceList(Resource):
    def get(self):
        items = [item.json() for item in Item.find_all()]
        return {"items": items}, 200
