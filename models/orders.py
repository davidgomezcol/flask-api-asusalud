import datetime
import string
import random

from db import db


def tracking_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class OrderModel(db.Model):
    """Order Model"""

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    order_status = db.Column(db.String(20), default="Created")
    payment_mode = db.Column(db.String(255))
    tracking_number = db.Column(db.String(150), default=tracking_generator(), unique=True)
    order_total = db.Column(db.Float(precision=2))
    is_paid = db.Column(db.Boolean, default=False)
    order_date = db.Column(db.DateTime, default=datetime.datetime.now)
    shipped_date = db.Column(db.DateTime)

    def __init__(self, user_id, order_status, payment_mode,
                 tracking_number, order_total, is_paid):
        self.user_id = user_id
        self.order_status = order_status
        self.payment_mode = payment_mode
        self.tracking_number = tracking_number
        self.order_total = order_total
        self.is_paid = is_paid

    def json(self):
        return {
            "id": self.id,
            "user": self.user_id,
            "order_status": self.order_status,
            "payment_mode": self.payment_mode,
            "tracking_number": self.tracking_number,
            "order_total": self.order_total,
            "is_paid": self.is_paid,
            "order_date": self.order_date,
            "shipped_date": self.shipped_date,
        }

    @classmethod
    def find_by_tracking_number(cls, tracking_number):
        return cls.query.filter_by(tracking_number=tracking_number).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
