from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_required, 
    get_jwt_identity)
from models.user import UserModel
import hmac

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
        type = str,
        required= True,
        help="This field cannot be left blank"
    )
_user_parser.add_argument('password',
    type= str,
    required= True,
    help="This field cannot be left blank"
    )



class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "username already taken"}, 400
        
        user = UserModel(**data)
        user.save_to_db()


        return {"message": "User created"}, 201
    
class User(Resource):
    def get(self, username):
        user = UserModel.find_by_username(username)
        if user:
            return user.json()
        else:
            return {'message': f'User named {username} was not found'}, 404

    def delete(self, username):
        user = UserModel.find_by_username(username)
        if user:
            user.delete_from_db()
            return {'message': 'User deleted'} 
        return {'message': f"User named {username} doesn't exist"}, 404

class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])

        if user and hmac.compare_digest(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token, 
                'refresh_token': refresh_token
            }
        return {'message': 'Invalid credentials'}, 401

class UserList(Resource):
    def get(self):
        return {'items': [user.json() for user in UserModel.find_all()]}

class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}