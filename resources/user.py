from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, \
    jwt_required, get_jwt_identity, get_jwt

from models.user import UserModel
from blacklist import BLACKLIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    'username',
    type=str,
    required=True,
    help='This field cannot be blank.',
)
_user_parser.add_argument(
    'password',
    type=str,
    required=True,
    help='This field cannot be blank.',
)


class UserRegister(Resource):
    """Register an User"""

    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {
                       "message": "A user with that username already exists.",
                   }, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {
                   "message": "User created successfully."
               }, 201


class User(Resource):
    """Retrieve and Delete User"""

    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {
                       "message": "User not found.",
                   }, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {
                       "message": "User not found."
                   }, 400
        user.delete_from_db()
        return {
                   "message": "User deleted."
               }, 200


class UserLogin(Resource):
    """Handles the login of a registered user"""

    @classmethod
    def post(cls):
        """get data from parser, find user in database,
        check password, create access token, create refresh
        token and return them"""
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                       "access_token": access_token,
                       "refresh_token": refresh_token
                   }, 200

        return {
                   "message": "Invalid credentials."
               }, 401


class UserLogout(Resource):
    """Handles the logout of an user"""

    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']  # jti is "JWT ID", a unique identifier for JWT
        BLACKLIST.add(jti)
        return {
                   "message": "Successfully logged out."
               }, 200


class TokenRefresh(Resource):
    """Token Refresher"""

    @jwt_required(refresh=True, fresh=False)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_refresh_token(identity=current_user)
        return {
                   "access_token": new_token
               }, 200
