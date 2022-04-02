from flask import request
from flask_restful import Resource, reqparse

from models.categories import CategoriesModel


class Categories(Resource):
    """Categories Resource, retrieve all and create new"""

    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help='This field cannot be left blank!.'
    )

    def get(self):
        category_url = request.args.get("name")
        if category_url:
            category = CategoriesModel.find_by_name(category_url)
            if category is not None:
                return {
                    "name": category.name
                }, 200
            return {
                "message": "Category not found."
            }, 404
        return {
                   "categories": [x.json() for x in CategoriesModel.find_all()]
               }, 200

    def post(self):
        data = Categories.parser.parse_args()
        if CategoriesModel.find_by_name(data['name']):
            return {
                       "message": "A category with name '{}' already exists.".format(data['name'])
                   }, 400

        category = CategoriesModel(data['name'])

        try:
            category.save_to_db()
        except ValueError:
            return {
                       "message": "An error occurred creating the category."
                   }, 500

        return category.json()
