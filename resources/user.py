import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
            type = str,
            required= True,
            help="This field cannot be left blank"
        )
    parser.add_argument('password',
        type= str,
        required= True,
        help="This field cannot be left blank"
     )

    def post(self):
        data = UserRegister.parser.parse_args()
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