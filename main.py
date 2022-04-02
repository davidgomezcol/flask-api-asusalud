from flask import Flask
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, User, \
    UserLogin, UserLogout, TokenRefresh

from resources.categories import Categories
from resources.products import Product
from resources.orders import Orders

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = "4nnMxHba5txDkScHb7mmqQNHergbfGsbtbQZrzzYCxynuXZ6xR99gt"
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)

api.add_resource(UserRegister, '/register/')
api.add_resource(User, '/user/<int:user_id>/')
api.add_resource(UserLogin, '/login/')
api.add_resource(UserLogout, '/logout/')
api.add_resource(TokenRefresh, '/refresh/')
api.add_resource(Categories, '/category/')
api.add_resource(Product, '/products/')
api.add_resource(Orders, '/orders/')

if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(port=8000, debug=True)
