from flask_restful import Resource

from models.store import Store


class StoreResource(Resource):
    @classmethod
    def get(cls, name: str):
        store = Store.find_by_name(name)
        if store:
            return store.json()
        return {"message": "Store not found."}, 404

    @classmethod
    def post(cls, name: str):
        if Store.find_by_name(name):
            return (
                {"message": "A store with name '{}' already exists.".format(name)},
                400,
            )

        store = Store(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred while creating the store."}, 500

        return store.json(), 201

    @classmethod
    def delete(cls, name: str):
        store = Store.find_by_name(name)
        if store:
            store.delete_from_db()

        return {"message": "Store deleted."}


class StoreResourceList(Resource):
    @classmethod
    def get(cls):
        return {"stores": [store.json() for store in Store.find_all()]}
