from flask_restful import Resource, reqparse
from models.store import StoreModel


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
    type=str,
    required = True,
    help = 'Store needs a name'
    )

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return{'message': 'store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f'store named {name} already exists'}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()        
        except:
            return {'message': 'An error occurred inserting the store'}, 500
        
        return store.json(), 201

    def put(self, name):
        data = Store.parser.parse_args()
        if StoreModel.find_by_name(data['name']):
            return {'message': f"store named {data['name']} already exists"}

        store = StoreModel.find_by_name(name)

        if store is None:
            store = StoreModel(name)
        else:
            store.name = data['name']
        
        store.save_to_db()

        return store.json(), 201


    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': 'store deleted'}
        return {'message': f"Store named {name} doesn't exist"}
        


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}