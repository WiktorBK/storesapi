from flask_restful import Resource, reqparse
from models.item import ItemModel


items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
            type= float,
            required= True,
            help="This field cannot be left blank"
        )
    parser.add_argument('store_id',
            type= int,
            required= True,
            help="Every item needs a store id."
        )


    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {'message': 'Item not found'}, 404

    def post(self, name):
        data = Item.parser.parse_args()
        if ItemModel.find_by_name_in_store(name, data['store_id']):
            return {'message': f"An item with name '{name}' already exists in that store."}, 400
        
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item"}, 500
       
        return item.json(), 201

    def delete(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name_in_store(name, data['store_id'])
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'} 
        return {'message': f"Item named {name} doesn't exist in that store"}, 400

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name_in_store(name, data['store_id'])


        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}

