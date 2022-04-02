from flask import request
from flask_restful import Resource, reqparse

from models.orders import OrderModel


class Orders(Resource):
    """Orders C.R.U.D endpoint"""
    parser = reqparse.RequestParser()

    parser.add_argument(
        'user',
        type=int,
        required=False,
        help='This field cannot be left blank!.'
    )
    parser.add_argument(
        'order_status',
        type=str,
        required=False,
    )
    parser.add_argument(
        'payment_mode',
        type=str,
        required=True,
        help='This field cannot be left blank!.'
    )
    parser.add_argument(
        'is_paid',
        type=bool,
        required=False,
    )
    parser.add_argument(
        'shipped_date',
        type=str,
        required=False,
    )

    def get(self):
        return {
            "message": [x.json() for x in OrderModel.find_all()]
        }, 200

    def post(self):
        data = Orders.parser.parse_args()

        order = OrderModel(user=request.user, **data)

        try:
            order.save_to_db()
        except ValueError:
            return {
                       "message": "An error occurred creating the category."
                   }, 500

        return order.json()
