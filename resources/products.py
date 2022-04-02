from flask import request
from flask_restful import Resource, reqparse

from models.products import ProductModel
from models.categories import CategoriesModel


class Product(Resource):
    """Product retrieve, create and delete"""

    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help='This field cannot be left blank!.'
    )
    parser.add_argument(
        'description',
        type=str,
        required=True,
        help='This field cannot be left blank!.'
    )
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='This field cannot be left blank!.'
    )
    parser.add_argument(
        'category_id',
        type=str,
        required=True,
        help='This field cannot be left blank!.'
    )
    parser.add_argument(
        'weight',
        type=str,
        required=True,
        help='This field cannot be left blank!.'
    )
    parser.add_argument(
        'units',
        type=str,
        required=True,
        help='This field cannot be left blank!.'
    )
    parser.add_argument(
        'featured',
        type=bool,
        required=True,
        help='This field cannot be left blank!.'
    )
    parser.add_argument(
        'discount',
        type=float,
        required=False,
        help='This field cannot be left blank!.'
    )

    def get(self):
        product_url = request.args.get("category")
        if product_url:
            category = CategoriesModel.query.filter_by(name=product_url).first()
            product = ProductModel.query.filter_by(category_id=category.id)
            if product is not None:
                return {
                           "products": [x.json() for x in product]
                       }, 200
            return {
                       "message": "Product not found."
                   }, 404
        return {
                   "products": [x.json() for x in ProductModel.find_all()]
               }, 200

    def post(self):
        data = Product.parser.parse_args()
        if ProductModel.find_by_name(data['name']):
            return {
                       "message": "A Product with name '{}' already exists.".format(data['name'])
                   }, 400

        product = ProductModel(**data)

        try:
            product.save_to_db()
        except ValueError:
            return {
                       "message": "An error occurred creating the category."
                   }, 500

        return product.json()
