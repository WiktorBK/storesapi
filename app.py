import os
from flask_jwt_extended import JWTManager
from flask import Flask 
from flask_restful import Api
from resources.user import UserRegister, User, UserLogin, UserList
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'top_secret'
api = Api(app)


jwt = JWTManager(app) 

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<string:username>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserList, '/users')



if __name__ == '__main__':
    app.run(port=5000, debug=True)