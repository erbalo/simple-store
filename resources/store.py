from flask_restful import Resource

from models.store import Store
from schemas.store import StoreSchema

store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)


class StoreResource(Resource):
    @classmethod
    def get(cls, name: str):
        store = Store.find_by_name(name)
        if store:
            return store_schema.dump(store), 200
        return {"message": "Store not found."}, 404

    @classmethod
    def post(cls, name: str):
        if Store.find_by_name(name):
            return (
                {"message": "A store with name '{}' already exists.".format(name)},
                400,
            )

        store = Store(name=name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred while creating the store."}, 500

        return store_schema.dump(store), 201

    @classmethod
    def delete(cls, name: str):
        store = Store.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message": "Store deleted."}, 204

        return {"message": "store not found"}, 404


class StoreResourceList(Resource):
    @classmethod
    def get(cls):
        stores = store_list_schema.dump(Store.find_all())
        return {"stores": stores}, 200
